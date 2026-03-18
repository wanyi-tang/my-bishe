# -*- coding: utf-8 -*-
"""Fix Bookshelf.vue encoding and syntax issues"""

file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the corrupted line 64 - replace mojibake with correct Chinese AND fix syntax
old_line = """            <h3>{{ hasAnyFilter ? '鏆傛棤绗﹀悎绛涢€夌殑涔︾睄' : '褰撳墠涔︽灦鏆傛棤涔︾睄' }}</h3>
            <p>{{ hasAnyFilter ? '璇疯皟鏁寸瓫閫夋潯浠跺悗閲嶈瘯銆？ : '鍙互鍏堟坊鍔犵涓€鏈功銆？ }}</p>
            <div class="empty-actions">
              <button class="add-first-book-btn" @click="openAddDialog">娣诲姞涔︾睄</button>"""

new_line = """            <h3>{{ hasAnyFilter ? '暂无符合筛选的书籍' : '当前书架暂无书籍' }}</h3>
            <p>{{ hasAnyFilter ? '请调整筛选条件后重试。' : '可以先添加第一本书。' }}</p>
            <div class="empty-actions">
              <button class="add-first-book-btn" @click="openAddDialog">添加书籍</button>"""

if old_line in content:
    content = content.replace(old_line, new_line)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Successfully fixed Bookshelf.vue!")
    print("\nFixed issues:")
    print("  1. Corrected mojbake (garbled Unicode)")
    print("  2. Fixed ternary operator syntax (? was missing before :)")
else:
    print("✗ Could not find the target text. File may have different formatting.")
    
# Show verification
print("\nVerification - Line 64 now reads:")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"Line 64: {lines[63].strip()}")
