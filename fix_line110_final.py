# -*- coding: utf-8 -*-
import sys

file_path = r'd:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用英文问号 (ASCII 0x3F)
old = '作者？/h3>'  # 英文问号
new = '作者</h3>'

if old in content:
    content = content.replace(old, new)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✓ SUCCESS: Fixed 作者？/h3> -> 作者</h3>')
else:
    print('✗ FAILED: 作者？/h3> not found')
    # 显示实际内容
    lines = content.split('\n')
    for i, line in enumerate(lines[107:115], start=108):
        print(f'Line {i}: {line}')
