$filePath = "d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"
$content = Get-Content $filePath -Raw -Encoding UTF8

# Replace the whole line with correct pattern
$oldLine = 'const tagSeparators = /[锛？;\n]/;'
$newLine = 'const tagSeparators = /[，,;\n]/;'

if ($content -match [regex]::Escape($oldLine)) {
    $content = $content.Replace($oldLine, $newLine)
    Set-Content $filePath -Value $content -Encoding UTF8 -NoNewline
    Write-Host "✓ Fixed using PowerShell Replace"
} else {
    # Try regex approach
    $pattern = '/\[.{3,6};\\n\]/;'
    if ($content -match $pattern) {
        Write-Host "Found pattern: $($Matches[0])"
        $content = $content -replace $pattern, '/[，,;\\n]/;'
        Set-Content $filePath -Value $content -Encoding UTF8 -NoNewline
        Write-Host "✓ Fixed using Regex"
    } else {
        Write-Host "Pattern not found or already correct"
        # Show what's actually on line 211
        $lines = Get-Content $filePath
        Write-Host "Line 211:" $lines[210]
    }
}
