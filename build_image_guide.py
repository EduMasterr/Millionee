import os
import shutil

# 1. Setup folders
brain_dir = r"C:\Users\A1\.gemini\antigravity\brain\3625bbc1-69e9-4c85-a51b-fbdca5d9f272"
base_dir = r"c:\Users\A1\Desktop\Millione\Firebase_Setup_Guide"
media_dir = os.path.join(base_dir, "media")
os.makedirs(media_dir, exist_ok=True)

# 2. Map correct PNG artifacts
mapping = [
    ("media__1775524259339.png", "1_create_project.png"),
    ("media__1775524466893.png", "2_project_overview.png"),
    ("media__1775525094566.png", "3_firebase_config.png"),
    ("media__1775525762413.png", "4_realtime_database.png"),
    ("media__1775526798086.png", "5_security_rules.png")
]

# 3. Copy files
for src, dst in mapping:
    src_path = os.path.join(brain_dir, src)
    dst_path = os.path.join(media_dir, dst)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)

# 4. Remove any mistaken webm files
for f in os.listdir(media_dir):
    if f.endswith(".webm"):
        os.remove(os.path.join(media_dir, f))

# 5. Create final index.html with static images
html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دليل إعداد فايربيس - رحلة المليون</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1b2a; color: #e0e1dd; padding: 20px; line-height: 1.8; margin: 0; }
        .container { max-width: 950px; margin: auto; background: #1b263b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border-top: 6px solid #f1c40f; }
        h1 { color: #f1c40f; text-align: center; font-size: 2.2rem; margin-bottom: 30px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        .intro { text-align: center; color: #aaa; margin-bottom: 40px; font-size: 1.1rem; }
        .step { background: rgba(0,0,0,0.25); padding: 25px; margin-bottom: 40px; border-radius: 10px; border-right: 5px solid #2ecc71; box-shadow: inset 0 0 15px rgba(255,255,255,0.05); }
        .step h2 { color: #f39c12; margin-top: 0; font-size: 1.5rem; display: flex; align-items: center; gap: 10px; }
        .step p { margin: 15px 0; color: #eee; }
        .img-container { margin-top: 20px; border-radius: 8px; overflow: hidden; border: 2px solid #34495e; transition: transform 0.3s ease; }
        .img-container:hover { transform: scale(1.01); border-color: #f1c40f; }
        img { width: 100%; height: auto; display: block; }
        .highlight { font-weight: bold; color: #2ecc71; }
        code { background: #2c3e50; padding: 2px 8px; border-radius: 4px; color: #f1c40f; direction: ltr; display: inline-block; font-family: 'Courier New', Courier, monospace; }
        footer { text-align: center; margin-top: 50px; color: #777; font-size: 0.9rem; border-top: 1px solid #34495e; padding-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 الدليل العملي المصور لإعداد Firebase</h1>
        <p class="intro">هذا الملف يحتوي على الصور الفعلية لكل خطوة قمت بها، ليكون مرجعك الدائم في إرسال وتحميل البيانات عالمياً.</p>

        <div class="step">
            <h2>الخطوة 1: إنشاء المشروع</h2>
            <p>من لوحة تحكم Firebase، قمنا بإنشاء مشروع جديد باسم <span class="highlight">Million-Journey</span>.</p>
            <div class="img-container">
                <img src="media/1_create_project.png" alt="إنشاء المشروع">
            </div>
        </div>

        <div class="step">
            <h2>الخطوة 2: نظرة عامة على المشروع</h2>
            <p>بعد الدخول للمشروع، ستظهر لك هذه الشاشة. نضغط هنا على أيقونة الويب <span class="highlight"><code>&lt;/&gt;</code></span> للبدء في ربط اللعبة.</p>
            <div class="img-container">
                <img src="media/2_project_overview.png" alt="نظرة عامة">
            </div>
        </div>

        <div class="step">
            <h2>الخطوة 3: الحصول على أكواد الاتصال</h2>
            <p>هذا هو أهم جزء، حيث يظهر كود <span class="highlight">firebaseConfig</span> الذي يحتوي على مفاتيح البرمجة. هذا الكود هو ما وضعناه داخل ملفات اللعبة ليتواصل مع السيرفر.</p>
            <div class="img-container">
                <img src="media/3_firebase_config.png" alt="كود الدخول">
            </div>
        </div>

        <div class="step">
            <h2>الخطوة 4: إنشاء قاعدة البيانات (Realtime DB)</h2>
            <p>من القائمة الجانبية اخترنا <span class="highlight">Realtime Database</span> ثم ضغطنا على إنشاء لتبدأ في تخزين نتائج اللاعبين والمقترحات فورياً.</p>
            <div class="img-container">
                <img src="media/4_realtime_database.png" alt="قاعدة البيانات">
            </div>
        </div>

        <div class="step">
            <h2>الخطوة 5: ضبط صلاحيات الدخول (Rules)</h2>
            <p>هذه هي النتيجة النهائية الصحيحة، حيث قمنا بجعل <code>read</code> و <code>write</code> تساوي <code>true</code> للسماح للعبة بإرسال البيانات واستقبالها بنجاح.</p>
            <div class="img-container">
                <img src="media/5_security_rules.png" alt="قواعد الأمان">
            </div>
        </div>

        <footer>
            ✅ تم إنجاز الربط السحابي بنجاح! اللعبة الآن متصلة عالمياً.
        </footer>
    </div>
</body>
</html>
"""

with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Images guide created successfully with correct static PNGs.")
