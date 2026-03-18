# -*- coding: utf-8 -*-
file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all remaining encoding issues
replacements = {
    '鏆傛棤绗﹀悎绛涢€夌殑涔︾睄': '暂无符合筛选的书籍',
    '褰撳墠涔︽灦鏆傛棤涔︾睄': '当前书架暂无书籍',
    '娣诲姞涔︾睄': '添加书籍'
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Fixed: '{old[:20]}...' -> '{new}'")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ All encoding issues fixed!")
print("\nFinal verification (lines 62-68):")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i in range(61, min(68, len(lines))):
        print(f"Line {i+1}: {lines[i].rstrip()}")
