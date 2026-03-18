file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the line with tagSeparators
for i, line in enumerate(lines):
    if 'const tagSeparators' in line and '[，,;' in line:
        # Check if it's malformed (has actual newline instead of \n)
        if '/[，,;\n]/;' not in line and len(line.strip()) < 30:
            # This might be split across lines, merge it
            if i+1 < len(lines) and ']/;' in lines[i+1]:
                # Merge the two lines
                merged_line = line.rstrip('\n').rstrip('\\') + '\\n]/;\n'
                lines[i] = merged_line
                lines.pop(i+1)
                print(f"✓ Fixed multiline regex at line {i+1}")
                break

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done checking Bookshelf.vue")
