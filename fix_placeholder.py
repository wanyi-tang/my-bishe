file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 placeholder 乱码
old_text = 'placeholder="鎼滅储涔﹀悕..."'
new_text = 'placeholder="搜索书名..."'

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Fixed placeholder text in Bookshelf.vue")
    print(f"  Old: {old_text}")
    print(f"  New: {new_text}")
else:
    print("Placeholder text looks correct already")
