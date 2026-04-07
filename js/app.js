const PRIZE_LADDER = [
    0,
    100, 200, 300, 500, 1000, // 5 is checkpoint
    2000, 4000, 8000, 16000, 32000, // 10 is checkpoint
    64000, 125000, 250000, 500000, 1000000 // 15 is WIN
];

const SECONDS_PER_QUESTION = 30;

let currentLevel = 1;
let currentQuestion = null;
let timer = null;
let timeLeft = SECONDS_PER_QUESTION;
let isTimeFrozen = false;
let lifeVestActive = false;

let playerName = "";
let playerAge = "";

const USED_QUESTIONS_KEY = 'million_journey_used_ids';
const LEADERBOARD_KEY = 'million_journey_leaderboard';
let usedQuestions = JSON.parse(localStorage.getItem(USED_QUESTIONS_KEY)) || [];
let isAdmin = false;

// Questions pool populated from files
const questionsPool = {
    1: [], // Very Easy (from 1.txt)
    2: [], // Easy (from 2.txt)
    3: [], // Normal (from 3.txt)
    4: [], // Hard (from 4.txt)
    5: []  // Legend (from 5.txt)
};


// Cheat Button Check
document.getElementById("admin-cheat-btn").onclick = function() {
    if (!isAdmin || !currentQuestion) return;
    const icon = this.querySelector("i");
    if (icon.classList.contains("fa-eye-slash")) {
        icon.className = "fas fa-eye glow-text gold";
        this.style.color = "var(--gold)";
        document.querySelectorAll(".option-btn").forEach(btn => {
            const btnText = btn.querySelector(".option-text").innerText.trim();
            const correctAns = currentQuestion.answer.trim();
            
            // Log to console for debugging if it still fails
            console.log(`Checking match: "${btnText}" VS "${correctAns}"`);

            if (btnText === correctAns || btnText.includes(correctAns) || correctAns.includes(btnText)) {
                btn.style.border = "3px solid var(--gold)";
                btn.style.boxShadow = "0 0 25px var(--gold)";
            }
        });
    } else {
        icon.className = "fas fa-eye-slash";
        this.style.color = "var(--danger)";
        document.querySelectorAll(".option-btn").forEach(btn => {
            btn.style.border = "";
            btn.style.boxShadow = "";
        });
    }
};
const dom = {
    startScreen: document.getElementById('start-screen'),
    gameScreen: document.getElementById('game-screen'),
    overlayScreen: document.getElementById('overlay-screen'),
    startBtn: document.getElementById('start-btn'),
    leaderboardBtn: document.getElementById('leaderboard-btn'),
    closeLeaderboardBtn: document.getElementById('close-leaderboard-btn'),
    loader: document.getElementById('loading-indicator'),
    
    leaderboardModal: document.getElementById('leaderboard-modal'),
    leaderboardList: document.getElementById('leaderboard-list'),
    
    qNumber: document.getElementById('question-number'),
    prizeAmount: document.getElementById('current-prize'),
    timeLeft: document.getElementById('time-left'),
    timerContainer: document.getElementById('timer-container'),
    
    questionText: document.getElementById('question-text'),
    options: [
        document.getElementById('opt-0'),
        document.getElementById('opt-1'),
        document.getElementById('opt-2'),
        document.getElementById('opt-3')
    ],
    optionBtns: document.querySelectorAll('.option-btn'),
    
    overlayTitle: document.getElementById('overlay-title'),
    overlayMessage: document.getElementById('overlay-message'),
    overlayActionBtn: document.getElementById('overlay-action-btn'),
    
    suspenseModal: document.getElementById('suspense-modal'),
    confirmAnswerBtn: document.getElementById('confirm-answer-btn'),
    cancelAnswerBtn: document.getElementById('cancel-answer-btn'),
    
    lifelines: {
        lifeVest: document.getElementById('life-vest-btn'),
        pathSwap: document.getElementById('path-swap-btn'),
        timeFreeze: document.getElementById('time-freeze-btn'),
        returnTicket: document.getElementById('return-ticket-btn')
    }
};

