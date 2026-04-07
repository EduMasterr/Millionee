import os
import shutil

brain_dir = r"C:\Users\A1\.gemini\antigravity\brain\3625bbc1-69e9-4c85-a51b-fbdca5d9f272"
dest_dir = r"c:\Users\A1\Desktop\Millione\assets\guide_images"
os.makedirs(dest_dir, exist_ok=True)

files = [
    ("uploaded_media_1775521140014.img", "1_add_app.webm"),
    ("uploaded_media_1775522181157.img", "2_register.webm"),
    ("uploaded_media_1775522374012.img", "3_config.webm"),
    ("uploaded_media_1775523127570.img", "4_db_1.webm"),
    ("uploaded_media_1775523618184.img", "5_db_2.webm"),
    ("uploaded_media_1775524545397.img", "6_rules.webm")
]

for src, dst in files:
    src_path = os.path.join(brain_dir, src)
    dst_path = os.path.join(dest_dir, dst)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>الدليل المصور الشامل لربط فايربيس</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1b2a; color: #e0e1dd; padding: 20px; line-height: 1.8; }
        .container { max-width: 900px; margin: auto; background: #1b263b; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.5); border-top: 5px solid #f1c40f; }
        h1 { color: #f1c40f; text-align: center; border-bottom: 2px solid #ffffff22; padding-bottom: 20px; font-weight: 900; }
        .step { background: rgba(0,0,0,0.3); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-right: 4px solid #f39c12; }
        .step h2 { color: #e74c3c; margin-top: 0; }
        video { max-width: 100%; height: auto; border: 2px solid #555; border-radius: 5px; margin-top: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); display: block; }
        .highlight { font-weight: bold; color: #2ecc71; }
        code { background: #000; padding: 2px 6px; border-radius: 4px; color: #f1c40f; direction: ltr; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 الدليل العملي المصور لإعداد Firebase</h1>
        <p style="text-align: center; font-size: 1.1rem; color: #aaa;">
            هذا الدليل تم بناؤه من الخطوات الحية التي قمت بها مع ترتيب الصور بصيغتها الأصلية<br>
            لتكون مرجعاً دائماً لك في المستقبل (تم الحفظ في مجلد assets/guide_images).
        </p>

        <div class="step">
            <h2>الخطوة 1: الشروع في تطبيق الويب</h2>
            <p>من الصفحة الرئيسية למشروعك <span class="highlight">Million-Journey</span>، اضغط على زر الزائد الصغير، ثم اختر أيقونة إنشاء تطبيق الويب <span class="highlight"><code>&lt;/&gt;</code></span>.</p>
            <video autoplay loop muted playsinline><source src="assets/guide_images/1_add_app.webm" type="video/webm"></video>
        </div>

        <div class="step">
            <h2>الخطوة 2: تسمية التطبيق وتسجيله</h2>
            <p>أدخل اسماً للتطبيق (مثل My Web App)، ثم اضغط على زر <strong>Register app</strong> لمتابعة الإعداد.</p>
            <video autoplay loop muted playsinline><source src="assets/guide_images/2_register.webm" type="video/webm"></video>
        </div>

        <div class="step">
            <h2>الخطوة 3: الحصول على أكواد الربط (Firebase Config)</h2>
            <p>هذا هو الملف السحري (firebaseConfig) الذي قمنا بتركيبه في كود اللعبة الخاصة بك.</p>
            <video autoplay loop muted playsinline><source src="assets/guide_images/3_config.webm" type="video/webm"></video>
        </div>

        <div class="step">
            <h2>الخطوة 4: التوجه إلى قاعدة البيانات</h2>
            <p>من القائمة الجانبية، ابحث عن <strong>Build</strong> ثم اختر <strong>Realtime Database</strong> لبناء قاعدة بيانات فورية للمقترحات ولوحة الشرف.</p>
            <video autoplay loop muted playsinline><source src="assets/guide_images/4_db_1.webm" type="video/webm"></video>
            <video autoplay loop muted playsinline><source src="assets/guide_images/5_db_2.webm" type="video/webm"></video>
        </div>

        <div class="step">
            <h2>الخطوة 5 والأخيرة: ضبط قواعد الأمان (Rules)</h2>
            <p>من التبويب <strong>Rules</strong>، يتم تحويل الحالات إلى <code>true</code>. يجب أن تكون كما بالشكل التالي (وبدون أي فواصل زائدة) ثم الضغط على <strong>Publish</strong>.</p>
            <video autoplay loop muted playsinline><source src="assets/guide_images/6_rules.webm" type="video/webm"></video>
        </div>

        <div style="text-align: center; padding-top: 30px;">
            <p style="color: #2ecc71; font-size: 1.5rem; font-weight: bold;">✅ تم الانتهاء بنجاح! نظامك متصل بالعالم الآن.</p>
        </div>
    </div>
</body>
</html>
"""

guide_path = r"c:\Users\A1\Desktop\Millione\firebase_guide.html"
with open(guide_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Guide compiled with WEBM media tags in assets/guide_images directory!")
