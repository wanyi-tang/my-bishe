import re

file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the regex pattern
old_regex = r"/\[，,;\]/;"
new_regex = r"/[，,;\\n]/;"

if old_regex in content:
    updated_content = content.replace(old_regex, new_regex)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✓ Fixed regex pattern in Bookshelf.vue!")
else:
    print("Regex pattern looks correct or different issue.")
    # Let's check what we have
    import re
    match = re.search(r'const tagSeparators = .*?;', content)
    if match:
        print(f"Current pattern: {match.group()}")