window.onload = async () => {
    // Permanent cleanup of admin entries
    let lb = JSON.parse(localStorage.getItem('million_leaderboard') || '[]');
    let filteredLb = lb.filter(item => item.name.trim().toLowerCase() !== 'admin');
    if (lb.length !== filteredLb.length) {
        localStorage.setItem('million_leaderboard', JSON.stringify(filteredLb));
    }
    dom.startBtn.style.display = 'none';
    dom.loader.style.display = 'block';
    
    // Increment Visitors & Players via Firebase Transactions
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
    });

    // Make stats clickable
    const visitorsStat = document.getElementById('home-visitors').closest('.hero-stat');
    if (visitorsStat) {
        visitorsStat.onclick = () => {
            if (typeof showLeaderboard === 'function') showLeaderboard();
            else if (dom.leaderboardBtn) dom.leaderboardBtn.click();
        };
    }
    const playersStat = document.getElementById('home-players').closest('.hero-stat');
    // Also hook up the plus button
    const plusBtn = document.getElementById('plus-leaderboard-btn');
    if (plusBtn) {
        plusBtn.onclick = (e) => {
            e.stopPropagation(); // Don't trigger the parent stat click twice
            if (typeof showLeaderboard === 'function') showLeaderboard();
            else if (dom.leaderboardBtn) dom.leaderboardBtn.click();
        };
    }

    if (playersStat) {
        playersStat.style.cursor = 'pointer';
        playersStat.title = 'عرض لوحة الشرف';
        playersStat.onclick = () => {
            if (typeof showLeaderboard === 'function') showLeaderboard();
            else if (dom.leaderboardBtn) dom.leaderboardBtn.click();
        };
    }

    // تم تعطيل التكميل التلقائي بناءً على طلبك
    // Immediate clear on uncheck
    document.getElementById('remember-me').addEventListener('change', function() {
        if (!this.checked) {
            localStorage.removeItem('million_player_name');
            localStorage.removeItem('million_player_age');
        }
    });

    const savedName = localStorage.getItem('million_player_name');
    const savedAge = localStorage.getItem('million_player_age');
    if (savedName) {
    document.getElementById('player-name').value = savedName;
    document.getElementById('remember-me').checked = true;
    }
    if (savedAge) document.getElementById('player-age').value = savedAge;

    try {
        await loadQuestions();
        dom.loader.style.display = 'none';
        dom.startBtn.style.display = 'inline-block';
    } catch (e) {
        dom.loader.innerHTML = `حدث خطأ في تحميل الأسئلة. الرجاء التأكد من تشغيل الخادم المحلي. <br><small>${e.message}</small>`;
    }
};

async function loadQuestions() {
    // Populate from the injected JS object
    if (!window.QUESTIONS_DATA) {
        throw new Error("لم يتم العثور على الأسئلة في ملف البيانات.");
    }
    
    for (let i = 1; i <= 5; i++) {
        let parsed = window.QUESTIONS_DATA[i] || [];
        
        // If this level is empty, borrow from the nearest available level
        if (parsed.length === 0) {
            const fallbackOrder = [i-1, i+1, i-2, i+2, 2, 4].filter(n => n >= 1 && n <= 5);
            for (const fallback of fallbackOrder) {
                if (window.QUESTIONS_DATA[fallback] && window.QUESTIONS_DATA[fallback].length > 0) {
                    parsed = window.QUESTIONS_DATA[fallback];
                    console.log(`Level ${i} is empty. Using level ${fallback} as fallback.`);
                    break;
                }
            }
        }
        
        // Filter out used questions to guarantee no repetition across sessions
        let available = parsed.filter(q => !usedQuestions.includes(q.id));
        
        // If all questions in this level are exhausted, borrow from adjacent levels (NEVER reset history)
        if (available.length === 0 && parsed.length > 0) {
            console.log(`Level ${i} questions exhausted. Borrowing from adjacent levels...`);
            const borrowOrder = [i-1, i+1, i-2, i+2].filter(n => n >= 1 && n <= 5 && n !== i);
            for (const bLevel of borrowOrder) {
                const bParsed = window.QUESTIONS_DATA[bLevel] || [];
                const bAvailable = bParsed.filter(q => !usedQuestions.includes(q.id));
                if (bAvailable.length > 0) {
                    available = bAvailable;
                    console.log(`Borrowed ${bAvailable.length} questions from level ${bLevel}`);
                    break;
                }
            }
        }
        
        // Fisher-Yates Shuffle for true randomness without perceived clusters
        for (let j = available.length - 1; j > 0; j--) {
            const k = Math.floor(Math.random() * (j + 1));
            [available[j], available[k]] = [available[k], available[j]];
        }
        
        questionsPool[i] = available;
    }
}

