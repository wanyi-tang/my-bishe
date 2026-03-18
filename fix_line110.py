# -*- coding: utf-8 -*-
file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查并修复第 110 行
old_text = '作者？/h3>'
new_text = '作者</h3>'

if old_text in content:
    content = content.replace(old_text, new_text)
    print(f"✓ Found and replaced '{old_text}' with '{new_text}'")
else:
    print(f"✗ Text '{old_text}' not found")
    # Try to find any variation
    import re
    matches = re.findall(r'<h3>.*?</h3>|<h3>[^\n]*', content)
    print("\nAll h3 tags found:")
    for m in matches[:20]:
        print(f"  {repr(m)}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nLines 108-115 after fix:")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i in range(107, min(115, len(lines))):
        print(f"Line {i+1}: {lines[i].rstrip()}")
