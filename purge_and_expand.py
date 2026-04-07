import json

print("Loading Database and searching for any trace of Math...")
with open('js/questions_data.js', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('{')
end = text.rfind(';')
db = json.loads(text[start:end])

cleaned_db = {"1":[], "2":[], "3":[], "4":[], "5":[]}
math_purged = 0

# Aggressive Math words
math_keywords = ['احسب', 'ناتج', 'يساوي', '+', '-', '×', '÷', 'ضرب', 'طرح', 'جمع', 'قسمة', 'معادلة', 'مسألة', 'رياضية', 'رياضي']

for level, qs in db.items():
    for q in qs:
        q_text = str(q.get('question', '')).strip()
        
        # Check if it has any math keyword
        is_math = False
        for kw in math_keywords:
            if kw in q_text:
                is_math = True
                break
                
        # Also kill logical additions about words that use arithmetic
        if "رقم" in q_text and "+" in q_text: is_math = True

        if is_math:
            math_purged += 1
            continue
            
        cleaned_db[level].append(q)

print(f"Purged {math_purged} remaining Math questions!")

print('\n=== COUNTS BEFORE ADDING NEW TRIVIA ===')
total = 0
for k, v in cleaned_db.items():
    print(f'Level {k}: {len(v)}')
    total += len(v)
print(f'Total: {total}')

import random
idx = 200000
def add(level, q, ans, pool):
    global idx
    candidates = [x for x in pool if x != ans]
    if len(candidates) < 3: return
    dists = random.sample(candidates, 3)
    opts = dists + [ans]
    random.shuffle(opts)
    cleaned_db[str(level)].append({'id': f'cultv2_{idx}', 'question': q, 'options': opts, 'answer': str(ans)})
    idx += 1

# MASSIVE CULTURAL/GENERAL INFO GENERATOR

# World Currencies (100+)
currencies = [
    ('الجزائر','الدينار الجزائري'),('البحرين','الدينار البحريني'),('مصر','الجنيه المصري'),('العراق','الدينار العراقي'),
    ('الأردن','الدينار الأردني'),('الكويت','الدينار الكويتي'),('لبنان','الليرة اللبنانية'),('ليبيا','الدينار الليبي'),
    ('المغرب','الدرهم المغربي'),('عمان','الريال العماني'),('فلسطين','الشيكل/الدينار'),('قطر','الريال القطري'),
    ('السعودية','الريال السعودي'),('سوريا','الليرة السورية'),('تونس','الدينار التونسي'),('الإمارات','الدرهم الإماراتي'),
    ('اليمن','الريال اليمني'),('أمريكا','الدولار الأمريكي'),('بريطانيا','الجنيه الإسترليني'),('اليابان','الين الياباني'),
    ('الصين','اليوان الصيني'),('الهند','الروبية الهندية'),('روسيا','الروبل الروسي'),('تركيا','الليرة التركية'),
    ('كوريا الجنوبية','الوون الكوري'),('البرازيل','الريال البرازيلي'),('الأرجنتين','البيزو الأرجنتيني')
]
all_curr = [c[1] for c in currencies]
for c in currencies:
    add(2, f'ما هي العملة الرسمية لدولة {c[0]}؟', c[1], all_curr)
    add(3, f'تستخدم عملة "{c[1]}" كعملة رسمية في دولة:', c[0], [x[0] for x in currencies])

# Geography Seas/Oceans
water = [('البحر الأحمر','بين آسيا وأفريقيا'),('البحر المتوسط','شمال أفريقيا وجنوب أوروبا'),('بحر قزوين','أكبر بحيرة مغلقة'),
         ('البحر الميت','أخفض بقعة على الأرض'),('المحيط الهندي','جنوب آسيا')]
water_names = [w[0] for w in water]
for w in water:
    add(3, f'أي مسطح مائي يوصف بأنه ({w[1]})؟', w[0], water_names)

# Inventions Additions
inv2 = [('التلغراف','صامويل مورس'),('المطبعة','يوهان غوتنبرغ'),('البطارية','أليساندرو فولتا'),('المحول الكهربائي','مايكل فاراداي'),('البنسلين','ألكسندر فليمنغ'),('السماعة الطبية','رينيه لينيك'),('الديناميت','ألفريد نوبل')]
for i in inv2:
    add(4, f'من هو مخترع {i[0]}؟', i[1], [x[1] for x in inv2] + ['أينشتاين','نيوتن','أديسون'])

# Animal gestation (weird facts for level 5)
gestation = [('الفيل','22 شهراً'),('الحوت الأزرق','11 شهراً'),('الزرافة','15 شهراً'),('الجمل','13 شهراً'),('القط','شهران')]
gestation_times = [g[1] for g in gestation] + ['5 أشهر','9 أشهر','40 يوماً']
for g in gestation:
    add(5, f'كم تبلغ فترة الحمل تقريباً لدى إناث {g[0]}؟', g[1], gestation_times)

# Historical Nicknames
nicknames = [('سيف الله المسلول','خالد بن الوليد'),('الفاروق','عمر بن الخطاب'),('ذو النورين','عثمان بن عفان'),('الصديق','أبو بكر'),('حبر الأمة','عبد الله بن عباس'),('أسد الله','حمزة بن عبد المطلب'),('أمين الأمة','أبو عبيدة بن الجراح')]
nicks_pool = [n[1] for n in nicknames]
for n in nicknames:
    add(2, f'من هو الصحابي الجليل الملقب بـ ({n[0]})؟', n[1], nicks_pool)

# Fill to ensure every level hits ~1000 minimum without ANY math
tech_companies = [('أبل','تيم كوك'),('غوغل','سوندار بيتشاي'),('مايكروسوفت','ساتيا ناديلا'),('فيسبوك/ميتا','مارك زوكربيرغ')]
for t in tech_companies:
    add(4, f'من هو المدير التنفيذي (CEO) الأشهر لشركة {t[0]} وممثلها؟', t[1], [x[1] for x in tech_companies] + ['بيل غيتس','إيلون ماسك'])

print('\n=== FINAL COUNTS AFTER RE-ADDING PURE TRIVIA ===')
total = 0
for k in sorted(cleaned_db.keys()):
    print(f'Level {k}: {len(cleaned_db[k])} questions')
    total += len(cleaned_db[k])
print(f'TOTAL: {total}')

new_js = 'window.QUESTIONS_DATA = ' + json.dumps(cleaned_db, ensure_ascii=False, indent=4) + ';'
with open('js/questions_data.js', 'w', encoding='utf-8') as f:
    f.write(new_js)
print('Execution Complete!')
