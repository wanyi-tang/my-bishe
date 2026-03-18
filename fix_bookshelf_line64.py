# -*- coding: utf-8 -*-
file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 64 (index 63)
bad_line = "            <p>{{ hasAnyFilter ? '璇疯皟鏁寸瓫閫夋潯浠跺悗閲嶈瘯銆？ : '鍙互鍏堟坊鍔犵涓€鏈功銆？ }}</p>\n"
good_line = "            <p>{{ hasAnyFilter ? '请调整筛选条件后重试。' : '可以先添加第一本书。' }}</p>\n"

if bad_line in lines:
    idx = lines.index(bad_line)
    lines[idx] = good_line
    print(f"✓ Found and replaced line {idx + 1}")
else:
    # Try to find by partial match
    for i, line in enumerate(lines):
        if 'hasAnyFilter' in line and '<p>' in line and '{{' in line:
            print(f"Found similar line at {i + 1}: {line.strip()}")
            lines[i] = good_line
            print(f"✓ Replaced line {i + 1}")
            break
    else:
        print("✗ Could not find the target line")
        exit(1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✓ Successfully fixed Bookshelf.vue line 64!")
print("\nVerification:")
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"Line 64: {lines[63].strip()}")
