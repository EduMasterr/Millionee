// Using the 'db' variable initialized in firebase_init.js
let allQuestions = []; // flat array of ALL questions
let filteredQuestions = [];
let currentPage = 1;
const PAGE_SIZE = 25;

// Login logic
function checkLoginState() {
    if (sessionStorage.getItem('admin_logged_in') === 'true') {
        document.getElementById('login-view').style.display = 'none';
        document.getElementById('editor-view').style.display = 'block';
    // Ensure visibility
        initEditor();
        updateDashboardStats();
        renderMessages();
    }
}

function login() {
    const u = document.getElementById('admin-user').value;
    const p = document.getElementById('admin-pass').value;

    if (u === 'admin' && p === 'admin135') {
        sessionStorage.setItem('admin_logged_in', 'true');
        document.getElementById('login-view').style.display = 'none';
        document.getElementById('editor-view').style.display = 'block';
    // Ensure visibility
        initEditor();
        updateDashboardStats();
        renderMessages();
    } else {
        alert("بيانات الدخول خاطئة!");
    }
}

window.onload = checkLoginState;

function initEditor() {
    const saved = localStorage.getItem('admin_pending_db');
    if (saved) {
        db = JSON.parse(saved);
    } else {
        db = JSON.parse(JSON.stringify(window.QUESTIONS_DATA));
    }

    // Flatten ALL questions from ALL keys (including non-numeric keys like "2021", "2022"...)
    allQuestions = [];
    const allKeys = Object.keys(db);
    allKeys.forEach(key => {
        if (Array.isArray(db[key])) {
            db[key].forEach((q, idx) => {
                allQuestions.push({
                    poolKey: key,
                    index: idx,
                    data: q
                });
            });
        }
    });

    document.getElementById('db-stats').innerHTML = `
        <div>إجمالي الأسئلة: <strong class="gold">${allQuestions.length}</strong></div>
        <div>(موزعة على ${allKeys.length} مستوى)</div>
    `;

    // Show all questions by default
    filteredQuestions = [...allQuestions];
    currentPage = 1;
    renderResults();
}

function performSearch() {
    const q = document.getElementById('search-input').value.trim().toLowerCase();

    if (!q) {
        filteredQuestions = [...allQuestions];
    } else {
        filteredQuestions = allQuestions.filter(res => {
            const inQ = res.data.question && res.data.question.toLowerCase().includes(q);
            const inOpts = res.data.options && res.data.options.some(opt => opt.toLowerCase().includes(q));
            const inAns = res.data.answer && res.data.answer.toLowerCase().includes(q);
            return inQ || inOpts || inAns;
        });
    }

    currentPage = 1;
    renderResults();
}

function renderResults() {
    const container = document.getElementById('results-container');
    const totalPages = Math.ceil(filteredQuestions.length / PAGE_SIZE);
    const start = (currentPage - 1) * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, filteredQuestions.length);
    const pageItems = filteredQuestions.slice(start, end);

    if (filteredQuestions.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; color: var(--danger); padding: 20px;">
                <i class="fas fa-times-circle" style="font-size: 3rem; margin-bottom: 15px;"></i>
                <p>لم يتم العثور على أي أسئلة تطابق بحثك</p>
            </div>
        `;
        return;
    }

    // Search result count + pagination controls
    let html = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; flex-wrap:wrap; gap:10px;">
            <div style="color:var(--success);">
                يُعرض <strong>${start + 1}</strong> - <strong>${end}</strong> من <strong>${filteredQuestions.length}</strong> سؤال
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
                <button class="btn" style="padding:6px 14px; font-size:0.85rem;" onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled style="opacity:0.4;cursor:not-allowed;"' : ''}>
                    <i class="fas fa-chevron-right"></i> السابق
                </button>
                <span style="color:#aaa; font-size:0.9rem;">صفحة ${currentPage} / ${totalPages}</span>
                <button class="btn" style="padding:6px 14px; font-size:0.85rem;" onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled style="opacity:0.4;cursor:not-allowed;"' : ''}>
                    التالي <i class="fas fa-chevron-left"></i>
                </button>
            </div>
        </div>
    `;

    pageItems.forEach((res, i) => {
        const absIdx = start + i;
        const qData = res.data;
        const opts = qData.options || ['', '', '', ''];
        html += `
            <div class="question-card" id="card-${absIdx}">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:0.85rem; color: #aaa; flex-wrap:wrap; gap:5px;">
                    <span>معرف (ID): <strong style="color:var(--gold)">${qData.id || 'N/A'}</strong></span>
                    <span>المستوى: <strong style="color:var(--accent)">Pool ${res.poolKey}</strong></span>
                    <span style="color:#666;">${start + i + 1} / ${filteredQuestions.length}</span>
                </div>

                <label>نص السؤال:</label>
                <input type="text" class="q-input" id="edit-q-${absIdx}" value="${escapeHtml(qData.question || '')}">

                <label>الخيارات الأربعة:</label>
                <input type="text" class="q-input" id="edit-opt-${absIdx}-0" value="${escapeHtml(opts[0] || '')}">
                <input type="text" class="q-input" id="edit-opt-${absIdx}-1" value="${escapeHtml(opts[1] || '')}">
                <input type="text" class="q-input" id="edit-opt-${absIdx}-2" value="${escapeHtml(opts[2] || '')}">
                <input type="text" class="q-input" id="edit-opt-${absIdx}-3" value="${escapeHtml(opts[3] || '')}">

                <label>الإجابة الصحيحة (يجب أن تطابق أحد الخيارات حرفياً):</label>
                <input type="text" class="q-input" id="edit-ans-${absIdx}" value="${escapeHtml(qData.answer || '')}">

                <button class="btn" style="width:100%; margin-top:10px;" onclick="saveSingleQuestion(${absIdx})">
                    <i class="fas fa-save"></i> حفظ التعديل في الذاكرة
                </button>
            </div>
        `;
    });

    // Bottom pagination
    if (totalPages > 1) {
        html += `
            <div style="display:flex; justify-content:center; gap:8px; margin-top:20px; flex-wrap:wrap;">
                ${Array.from({length: Math.min(totalPages, 10)}, (_, i) => {
                    const pg = i + 1;
                    return `<button class="btn" style="padding:6px 12px; font-size:0.85rem; ${pg === currentPage ? 'background:var(--success);' : 'opacity:0.7;'}" onclick="goToPage(${pg})">${pg}</button>`;
                }).join('')}
                ${totalPages > 10 ? `<span style="color:#aaa; align-self:center;">... ${totalPages} صفحة</span>` : ''}
            </div>
        `;
    }

    container.innerHTML = html;
    container.scrollTop = 0;
}

