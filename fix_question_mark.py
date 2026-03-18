# -*- coding: utf-8 -*-
file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 注意这里是英文问号 ? 不是中文问号？
old = '作者？/h3>'
new = '作者</h3>'

if old in content:
    content = content.replace(old, new)
    print(f"✓ SUCCESS: Fixed '{old}' -> '{new}'")
else:
    print(f"✗ FAILED: '{old}' not found in file")
    # Show what we have
    import re
    matches = re.findall(r'作者.', content)
    print(f"Found variations of 作者：{set(matches)}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nLine 110 now:")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"Line 110: {lines[109].rstrip()}")
