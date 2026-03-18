# -*- coding: utf-8 -*-
file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 修复第 110 行
fixed = False
for i, line in enumerate(lines):
    if '浣滆€?' in line or ('作者？' in line and '</h3>' not in line):
        print(f"Found problem at line {i+1}: {line.rstrip()}")
        lines[i] = line.replace('作者？/h3>', '作者</h3>').replace('浣滆€？/h3>', '作者</h3>')
        print(f"Fixed to: {lines[i].rstrip()}")
        fixed = True
        break

if not fixed:
    print("No obvious problem found, checking all h3 tags...")
    for i, line in enumerate(lines):
        if '<h3>' in line and '</h3>' not in line:
            print(f"Incomplete h3 at line {i+1}: {line.rstrip()}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nDone! Checking lines 108-115:")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i in range(107, min(115, len(lines))):
        print(f"Line {i+1}: {lines[i].rstrip()}")