// ---- Leaderboard Handlers ----
dom.leaderboardBtn.addEventListener('click', showLeaderboard);
dom.closeLeaderboardBtn.addEventListener('click', () => {
    dom.leaderboardModal.classList.remove('active');
    dom.startScreen.classList.add('active');
});

function saveToLeaderboard(name, age, score) {
    db.ref('leaderboard').push({
        name: name,
        age: age,
        score: Number(score),
        date: new Date().toISOString()
    });
}

function showLeaderboard() {
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
}

// ----------------

dom.startBtn.addEventListener('click', startGame);

function startGame() {
    playerName = document.getElementById('player-name').value.trim();
    playerAge = document.getElementById('player-age').value.trim();
    
    if (!playerName || !playerAge) {
        showCustomAlert("يا بطل، لازم تكتب اسمك وسنك عشان نسجلك في لوحة الشرف!", "fa-exclamation-triangle");
        return;
    }
    
    if (playerName === "admin" && playerAge === "135") {
        isAdmin = true;
        let cheatBtn = document.getElementById("admin-cheat-btn");
        if (cheatBtn) cheatBtn.style.display = "inline-block";
    }

    // حفظ البيانات للمرة القادمة إذا طلب اللاعب
    const rememberMe = document.getElementById('remember-me').checked;
    if (rememberMe) {
        localStorage.setItem('million_player_name', playerName);
        localStorage.setItem('million_player_age', playerAge);
    } else {
        localStorage.removeItem('million_player_name');
        localStorage.removeItem('million_player_age');
    }

    // Increment Total Players Globally
    db.ref('stats/players').transaction((current) => {
        return (current || 0) + 1;
    });

    currentLevel = 1;
    dom.startScreen.classList.remove('active');
    dom.gameScreen.classList.add('active');
    dom.gameScreen.style.opacity = 1;
    dom.gameScreen.style.pointerEvents = 'all';
    
    // Reset lifelines
    Object.values(dom.lifelines).forEach(btn => {
        btn.classList.remove('used');
        btn.disabled = false;
    });
    
    loadNextQuestion();
}

function showScreen(screen) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    screen.classList.add('active');
}

function getPoolLevel(level) {
    if (level <= 3) return 1;
    if (level <= 6) return 2;
    if (level <= 10) return 3;
    if (level <= 13) return 4;
    return 5;
}

function getRandomQuestion(poolLevel) {
    const pool = questionsPool[poolLevel];
    if (!pool || pool.length === 0) {
        return {
            id: 'fallback-' + Date.now(),
            question: "سؤال احتياطي: ما هو الكوكب الذي نعيش عليه؟",
            options: ["المريخ", "الأرض", "عطارد", "زحل"],
            answer: "الأرض"
        };
    }
    // We already shuffled the pool during loadQuestions! So we just pop the last one.
    // This is mathematically the most robust way to prevent perceived repetition clusters.
    const q = pool.pop();
    return q;
}

