# -*- coding: utf-8 -*-
file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复两个问题
fixes = [
    ('作者？/h3>', '作者</h3>'),  # 英文问号
    ('鎻忚堪', '描述'),  # 乱码
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Fixed: '{old}' -> '{new}'")
    else:
        print(f"✗ Not found: '{old}'")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nLines 108-125 after fix:")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i in range(107, min(125, len(lines))):
        print(f"Line {i+1}: {lines[i].rstrip()}")
