# -*- coding: utf-8 -*-
file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 英文问号 ?  ASCII 0x3F
old = '作者？/h3>'
new = '作者</h3>'

if old in content:
    content = content.replace(old, new)
    print(f"SUCCESS: Fixed '{old}'")
    print(f"  -> '{new}'")
else:
    print(f"FAILED: '{old}' not found")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"\nLine 110: {lines[109].strip()}")