function loadNextQuestion(poolOverride = null) {
    lifeVestActive = false;
    let pLevel = poolOverride ? poolOverride : getPoolLevel(currentLevel);
    currentQuestion = getRandomQuestion(pLevel);
    
    // Save to used questions
    if (currentQuestion && currentQuestion.id) {
        usedQuestions.push(currentQuestion.id);
        localStorage.setItem(USED_QUESTIONS_KEY, JSON.stringify(usedQuestions));
    }
    
    dom.qNumber.innerText = currentLevel;
    dom.prizeAmount.innerText = PRIZE_LADDER[currentLevel - 1].toLocaleString();
    
    dom.questionText.innerText = currentQuestion.question;
    playSound('appear');
    
    // Shuffle options
    let options = [...currentQuestion.options];
    options.sort(() => Math.random() - 0.5);
    
    // Save mapped answer checking logic
    currentQuestion.shuffledOptions = options;
    
    dom.optionBtns.forEach((btn, index) => {
        btn.classList.remove('selected', 'correct', 'wrong');
        btn.style.opacity = '1';
        btn.disabled = false;
        
        let textNode = btn.querySelector('.option-text');
        if(!textNode) {
            textNode = document.createElement('span');
            textNode.className = 'option-text';
            btn.appendChild(textNode);
        }
        textNode.innerText = options[index];
        btn.onclick = () => handleAnswer(btn, options[index]);
    });
    
    startTimer();
}

function startTimer() {
    clearInterval(timer);
    timeLeft = SECONDS_PER_QUESTION;
    isTimeFrozen = false;
    dom.timerContainer.classList.remove('freeze-anim');
    updateTimerDisplay();
    
    timer = setInterval(() => {
        if (isTimeFrozen) return;
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 0) {
            clearInterval(timer);
            loseGame('انتهى الوقت!');
        }
    }, 1000);
}

function updateTimerDisplay() {
    dom.timeLeft.innerText = timeLeft;
    if(timeLeft <= 5) {
        dom.timerContainer.style.borderColor = 'red';
        dom.timerContainer.style.color = 'red';
    } else {
        dom.timerContainer.style.borderColor = '#D4AF37';
        dom.timerContainer.style.color = '#D4AF37';
    }
}

function handleAnswer(btn, selectedOption) {
    if(isTimeFrozen) {
        isTimeFrozen = false;
        dom.timerContainer.classList.remove('freeze-anim');
    }
    
    clearInterval(timer);
    
    dom.optionBtns.forEach(b => b.disabled = true);
        btn.classList.add('selected');
        const processAnswer = () => {
            setTimeout(() => {
                const isCorrect = (selectedOption === currentQuestion.answer);
                btn.classList.remove('selected');
                
                if (isCorrect) {
                    btn.classList.add('correct');
                    playSound('correct');
                    setTimeout(() => advanceLevel(), 2000);
                } else {
                    btn.classList.add('wrong');
                    // Show correct answer
                    dom.optionBtns.forEach(b => {
                        if (b.querySelector('.option-text').innerText === currentQuestion.answer) {
                            b.classList.add('correct');
                        }
                    });
                    
                    if (lifeVestActive) {
                        setTimeout(async () => {
                            await showCustomAlert("سترة النجاة شغالة! العناية الإلهية أنقذتك.. ليك فرصة ثانية عشان تجاوب الصح.", "fa-life-ring");
                            lifeVestActive = false;
                            btn.classList.remove('wrong');
                            btn.style.opacity = '0';
                            dom.optionBtns.forEach(b => {
                                if (!b.classList.contains('wrong') && b.style.opacity !== '0') {
                                    b.disabled = false;
                                }
                                b.classList.remove('correct');
                            });
                            startTimer();
                        }, 2000);
                    } else {
                        playSound('wrong');
                        setTimeout(() => loseGame('للأسف إجابة خاطئة!'), 2000);
                    }
                }
            }, 3000); // Suspense
        };

        if (currentLevel >= 10) {
            dom.suspenseModal.classList.add('active');
            
            dom.confirmAnswerBtn.onclick = () => {
                dom.suspenseModal.classList.remove('active');
                processAnswer();
            };
            
            dom.cancelAnswerBtn.onclick = () => {
                dom.suspenseModal.classList.remove('active');
                btn.classList.remove('selected');
                dom.optionBtns.forEach(b => b.disabled = false);
                startTimer();
            };
        } else {
            processAnswer();
        }
}

function advanceLevel() {
    if (currentLevel === 15) {
        winGame();
    } else {
        currentLevel++;
        loadNextQuestion();
    }
}

