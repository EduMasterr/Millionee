import os

app_js_path = 'js/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    app_js = f.read()

# 1. Update Visitors Logic
visitors_old = """    // Increment Visitors
    let vCount = Number(localStorage.getItem('million_total_visitors')) || 0;
    localStorage.setItem('million_total_visitors', vCount + 1);

    // Update home page stats
    const homeVisitors = document.getElementById('home-visitors');
    const homePlayers = document.getElementById('home-players');
    if (homeVisitors) homeVisitors.textContent = (vCount + 1).toLocaleString();
    const pCount = Number(localStorage.getItem('million_total_players')) || 0;
    if (homePlayers) homePlayers.textContent = pCount.toLocaleString();"""

visitors_new = """    // Increment Visitors & Players via Firebase Transactions
    const homeVisitors = document.getElementById('home-visitors');
    const homePlayers = document.getElementById('home-players');
    
    // Listen to values dynamically
    db.ref('stats/visitors').on('value', (s) => {
        if(homeVisitors) homeVisitors.textContent = (s.exists() ? s.val() : 0).toLocaleString();
    });
    db.ref('stats/players').on('value', (s) => {
        if(homePlayers) homePlayers.textContent = (s.exists() ? s.val() : 0).toLocaleString();
    });

    // Transaction to safely increment visitors globally
    db.ref('stats/visitors').transaction((current) => {
        return (current || 0) + 1;
    });"""
app_js = app_js.replace(visitors_old, visitors_new)

# 2. Update Total Players Increment
players_old = """    // Increment Total Players
    let pCount = Number(localStorage.getItem('million_total_players')) || 0;
    localStorage.setItem('million_total_players', pCount + 1);"""

players_new = """    // Increment Total Players Globally
    db.ref('stats/players').transaction((current) => {
        return (current || 0) + 1;
    });"""
app_js = app_js.replace(players_old, players_new)

# 3. Save to Leaderboard
save_lb_old = """function saveToLeaderboard(name, age, score) {
    let lb = JSON.parse(localStorage.getItem(LEADERBOARD_KEY)) || [];
    lb.push({ name, age, score: Number(score), date: new Date().toISOString() });
    
    // Sort descending by score. If scores are equal, sort by newest date.
    lb.sort((a,b) => {
        if (b.score === a.score) {
            return new Date(b.date) - new Date(a.date);
        }
        return b.score - a.score;
    });
    
    lb = lb.slice(0, 10);
    localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(lb));
}"""

save_lb_new = """function saveToLeaderboard(name, age, score) {
    db.ref('leaderboard').push({
        name: name,
        age: age,
        score: Number(score),
        date: new Date().toISOString()
    });
}"""
app_js = app_js.replace(save_lb_old, save_lb_new)

# 4. Show Leaderboard
show_lb_old = """function showLeaderboard() {
    dom.startScreen.classList.remove('active');
    dom.leaderboardModal.classList.add('active');
    
    let lb = JSON.parse(localStorage.getItem(LEADERBOARD_KEY)) || [];
    dom.leaderboardList.innerHTML = '';
    
    if (lb.length === 0) {
        dom.leaderboardList.innerHTML = '<p style="color: white; text-align: center;">لا يوجد أبطال حتى الآن. كن أنت الأول!</p>';
        return;
    }
    
    lb.forEach((player, index) => {
        const item = document.createElement('div');
        item.className = 'rank-item';
        
        let iconColor = 'rgba(255,255,255,0.5)';
        if (index === 0) { item.classList.add('top-1'); iconColor = '#D4AF37'; }
        else if (index === 1) { item.classList.add('top-2'); iconColor = '#C0C0C0'; }
        else if (index === 2) { item.classList.add('top-3'); iconColor = '#CD7F32'; }
        
        item.innerHTML = `
            <div class="rank-name">
                <span style="color: ${iconColor}; font-weight: bold; width: 20px;">#${index + 1}</span>
                <span>${player.name} <small style="color: #aaa; font-size: 0.8rem;">(${player.age}س)</small></span>
            </div>
            <div class="rank-score">${player.score.toLocaleString()} 💰</div>
        `;
        dom.leaderboardList.appendChild(item);
    });
}"""

