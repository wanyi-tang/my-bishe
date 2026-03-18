import sys

file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\JournalEditor.vue"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the incorrect import path
    old_import = "import Editor from '../src/index.js';"
    new_import = "import Editor from '../../src/index.js';"
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Successfully fixed import path in JournalEditor.vue")
        print(f"  Changed: {old_import}")
        print(f"  To:      {new_import}")
    else:
        print("Import path already correct or different issue")
        # Show what we have
        for i, line in enumerate(content.split('\n')[:10], 1):
            if 'import Editor' in line:
                print(f"Line {i}: {line}")
except Exception as e:
    print(f"✗ Error: {e}", file=sys.stderr)
    sys.exit(1)
