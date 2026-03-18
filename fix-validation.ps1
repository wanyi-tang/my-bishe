$filePath = "d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\JournalEditor.vue"
$content = Get-Content $filePath -Raw -Encoding UTF8

# 查找并替换验证逻辑
$oldValidation = @"
    const saveJournal = () => {
      if (!selectedBookId.value || !currentContent.value.trim()) return;
"@

$newValidation = @"
    const saveJournal = () => {
      if (!selectedBookId.value) {
        alert('请先选择一本书籍！');
        return;
      }
      if (!currentContent.value.trim()) {
        alert('请输入笔记内容！');
        return;
      }
"@

if ($content.Contains($oldValidation)) {
    $content = $content.Replace($oldValidation, $newValidation)
    $content | Set-Content $filePath -Encoding UTF8 -NoNewline
    Write-Host "✓ 文件已成功更新"
} else {
    Write-Host "✗ 未找到要替换的内容"
    Write-Host "当前内容片段:"
    $lines = Get-Content $filePath
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "const saveJournal") {
            for ($j = $i; $j -lt [Math]::Min($i + 5, $lines.Count); $j++) {
                Write-Host "$($j+1): $($lines[$j])"
            }
            break
        }
    }
}