function goToPage(page) {
    const totalPages = Math.ceil(filteredQuestions.length / PAGE_SIZE);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderResults();
    document.getElementById('results-container').scrollIntoView({ behavior: 'smooth' });
}

function saveSingleQuestion(absIdx) {
    const res = filteredQuestions[absIdx];

    const newQ = document.getElementById(`edit-q-${absIdx}`).value.trim();
    const newOpts = [
        document.getElementById(`edit-opt-${absIdx}-0`).value.trim(),
        document.getElementById(`edit-opt-${absIdx}-1`).value.trim(),
        document.getElementById(`edit-opt-${absIdx}-2`).value.trim(),
        document.getElementById(`edit-opt-${absIdx}-3`).value.trim()
    ];
    const newAns = document.getElementById(`edit-ans-${absIdx}`).value.trim();

    if (!newOpts.includes(newAns)) {
        alert("تنبيه: الإجابة الصحيحة غير موجودة في الخيارات الأربعة! يرجى التأكد من تطابق الحروف تماماً.");
        return;
    }

    db[res.poolKey][res.index].question = newQ;
    db[res.poolKey][res.index].options = newOpts;
    db[res.poolKey][res.index].answer = newAns;

    // Update the flat array too
    allQuestions.find(q => q.poolKey === res.poolKey && q.index === res.index).data = db[res.poolKey][res.index];

    localStorage.setItem('admin_pending_db', JSON.stringify(db));

    const btn = document.querySelector(`#card-${absIdx} .btn`);
    const originalText = btn.innerHTML;
    btn.innerHTML = `<i class="fas fa-check"></i> تم الحفظ في الذاكرة!`;
    btn.style.background = 'var(--success)';

    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.background = 'var(--gold)';
    }, 2000);
}

function downloadUpdatedDB() {
    const jsContent = `window.QUESTIONS_DATA = ${JSON.stringify(db)};`;
    const blob = new Blob([jsContent], {type: "text/javascript;charset=utf-8"});
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "questions_data.js";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    alert(`تم تحميل الملف!\n\nيرجى نسخ الملف المحمل (questions_data.js) ولصقه داخل مجلد (js) الخاص باللعبة والموافقة على الاستبدال (Replace) لتطبيق التعديلات نهائياً.`);
}

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

// Stats & Dashboard Logic
function updateDashboardStats() {
    db.ref('stats').on('value', (snapshot) => {
        const data = snapshot.val() || {};
        const visitors = data.visitors || 0;
        const players = data.players || 0;
        document.getElementById('total-visitors').innerText = Number(visitors).toLocaleString();
        document.getElementById('total-players').innerText = Number(players).toLocaleString();
    });
}

function resetStats() {
    if (confirm("تحذير: هل أنت متأكد من تصفير العدادات ولوحة الشرف؟ هذا الإجراء لا يمكن التراجع عنه!")) {
        db.ref('stats').set({ visitors: 0, players: 0 });
        db.ref('leaderboard').remove();
        alert('تم التصفير والحذف من قاعدة البيانات العالمية بنجاح!');
    }
}

function switchTab(tab) {
    const isQ = tab === 'questions';
    document.getElementById('section-questions').style.display = isQ ? 'block' : 'none';
    document.getElementById('section-messages').style.display = isQ ? 'none' : 'block';
    
    document.getElementById('tab-questions').style.background = isQ ? 'var(--gold)' : '#2c3e50';
    document.getElementById('tab-questions').style.color = isQ ? '#000' : '#fff';
    
    document.getElementById('tab-messages').style.background = isQ ? '#2c3e50' : 'var(--gold)';
    document.getElementById('tab-messages').style.color = isQ ? '#fff' : '#000';
    
    if (!isQ) renderMessages();
}

function renderMessages() {
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
}

function deleteMessage(key) {
    if(confirm("هل متأكد من حذف هذه الرسالة نهائياً؟")) {
        db.ref('feedback/' + key).remove();
    }
}

function clearAllMessages() {
    if (confirm("تحذير: هل أنت متأكد من حذف جميع الرسائل والمقترحات من السيرفر نهائياً؟")) {
        db.ref('feedback').remove();
    }
}
