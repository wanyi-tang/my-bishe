$content = Get-Content "d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\JournalEditor.vue" -Raw
$newContent = $content -replace "import Editor from '\.\./src/index\.js';", "import Editor from '../../src/index.js';"
Set-Content -Path "d:\毕设\毕设代码\vue-tiptap-master\vue-tiptap-master\app\components\JournalEditor.vue" -Value $newContent -Encoding UTF8
Write-Host "Fixed import path in JournalEditor.vue"