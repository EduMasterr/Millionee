const fs = require('fs');
const path = require('path');

const folder = path.join(__dirname, 'المليون');
const files = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt'];

let allIds = [];
let allQuestions = [];

console.log('=== تحليل ملفات الأسئلة ===\n');

files.forEach(file => {
    const filePath = path.join(folder, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Extract all "id": NUMBER patterns
    const idMatches = [...content.matchAll(/"id"\s*:\s*(\d+)/g)];
    const ids = idMatches.map(m => parseInt(m[1]));
    
    // Extract question texts to check text-level duplicates
    const qMatches = [...content.matchAll(/"question"\s*:\s*"([^"]+)"/g)];
    const questions = qMatches.map(m => m[1].trim());
    
    console.log(`${file}: ${ids.length} سؤال (IDs: ${ids[0]} -> ${ids[ids.length-1]})`);
    
    allIds.push(...ids);
    allQuestions.push(...questions);
});

console.log('\n=== النتائج الإجمالية ===');
console.log(`إجمالي الأسئلة (كل الملفات): ${allIds.length}`);

// Check duplicate IDs
const idCount = {};
allIds.forEach(id => { idCount[id] = (idCount[id] || 0) + 1; });
const dupIds = Object.entries(idCount).filter(([id, count]) => count > 1);
const uniqueIds = Object.keys(idCount).length;

console.log(`IDs فريدة: ${uniqueIds}`);
console.log(`IDs مكررة: ${dupIds.length} معرف`);

if (dupIds.length > 0 && dupIds.length <= 30) {
    console.log('\nالـ IDs المكررة:');
    dupIds.forEach(([id, count]) => console.log(`  ID ${id}: مكرر ${count} مرة`));
} else if (dupIds.length > 30) {
    console.log(`\nأول 20 ID مكرر:`);
    dupIds.slice(0, 20).forEach(([id, count]) => console.log(`  ID ${id}: مكرر ${count} مرة`));
}

// Check duplicate QUESTIONS (text-level)
const qCount = {};
allQuestions.forEach(q => { qCount[q] = (qCount[q] || 0) + 1; });
const dupQuestions = Object.entries(qCount).filter(([q, count]) => count > 1);

console.log(`\nنصوص أسئلة فريدة: ${Object.keys(qCount).length}`);
console.log(`نصوص أسئلة مكررة: ${dupQuestions.length} سؤال`);

if (dupQuestions.length > 0 && dupQuestions.length <= 20) {
    console.log('\nأسئلة مكررة (نص):');
    dupQuestions.forEach(([q, count]) => console.log(`  [x${count}] ${q.substring(0, 60)}...`));
} else if (dupQuestions.length > 20) {
    console.log(`\nأول 10 أسئلة مكررة (نص):`);
    dupQuestions.slice(0, 10).forEach(([q, count]) => console.log(`  [x${count}] ${q.substring(0, 60)}`));
}

console.log('\n=== ملخص ===');
console.log(`الإجمالي الحقيقي بعد إزالة التكرار: ${Object.keys(qCount).length} سؤال فريد`);
