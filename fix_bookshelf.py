import re

file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Old function pattern
old_pattern = r"""    const addTag = \(value\) => \{
      if \(value && value\.trim\(\)\) \{
        const next = value\.trim\(\);
        if \(!selectedTags\.value\.includes\(next\)\) \{
          selectedTags\.value = \[\.\.\.new Set\(\[\.\.\.selectedTags\.value, next\]\)\];
        \}
      \}
    \};"""

# New function
new_function = """    const addTag = (value) => {
      if (value && value.trim()) {
        // Support both Chinese and English commas, plus semicolons and newlines as separators
        const tagSeparators = /[，,;\\n]/;
        const newTags = value
          .split(tagSeparators)
          .map((t) => t.trim())
          .filter((t) => t);
        
        newTags.forEach((tag) => {
          if (!selectedTags.value.includes(tag)) {
            selectedTags.value.push(tag);
          }
        });
        
        // Ensure reactivity by replacing the array
        selectedTags.value = [...new Set(selectedTags.value)];
      }
    };"""

# Replace
if re.search(old_pattern, content):
    updated_content = re.sub(old_pattern, new_function, content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✓ Successfully updated addTag function in Bookshelf.vue!")
else:
    print("✗ Could not find the old addTag function.")
    print("\nSearching for pattern...")
    # Try to find what's actually there
    search_result = re.search(r"const addTag.*?\};", content, re.DOTALL)
    if search_result:
        print(f"\nFound this instead:\n{search_result.group()}")
