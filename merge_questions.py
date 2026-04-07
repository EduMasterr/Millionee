import json
import os
import re

folder = r"C:\Users\A1\Desktop\Millione\المليون"
files = {
    "1": "1.txt",
    "2": "2.txt",
    "3": "3.txt",
    "4": "4.txt",
    "5": "5.txt"
}

merged_data = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": []
}

seen_questions = set()
total_original = 0

print("=== جاري معالجة ودمج ملفات الأسئلة ===\n")

for level, fname in files.items():
    fpath = os.path.join(folder, fname)
    if not os.path.exists(fpath):
        print(f"تحذير: الملف {fname} غير موجود.")
        continue
        
    try:
        # Some files might have multiple JSON arrays or slightly broken JSON
        # Let's try to find all JSON-like objects [...] in the file
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Extract everything between [ and ]
        # Since files are structured as arrays, we can find them
        # Note: Some files might have multiple arrays like [..][..]
        arrays = re.findall(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
        
        level_questions = []
        for arr_str in arrays:
            try:
                data = json.loads(arr_str)
                if isinstance(data, list):
                    level_questions.extend(data)
            except json.JSONDecodeError:
                # If direct fast loading fails, try a more robust approach if needed
                continue
        
        # If no arrays found, try parsing the whole content if it's a single array
        if not level_questions:
            try:
                level_questions = json.loads(content)
            except:
                pass

        if not level_questions:
            print(f"فشل في استخراج أسئلة من {fname}")
            continue

        added_to_level = 0
        total_original += len(level_questions)
        
        for q in level_questions:
            q_text = q.get('question', '').strip()
            if not q_text:
                continue
                
            # Deduplicate by text
            if q_text not in seen_questions:
                seen_questions.add(q_text)
                # Ensure the question object has consistent structure
                clean_q = {
                    "id": q.get("id", len(seen_questions)),
                    "question": q_text,
                    "options": q.get("options", []),
                    "answer": q.get("answer", ""),
                    "level": level, # Force level to match pool
                    "category": q.get("category", "عام")
                }
                merged_data[level].append(clean_q)
                added_to_level += 1
        
        print(f"تمت معالجة {fname}: {len(level_questions)} سؤال أصلي -> {added_to_level} سؤال فريد تم إضافته.")

    except Exception as e:
        print(f"خطأ في معالجة {fname}: {str(e)}")

# Combine into the final format
final_js = f"window.QUESTIONS_DATA = {json.dumps(merged_data, ensure_ascii=False, indent=2)};"

output_path = r"C:\Users\A1\Desktop\Millione\js\questions_data.js"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_js)

print(f"\n{'='*40}")
print(f"الإجمالي الأصلي: {total_original}")
print(f"الإجمالي الفريد النهائي: {len(seen_questions)}")
print(f"تم حفظ الملف الجديد في: {output_path}")
