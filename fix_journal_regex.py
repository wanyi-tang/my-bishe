import sys

file_path = r"d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\JournalEditor.vue"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    
    # Check and fix line 72 (index 71)
    if len(lines) > 71:
        old_line_72 = lines[71]
        if ',,' in old_line_72 or '[, ,' in old_line_72:
            lines[71] = old_line_72.replace('/[,,;\\n]/', '/[，,;\\n]/').replace('/[, , ;\\n]/', '/[，,;\\n]/')
            if lines[71] != old_line_72:
                print(f"✓ Fixed line 72:")
                print(f"  Old: {old_line_72.strip()}")
                print(f"  New: {lines[71].strip()}")
                modified = True
    
    # Check and fix line 118 (index 117)
    if len(lines) > 117:
        old_line_118 = lines[117]
        if '[, ,' in old_line_118:
            lines[117] = old_line_118.replace('/[, , ;\\n]/', '/[，,;\\n]/')
            if lines[117] != old_line_118:
                print(f"✓ Fixed line 118:")
                print(f"  Old: {old_line_118.strip()}")
                print(f"  New: {lines[117].strip()}")
                modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("\n✓ Successfully fixed regex patterns in JournalEditor.vue!")
    else:
        print("Patterns look correct or different issue.")
        # Show current patterns
        for i in [71, 117]:
            if i < len(lines):
                print(f"Line {i+1}: {lines[i].strip()}")
                
except Exception as e:
    print(f"✗ Error: {e}", file=sys.stderr)
    sys.exit(1)
