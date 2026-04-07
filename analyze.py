import re
import os
from collections import Counter

folder = r"C:\Users\A1\Desktop\Millione\المليون"
files = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']

all_ids = []
all_questions = []

print("=== تحليل ملفات الأسئلة ===\n")

for fname in files:
    fpath = os.path.join(folder, fname)
    content = open(fpath, encoding='utf-8', errors='ignore').read()
    
    ids = re.findall(r'"id"\s*:\s*(\d+)', content)
    ids = [int(x) for x in ids]
    
    questions = re.findall(r'"question"\s*:\s*"([^"]+)"', content)
    
    print(f"{fname}: {len(ids)} سؤال | IDs من {min(ids) if ids else 'N/A'} إلى {max(ids) if ids else 'N/A'}")
    
    all_ids.extend(ids)
    all_questions.extend(questions)

print(f"\n{'='*40}")
print(f"الإجمالي الكلي (كل الملفات): {len(all_ids)}")

# Duplicate IDs
id_counter = Counter(all_ids)
dup_ids = {k: v for k, v in id_counter.items() if v > 1}
print(f"IDs فريدة: {len(id_counter)}")
print(f"IDs مكررة: {len(dup_ids)} معرف")

# Duplicate Questions (text)
q_counter = Counter(all_questions)
dup_questions = {k: v for k, v in q_counter.items() if v > 1}
print(f"\nنصوص أسئلة فريدة: {len(q_counter)}")
print(f"نصوص أسئلة مكررة: {len(dup_questions)} سؤال")

if dup_questions:
    print(f"\nأمثلة على الأسئلة المكررة (أول 10):")
    for q, count in list(dup_questions.items())[:10]:
        print(f"  [x{count}] {q[:70]}")

print(f"\n{'='*40}")
print(f"الأسئلة الفريدة الحقيقية (بدون تكرار): {len(q_counter)}")
print(f"نسبة التكرار: {(len(all_questions) - len(q_counter)) / len(all_questions) * 100:.1f}%")
