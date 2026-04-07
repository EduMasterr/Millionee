import json, random

print("Loading Database...")
with open('js/questions_data.js', 'r', encoding='utf-8') as f:
    text = f.read()
start = text.find('{')
end = text.rfind(';')
db = json.loads(text[start:end])

cleaned_db = {"1":[], "2":[], "3":[], "4":[], "5":[]}
unique_qs = set()
removed_git = 0
removed_dupes = 0

for level, qs in db.items():
    for q in qs:
        q_id = str(q.get('id', ''))
        q_text = str(q.get('question', '')).strip()
        
        # 1. Remove github imported questions
        if q_id.startswith('git_'):
            removed_git += 1
            continue
            
        # 2. Remove duplicates by question text
        if q_text in unique_qs:
            removed_dupes += 1
            continue
            
        unique_qs.add(q_text)
        cleaned_db[level].append(q)

print(f"Cleanup Results:")
print(f" - Tossed {removed_git} imported questions with random logic.")
print(f" - Tossed {removed_dupes} duplicate questions.")

# Let's add some fresh, heavily curated questions to replace them!
idx = 90000
def add(level, q, ans, pool):
    global idx
    candidates = [x for x in pool if x != ans]
    if len(candidates) < 3: return
    dists = random.sample(candidates, 3)
    opts = dists + [ans]
    random.shuffle(opts)
    cleaned_db[str(level)].append({'id': f'curated_{idx}', 'question': q, 'options': opts, 'answer': str(ans)})
    idx += 1

# --- Curated Pool ---
historic_dates = [('سقوط الأندلس','1492'),('نهاية الحرب العالمية الثانية','1945'),('هدم جدار برلين','1989'),('حرب السادس من أكتوبر','1973'),('غزوة بدر','2 هـ'),('غزوة أحد','3 هـ'),('فتح مكة','8 هـ')]
yr_pool = [x[1] for x in historic_dates] + ['1914','1939','2001','1990']
for ev, yr in historic_dates:
    add(4, f'متى حدث: {ev}؟', yr, yr_pool)

arab_authors = [('عبقريات العقاد','عباس محمود العقاد'),('طوق الحمامة','ابن حزم الأندلسي'),('البخلاء','الجاحظ'),('رسالة الغفران','أبو العلاء المعري'),('مقدمة ابن خلدون','ابن خلدون')]
auth_pool = [x[1] for x in arab_authors] + ['طه حسين','نجيب محفوظ','توفيق الحكيم']
for book, au in arab_authors:
    add(3, f'من هو مؤلف كتاب "{book}"؟', au, auth_pool)

# Display final counts
print('\n=== FINAL PRISTINE DATABASE COUNTS ===')
total = 0
for k in sorted(cleaned_db.keys()):
    print(f'Level {k}: {len(cleaned_db[k])} questions')
    total += len(cleaned_db[k])
print(f'TOTAL: {total} pure, logical questions.')

# Save to disk
new_js = 'window.QUESTIONS_DATA = ' + json.dumps(cleaned_db, ensure_ascii=False, indent=4) + ';'
with open('js/questions_data.js', 'w', encoding='utf-8') as f:
    f.write(new_js)
print('Database optimized and saved securely!')
