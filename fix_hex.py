file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

# Read the file as bytes to see what's really there
with open(file_path, 'rb') as f:
    content_bytes = f.read()

# Find the problematic line
lines = content_bytes.split(b'\n')
for i, line in enumerate(lines[205:220], start=206):
    if b'tagSeparators' in line:
        print(f"Line {i}: {line}")
        print(f"Hex: {line.hex()}")
        
# Now try to fix it - look for the pattern with any 3-byte Chinese characters
import re
pattern = rb'/\[[^\]]{3,6};\\?n?\]/;'
matches = re.findall(pattern, content_bytes)
print(f"\nFound patterns: {matches}")

if matches:
    for match in matches:
        print(f"Replacing: {match}")
        content_bytes = content_bytes.replace(match, b'/[\xef\xbc\x8c,\xc2\xb7;\\n]/;')  # ，,·;\n
        
    with open(file_path, 'wb') as f:
        f.write(content_bytes)
    print("\n✓ Fixed!")
else:
    print("\nNo matches found")