function getSafeHavenAmount() {
    if (currentLevel > 10) return PRIZE_LADDER[10];
    if (currentLevel > 5) return PRIZE_LADDER[5];
    return 0;
}

function loseGame(reason) {
    const safeAmount = getSafeHavenAmount();
    saveToLeaderboard(playerName, playerAge, safeAmount);
    
    playSound('lose');
    
    dom.overlayTitle.innerText = "انتهت الرحلة! 🛑";
    dom.overlayTitle.style.color = "var(--gold)";
    dom.overlayMessage.innerHTML = `<span style="font-size: 1.5rem; color: #ccc;">${reason}</span><br><br>رصيدك النهائي الذي حصلت عليه هو:<br><strong class="gold" style="font-size: 3.5rem;">${safeAmount.toLocaleString()}</strong> <i class="fas fa-coins"></i>`;
    
    dom.overlayActionBtn.innerText = "العودة للبداية";
    dom.overlayActionBtn.onclick = () => window.location.reload();
    dom.overlayActionBtn.classList.add('pulse');
    
    showScreen(dom.overlayScreen);
}

function winGame() {
    saveToLeaderboard(playerName, playerAge, 1000000);
    
    dom.overlayTitle.innerHTML = "🏆 أسطوووووورة! إنت المليونير! 🎉";
    dom.overlayTitle.style.color = "var(--gold)";
    dom.overlayTitle.style.fontSize = "4rem";
    dom.overlayTitle.classList.add('glow-text');
    
    dom.overlayMessage.innerHTML = `<div style='font-size: 2rem; line-height: 1.8;'>بسم الله ما شاء الله يا بطل ${playerName} (${playerAge} سنة)، إنت كسرت الدنيا! 💥<br> 15 سؤال عدتهم بصعوبتهم، بضغطهم، بتوترهم.. وحققت الحلم!<br><strong class='gold' style='font-size: 3rem;'>المليـــــــــون معاك في جيبك! 💰💎</strong></div>`;
    
    dom.overlayActionBtn.innerText = "العب مرة أخرى عشان الملايين الجاية";
    dom.overlayActionBtn.onclick = () => window.location.reload();
    
    showScreen(dom.overlayScreen);
}

// ---- Custom UI Utils ----
function showCustomAlert(message, iconClass = "fa-info-circle") {
    return new Promise((resolve) => {
        const alertModal = document.getElementById('custom-alert');
        document.getElementById('custom-alert-message').innerText = message;
        document.getElementById('custom-alert-icon').className = `fas ${iconClass} glow-text gold`;
        alertModal.classList.add('active');
        
        playSound('appear');
        
        document.getElementById('custom-alert-btn').onclick = () => {
            alertModal.classList.remove('active');
            resolve();
        };
    });
}

// ---- Lifelines Handlers ----
dom.lifelines.lifeVest.onclick = async function() {
    this.classList.add('used');
    this.disabled = true;
    lifeVestActive = true;
    
    const wasFrozen = isTimeFrozen;
    isTimeFrozen = true;
    await showCustomAlert("تم تفعيل سترة النجاة! يمكنك الإجابة الآن بفرصتين.. العب بثقة واختار الإجابة بحذر.", "fa-shield-alt");
    isTimeFrozen = wasFrozen;
};

dom.lifelines.pathSwap.onclick = async function() {
    this.classList.add('used');
    this.disabled = true;
    
    const wasFrozen = isTimeFrozen;
    isTimeFrozen = true;
    await showCustomAlert("تم تبديل المسار بنجاح! جايلك سؤال جديد من نفس المستوى.. ركز!", "fa-exchange-alt");
    isTimeFrozen = wasFrozen;
    
    loadNextQuestion(); // reload same level
};

dom.lifelines.timeFreeze.onclick = async function() {
    this.classList.add('used');
    this.disabled = true;
    isTimeFrozen = true;
    dom.timerContainer.classList.add('freeze-anim');
    await showCustomAlert("تم تجميد الوقت! ❄️ خد وقتك وفكر براحتك بدون أي ضغط.", "fa-snowflake");
};