show_lb_new = """function showLeaderboard() {
    dom.startScreen.classList.remove('active');
    dom.leaderboardModal.classList.add('active');
    dom.leaderboardList.innerHTML = '<p style="color: white; text-align: center;"><i class="fas fa-spinner fa-spin"></i> جاري التحميل من فايربيس...</p>';
    
    db.ref('leaderboard').once('value').then((snapshot) => {
        let lb = [];
        snapshot.forEach((child) => {
            const p = child.val();
            if(p && p.name && p.name.toLowerCase() !== 'admin') {
                lb.push(p);
            }
        });
        
        lb.sort((a,b) => {
            if (b.score === a.score) return new Date(b.date) - new Date(a.date);
            return b.score - a.score;
        });
        
        lb = lb.slice(0, 10);
        dom.leaderboardList.innerHTML = '';
        
        if (lb.length === 0) {
            dom.leaderboardList.innerHTML = '<p style="color: white; text-align: center;">لا يوجد أبطال حتى الآن. كن أنت الأول!</p>';
            return;
        }

        lb.forEach((player, index) => {
            const item = document.createElement('div');
            item.className = 'rank-item';
            
            let iconColor = 'rgba(255,255,255,0.5)';
            if (index === 0) { item.classList.add('top-1'); iconColor = '#D4AF37'; }
            else if (index === 1) { item.classList.add('top-2'); iconColor = '#C0C0C0'; }
            else if (index === 2) { item.classList.add('top-3'); iconColor = '#CD7F32'; }
            
            item.innerHTML = `
                <div class="rank-name">
                    <span style="color: ${iconColor}; font-weight: bold; width: 20px;">#${index + 1}</span>
                    <span>${player.name} <small style="color: #aaa; font-size: 0.8rem;">(${player.age}س)</small></span>
                </div>
                <div class="rank-score">${player.score.toLocaleString()} 💰</div>
            `;
            dom.leaderboardList.appendChild(item);
        });
    });
}"""
app_js = app_js.replace(show_lb_old, show_lb_new)

# 5. Feedback Logic (Double block replacement issue avoided)
fb_old = """// ---- Feedback Logic ----
// ---- Feedback Logic ----
document.getElementById('submit-feedback-btn').addEventListener('click', async () => {
    const text = document.getElementById('feedback-text').value.trim();
    const name = document.getElementById('player-name').value.trim() || 'لاعب مجهول';
    const age = document.getElementById('player-age').value.trim() || '??';

    if (!text) {
        showCustomAlert('يرجى كتابة رسالتك قبل الإرسال!', 'fa-exclamation-circle');
        return;
    }

    let feedback = JSON.parse(localStorage.getItem('million_feedback')) || [];
    feedback.push({
        name,
        age,
        text,
        date: new Date().toISOString()
    });

    localStorage.setItem('million_feedback', JSON.stringify(feedback));
    document.getElementById('feedback-text').value = '';
    
    await showCustomAlert('تم استلام رسالتك بنجاح! شكراً لك.', 'fa-heart');
});"""

fb_new = """// ---- Feedback Logic ----
document.getElementById('submit-feedback-btn').addEventListener('click', async () => {
    const text = document.getElementById('feedback-text').value.trim();
    const name = document.getElementById('player-name').value.trim() || 'لاعب مجهول';
    const age = document.getElementById('player-age').value.trim() || '??';

    if (!text) {
        showCustomAlert('يرجى كتابة رسالتك قبل الإرسال!', 'fa-exclamation-circle');
        return;
    }

    db.ref('feedback').push({
        name: name,
        age: age,
        text: text,
        date: new Date().toISOString()
    }).then(async () => {
        document.getElementById('feedback-text').value = '';
        await showCustomAlert('تم إرسال اقتراحك للسيرفر بنجاح! شكراً لك.', 'fa-paper-plane');
    });
});"""
if fb_old in app_js:
    app_js = app_js.replace(fb_old, fb_new)
else:
    # Just in case the duplicate comment isn't there
    fb_old_single = fb_old.replace("// ---- Feedback Logic ----\n// ---- Feedback Logic ----", "// ---- Feedback Logic ----")
    app_js = app_js.replace(fb_old_single, fb_new)

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Firebase successfully integrated into app.js via script.")
