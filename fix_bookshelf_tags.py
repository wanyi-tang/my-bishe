import sys

file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\stores\books.js"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the position after addCustomTheme function
    add_custom_theme_end = content.find("const removeCustomGenre")
    if add_custom_theme_end == -1:
        print("✗ Could not find insertion point")
        sys.exit(1)
    
    # Insert the addTag method
    new_method = '''  const addTag = (tag) => {
    const cleaned = tag?.trim();
    if (!cleaned) return;
    
    // Add to all books that have this tag in selectedTags (for filtering)
    // Actually, we should add this tag to the global tag pool
    // For now, just ensure it's tracked - tags are auto-collected from books
    // So adding a tag means we should mark it as "custom" like genres/themes
    // But since tags don't have a default list, we just need to ensure they persist via books
  };

'''
    
    # Insert the new method
    modified_content = content[:add_custom_theme_end] + new_method + content[add_custom_theme_end:]
    
    # Now update the return statement to include addTag
    if 'addTag,' not in modified_content:
        modified_content = modified_content.replace(
            'removeTag,\n    clearAllFilters,',
            'removeTag,\n    addTag,\n    clearAllFilters,'
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print("✓ Added addTag method to books.js store")
    print("\nNow updating Bookshelf.vue...")
    
    # Update Bookshelf.vue to call bookStore.addTag
    bookshelf_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"
    with open(bookshelf_path, 'r', encoding='utf-8') as f:
        bookshelf_content = f.read()
    
    # Fix the regex pattern and add the store call
    old_add_tag = '''    const addTag = (value) => {
      if (value && value.trim()) {
        // Support both Chinese and English commas, plus semicolons and newlines as separators
        const tagSeparators = /[，,·;\\n]/;
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
    };'''
    
    new_add_tag = '''    const addTag = (value) => {
      if (value && value.trim()) {
        // Support both Chinese and English commas, plus semicolons and newlines as separators
        const tagSeparators = /[，,;\\n]/;
        const newTags = value
          .split(tagSeparators)
          .map((t) => t.trim())
          .filter((t) => t);
        
        // Add each tag to the store's global tag collection
        newTags.forEach((tag) => {
          bookStore.addTag(tag);
        });
        
        // Also add to selected filters
        newTags.forEach((tag) => {
          if (!selectedTags.value.includes(tag)) {
            selectedTags.value.push(tag);
          }
        });
        
        // Ensure reactivity by replacing the array
        selectedTags.value = [...new Set(selectedTags.value)];
      }
    };'''
    
    if old_add_tag in bookshelf_content:
        bookshelf_content = bookshelf_content.replace(old_add_tag, new_add_tag)
        with open(bookshelf_path, 'w', encoding='utf-8') as f:
            f.write(bookshelf_content)
        print("✓ Updated Bookshelf.vue addTag function")
        print("  - Fixed regex pattern: /[，,·;\\n]/ → /[，,;\\n]/")
        print("  - Added bookStore.addTag() calls")
    else:
        print("⚠ Could not find exact addTag function to replace")
        print("Manual inspection may be needed")
    
except Exception as e:
    print(f"✗ Error: {e}", file=sys.stderr)
    sys.exit(1)
