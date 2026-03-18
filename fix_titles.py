file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('<h1>鎴戠殑涓汉涔︽灦</h1>', '<h1>我的个人书架</h1>'),
    ('<p>鍙戠幇銆佹暣鐞嗗苟璁板綍鎮ㄧ殑闃呰鍐掗櫓</p>', '<p>发现、整理并记录您的阅读冒险</p>')
]

modified = False
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Fixed:")
        print(f"  Old: {old}")
        print(f"  New: {new}\n")
        modified = True

if modified:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated Bookshelf.vue titles!")
else:
    print("Titles look correct already")
