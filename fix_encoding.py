file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the malformed regex with correct one
old_pattern = '/[锛？;\\n]/;'
new_pattern = '/[，,;\\n]/;'

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print(f"✓ Fixed malformed regex pattern")
else:
    # Try to find any variation
    import re
    matches = re.findall(r'/\[.,;\s*\\?n?\]/;', content)
    if matches:
        print(f"Found patterns: {matches}")
        for match in matches:
            content = content.replace(match, '/[，,;\\n]/;')
        print("✓ Standardized regex pattern")
    else:
        print("Pattern looks correct or different issue")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
