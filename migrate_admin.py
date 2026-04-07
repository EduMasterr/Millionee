import os

admin_js_path = 'js/admin.js'
with open(admin_js_path, 'r', encoding='utf-8') as f:
    admin_js = f.read()

# 1. Dashboard Stats
stats_old = """function updateDashboardStats() {
    const visitors = localStorage.getItem('million_total_visitors') || 0;
    const players = localStorage.getItem('million_total_players') || 0;
    document.getElementById('total-visitors').innerText = Number(visitors).toLocaleString();
    document.getElementById('total-players').innerText = Number(players).toLocaleString();
}"""

stats_new = """function updateDashboardStats() {
    db.ref('stats').on('value', (snapshot) => {
        const data = snapshot.val() || {};
        const visitors = data.visitors || 0;
        const players = data.players || 0;
        document.getElementById('total-visitors').innerText = Number(visitors).toLocaleString();
        document.getElementById('total-players').innerText = Number(players).toLocaleString();
    });
}"""
admin_js = admin_js.replace(stats_old, stats_new)

# 2. Reset Stats
reset_old = """function resetStats() {
    if (confirm("هل أنت متأكد من تصفير عداد الزيارات واللاعبين؟")) {
        localStorage.setItem('million_total_visitors', 0);
        localStorage.setItem('million_total_players', 0);
        localStorage.removeItem('million_leaderboard');
        localStorage.setItem('million_total_visitors', 0);
        localStorage.setItem('million_total_players', 0);
        alert('تم التصفير والحذف بنجاح!');
        updateDashboardStats(); // Reset leaderboard entirely as requested
        updateDashboardStats();
        alert('تم تصفير العدادات ولوحة الشرف بنجاح!');
        localStorage.setItem('million_total_players', 0);
        updateDashboardStats();
    }
}"""

reset_new = """function resetStats() {
    if (confirm("تحذير: هل أنت متأكد من تصفير العدادات ولوحة الشرف؟ هذا الإجراء لا يمكن التراجع عنه!")) {
        db.ref('stats').set({ visitors: 0, players: 0 });
        db.ref('leaderboard').remove();
        alert('تم التصفير والحذف من قاعدة البيانات العالمية بنجاح!');
    }
}"""
admin_js = admin_js.replace(reset_old, reset_new)

# 3. Render Messages
render_old = """function renderMessages() {
    const container = document.getElementById('messages-container');
    let messages = [];
    try {
        messages = JSON.parse(localStorage.getItem('million_feedback')) || [];
        if (!Array.isArray(messages)) messages = [];
    } catch (e) {
        console.error("Failed to parse messages:", e);
    }
    
    if (messages.length === 0) {
        container.innerHTML = '<p style="text-align:center; padding:20px; color:#aaa;">لا توجد رسائل حالياً</p>';
        return;
    }
    
    const messagesCopy = [...messages];
    container.innerHTML = messagesCopy.reverse().map((msg, idx) => {
        const date = new Date(msg.date).toLocaleString('ar-EG');
        return `
            <div class="glass-panel" style="padding:15px; border-right:4px solid var(--gold); border-bottom:none; background:rgba(255,255,255,0.05);">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <strong style="color:var(--gold);"><i class="fas fa-user-edit"></i> ${escapeHtml(msg.name)} (${msg.age} سنة)</strong>
                    <span style="font-size:0.8rem; color:#888;">${date}</span>
                </div>
                <p style="margin:0; line-height:1.6; color:#eee;">${escapeHtml(msg.text)}</p>
                <div style="text-align:left; margin-top:10px;">
                    <button class="btn" style="background:transparent; border:1px solid var(--danger); color:var(--danger); padding:3px 10px; font-size:0.8rem;" onclick="deleteMessage(${messages.length - 1 - idx})">
                        <i class="fas fa-trash"></i> حذف
                    </button>
                </div>
            </div>
        `;
    }).join('');
}"""

render_new = """function renderMessages() {
    const container = document.getElementById('messages-container');
    container.innerHTML = '<p style="text-align:center; padding:20px; color:white;"><i class="fas fa-spinner fa-spin"></i> جاري جلب الرسائل من السيرفر...</p>';
    
    db.ref('feedback').on('value', (snapshot) => {
        let messages = [];
        snapshot.forEach((child) => {
            messages.push({
                key: child.key,
                ...child.val()
            });
        });
        
        if (messages.length === 0) {
            container.innerHTML = '<p style="text-align:center; padding:20px; color:#aaa;">لا توجد رسائل حالياً</p>';
            return;
        }
        
        container.innerHTML = messages.reverse().map((msg) => {
            const date = new Date(msg.date).toLocaleString('ar-EG');
            return `
                <div class="glass-panel" style="padding:15px; border-right:4px solid var(--gold); border-bottom:none; background:rgba(255,255,255,0.05);">
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <strong style="color:var(--gold);"><i class="fas fa-user-edit"></i> ${escapeHtml(msg.name)} (${msg.age} سنة)</strong>
                        <span style="font-size:0.8rem; color:#888;">${date}</span>
                    </div>
                    <p style="margin:0; line-height:1.6; color:#eee;">${escapeHtml(msg.text)}</p>
                    <div style="text-align:left; margin-top:10px;">
                        <button class="btn" style="background:transparent; border:1px solid var(--danger); color:var(--danger); padding:3px 10px; font-size:0.8rem;" onclick="deleteMessage('${msg.key}')">
                            <i class="fas fa-trash"></i> حذف
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    });
}"""
admin_js = admin_js.replace(render_old, render_new)

# 4. Delete specific Message
delete_old = """function deleteMessage(index) {
    let messages = [];
    try {
        messages = JSON.parse(localStorage.getItem('million_feedback')) || [];
        if (!Array.isArray(messages)) messages = [];
    } catch(e) {
        messages = [];
    }
    if (messages.length > index) {
        messages.splice(index, 1);
        localStorage.setItem('million_feedback', JSON.stringify(messages));
    }
    renderMessages();
}"""

delete_new = """function deleteMessage(key) {
    if(confirm("هل متأكد من حذف هذه الرسالة نهائياً؟")) {
        db.ref('feedback/' + key).remove();
    }
}"""
admin_js = admin_js.replace(delete_old, delete_new)

# 5. Clear all Messages
clear_old = """function clearAllMessages() {
    if (confirm("هل أنت متأكد من حذف جميع الرسائل والمقترحات؟")) {
        localStorage.removeItem('million_feedback');
        renderMessages();
    }
}"""

clear_new = """function clearAllMessages() {
    if (confirm("تحذير: هل أنت متأكد من حذف جميع الرسائل والمقترحات من السيرفر نهائياً؟")) {
        db.ref('feedback').remove();
    }
}"""
admin_js = admin_js.replace(clear_old, clear_new)

with open(admin_js_path, 'w', encoding='utf-8') as f:
    f.write(admin_js)

print("Firebase successfully integrated into admin.js via script.")
