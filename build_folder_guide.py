import os
import shutil

# 1. Setup new dedicated folder
brain_dir = r'C:\Users\A1\.gemini\antigravity\brain\3625bbc1-69e9-4c85-a51b-fbdca5d9f272'
base_dir = r'c:\Users\A1\Desktop\Millione\Firebase_Setup_Guide'
media_dir = os.path.join(base_dir, 'media')
os.makedirs(media_dir, exist_ok=True)

# 2. Files
files = [
    ('uploaded_media_1775521140014.img', '1_add_app.webm'),
    ('uploaded_media_1775522181157.img', '2_register.webm'),
    ('uploaded_media_1775522374012.img', '3_config.webm'),
    ('uploaded_media_1775523127570.img', '4_db_1.webm'),
    ('uploaded_media_1775523618184.img', '5_db_2.webm'),
    ('uploaded_media_1775524545397.img', '6_rules.webm')
]

for src, dst in files:
    src_path = os.path.join(brain_dir, src)
    dst_webm = os.path.join(media_dir, dst)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_webm)

# 3. HTML Content
html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دليل فايربيس - رحلة المليون</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1b2a; color: #e0e1dd; padding: 20px; line-height: 1.8; margin: 0; }
        .container { max-width: 900px; margin: auto; background: #1b263b; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.5); border-top: 5px solid #f1c40f; }
        h1 { color: #f1c40f; text-align: center; border-bottom: 2px solid #ffffff22; padding-bottom: 20px; }
        .step { background: rgba(0,0,0,0.3); padding: 20px; margin-bottom: 30px; border-radius: 8px; border-right: 4px solid #f39c12; }
        .step h2 { color: #e74c3c; margin-top: 0; }
        .media-container { margin-top: 15px; text-align: center; background: #000; border-radius: 8px; overflow: hidden; border: 2px solid #f1c40f55; }
        video { max-width: 100%; height: auto; display: block; margin: auto; }
        .highlight { font-weight: bold; color: #2ecc71; }
        code { background: #000; padding: 2px 6px; border-radius: 4px; color: #f1c40f; direction: ltr; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 الدليل العملي المصور لإعداد Firebase</h1>
        <p style="text-align: center; font-size: 1.1rem; color: #aaa;">تم تجهيز هذا الدليل كمرجع مستقل لك، مع حفظ مقاطع الفيديو التوضيحية داخل مجلد <strong>media</strong>.</p>

        <div class="step">
            <h2>الخطوة 1: الشروع في تطبيق الويب</h2>
            <p>من الصفحة الرئيسية למشروعك <span class="highlight">Million-Journey</span>، اضغط على أيقونة الويب <span class="highlight"><code>&lt;/&gt;</code></span>.</p>
            <div class="media-container"><video src="media/1_add_app.webm" autoplay loop muted playsinline controls></video></div>
        </div>

        <div class="step">
            <h2>الخطوة 2: تسمية التطبيق وتسجيله</h2>
            <p>أدخل اسماً للتطبيق (مثل My Web App)، ثم اضغط على زر <strong>Register app</strong>.</p>
            <div class="media-container"><video src="media/2_register.webm" autoplay loop muted playsinline controls></video></div>
        </div>

        <div class="step">
            <h2>الخطوة 3: الحصول على أكواد الربط (Firebase Config)</h2>
            <p>هذا كود (firebaseConfig) الذي قمنا بتركيبه في كود اللعبة الخاصة بك.</p>
            <div class="media-container"><video src="media/3_config.webm" autoplay loop muted playsinline controls></video></div>
        </div>

        <div class="step">
            <h2>الخطوة 4: التوجه إلى قاعدة البيانات</h2>
            <p>اختر <strong>Realtime Database</strong> لبناء قاعدة بيانات فورية للمقترحات ولوحة الشرف.</p>
            <div class="media-container"><video src="media/4_db_1.webm" autoplay loop muted playsinline controls></video></div>
            <div class="media-container"><video src="media/5_db_2.webm" autoplay loop muted playsinline controls></video></div>
        </div>

        <div class="step">
            <h2>الخطوة 5 والأخيرة: ضبط قواعد الأمان (Rules)</h2>
            <p>من التبويب <strong>Rules</strong>، يتم تحويل الحالات إلى <code>true</code> ومسح أي فواصل زائدة وتأكيد النشر.</p>
            <div class="media-container"><video src="media/6_rules.webm" autoplay loop muted playsinline controls></video></div>
        </div>

        <div style="text-align: center; padding-top: 30px;">
            <p style="color: #2ecc71; font-size: 1.5rem; font-weight: bold;">✅ تم الانتهاء بنجاح! مجلد الدليل المتكامل جاهز تماماً.</p>
        </div>
    </div>
</body>
</html>
"""

with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

# Clean up old single file guide
old_guide = r'c:\Users\A1\Desktop\Millione\firebase_guide.html'
if os.path.exists(old_guide):
    os.remove(old_guide)

print('Folder structured successfully! Old file removed.')
