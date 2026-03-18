file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复乱码的按钮文本
content = content.replace('娓呯┖绛涢€?/button>', '清空筛选</button>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed Bookshelf.vue button text")
