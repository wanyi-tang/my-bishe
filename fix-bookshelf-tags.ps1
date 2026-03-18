# PowerShell script to fix the addTag function in Bookshelf.vue

$filePath = "d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\Bookshelf.vue"
$content = Get-Content $filePath -Encoding UTF8 -Raw

$oldFunction = @"
    const addTag = (value) => {
      if (value && value.trim()) {
        const next = value.trim();
        if (!selectedTags.value.includes(next)) {
          selectedTags.value = [...new Set([...selectedTags.value, next])];
        }
      }
    };
"@

$newFunction = @"
    const addTag = (value) => {
      if (value && value.trim()) {
        // Support both Chinese and English commas, plus semicolons and newlines as separators
        const tagSeparators = /[，,;\n]/;
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
    };
"@

if ($content.Contains($oldFunction)) {
    $updatedContent = $content.Replace($oldFunction, $newFunction)
    Set-Content -Path $filePath -Value $updatedContent -Encoding UTF8 -NoNewline
    Write-Host "Successfully updated addTag function in Bookshelf.vue!" -ForegroundColor Green
} else {
    Write-Host "Could not find the old addTag function. Please check the file manually." -ForegroundColor Red
    Write-Host "Looking for:" -ForegroundColor Yellow
    Write-Host $oldFunction
}
