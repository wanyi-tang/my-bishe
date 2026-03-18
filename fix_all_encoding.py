file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

modified = False
for i in range(len(lines)):
    old_line = lines[i]
    new_line = old_line
    
    # 修复 placeholder 乱码
    if 'placeholder="鎼灭储涔﹀悕' in new_line:
        new_line = new_line.replace('placeholder="鎼灭储涔﹀悕...', 'placeholder="搜索书名..."')
    
    # 确保其他可能的乱码也修复
    if '+ 娣诲姞涔︾睄' in new_line:
        new_line = new_line.replace('+ 娣诲姞涔︾睄', '+ 添加书籍')
    
    if new_line != old_line:
        lines[i] = new_line
        print(f"✓ Fixed line {i+1}:")
        print(f"  Old: {old_line.strip()}")
        print(f"  New: {new_line.strip()}")
        modified = True

if modified:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("\n✓ Successfully fixed all encoding issues in Bookshelf.vue!")
else:
    print("No additional encoding issues found.")
