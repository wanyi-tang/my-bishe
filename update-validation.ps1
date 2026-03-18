param(
    [string]$FilePath = "d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\JournalEditor.vue"
)

# 读取文件内容
$content = Get-Content $FilePath -Raw -Encoding UTF8

# 定义要查找和替换的文本
$oldText = @'
    const saveJournal = () => {
      if (!selectedBookId.value || !currentContent.value.trim()) return;
'@

$newText = @'
    const saveJournal = () => {
      if (!selectedBookId.value) {
        alert('请先选择一本书籍！');
        return;
      }
      if (!currentContent.value.trim()) {
        alert('请输入笔记内容！');
        return;
      }
'@

# 执行替换
if ($content.Contains($oldText)) {
    $content = $content.Replace($oldText, $newText)
    $content | Set-Content $FilePath -Encoding UTF8 -NoNewline
    Write-Host "✓ 验证逻辑已成功更新!" -ForegroundColor Green
} else {
    Write-Host "✗ 未找到匹配的文本，无法替换" -ForegroundColor Red
    Write-Host "`n当前文件中的相关内容:" -ForegroundColor Yellow
    $lines = Get-Content $FilePath -Encoding UTF8
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "const saveJournal") {
            Write-Host "找到于第 $($i+1) 行:" -ForegroundColor Cyan
            for ($j = $i; $j -lt [Math]::Min($i + 3, $lines.Count); $j++) {
                Write-Host "  [$($j+1)] $($lines[$j])"
            }
            break
        }
    }
}