dom.lifelines.returnTicket.onclick = async function() {
    this.classList.add('used');
    this.disabled = true;
    
    const wasFrozen = isTimeFrozen;
    isTimeFrozen = true;
    await showCustomAlert("تذكرة العودة اشتغلت! 🎫 رجعناك لسؤال من المستوى الأول عشان تضمن النقطة دي.", "fa-ticket-alt");
    isTimeFrozen = wasFrozen;
    
    loadNextQuestion(1); // Force Level 1 pool
};

// ---- Sound Engine (Web Audio API) ----
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx;

function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();
}

function playSound(type) {
    try {
        initAudio();
        if (type === 'correct') {
            // Success Chime (Bright Major Chord)
            playTone(523.25, 'sine', 0, 0.4); // C5
            playTone(659.25, 'sine', 0, 0.4); // E5
            playTone(783.99, 'sine', 0, 0.4); // G5
            playTone(1046.50, 'sine', 0.1, 0.6); // C6
        } else if (type === 'wrong') {
            // Error Buzzer (Low dissonance dropping pitch)
            playTone(300, 'sawtooth', 0, 0.5, 100); 
            playTone(250, 'sawtooth', 0.1, 0.5, 50);
        } else if (type === 'lose') {
            // Sad losing sound (Descending minor notes)
            playTone(440, 'triangle', 0, 0.4); // A4
            playTone(349.23, 'triangle', 0.4, 0.4); // F4
            playTone(261.63, 'triangle', 0.8, 0.8, 100); // C4
        } else if (type === 'appear') {
            // Question Appear (Sci-fi scanning sound)
            playTone(800, 'sine', 0, 0.1);
            playTone(1200, 'sine', 0.05, 0.1);
            playTone(1600, 'sine', 0.1, 0.2);
        }
    } catch(e) { console.log('Audio not supported or blocked'); }
}

function playTone(freq, type, delay, duration, endFreq=null) {
    if(!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    
    const startTime = audioCtx.currentTime + delay;
    osc.frequency.setValueAtTime(freq, startTime);
    if(endFreq) {
        osc.frequency.exponentialRampToValueAtTime(endFreq, startTime + duration);
    }
    
    gain.gain.setValueAtTime(0, startTime);
    gain.gain.linearRampToValueAtTime(0.2, startTime + 0.05);
    gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start(startTime);
    osc.stop(startTime + duration);
}


// Global Keyboard Navigation (Enter/Escape)
document.addEventListener("keydown", (e) => {
    // Custom Alert
    const alertModal = document.getElementById("custom-alert");
    if (alertModal && alertModal.classList.contains("active")) {
        if (e.key === "Enter" || e.key === "Escape") {
            document.getElementById("custom-alert-btn").click();
            e.preventDefault();
        }
        return;
    }
    
    // Suspense Modal
    const suspenseModal = document.getElementById("suspense-modal");
    if (suspenseModal && suspenseModal.classList.contains("active")) {
        if (e.key === "Enter") {
            document.getElementById("confirm-answer-btn").click();
            e.preventDefault();
        } else if (e.key === "Escape") {
            document.getElementById("cancel-answer-btn").click();
            e.preventDefault();
        }
        return;
    }

    // Leaderboard
    const lbModal = document.getElementById("leaderboard-modal");
    if (lbModal && lbModal.classList.contains("active")) {
        if (e.key === "Escape" || e.key === "Enter") {
            document.getElementById("close-leaderboard-btn").click();
            e.preventDefault();
        }
        return;
    }

    // Overlay (Win/Loss)
    const overlayScreen = document.getElementById("overlay-screen");
    if (overlayScreen && overlayScreen.classList.contains("active")) {
        if (e.key === "Enter" || e.key === "Escape") {
            document.getElementById("overlay-action-btn").click();
            e.preventDefault();
        }
        return;
    }

    // Start Screen
    const startScreen = document.getElementById("start-screen");
    if (startScreen && startScreen.classList.contains("active")) {
        if (e.key === "Enter") {
            document.getElementById("start-btn").click();
            e.preventDefault();
        }
        return;
    }
});

// ---- Feedback Logic ----
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
});
