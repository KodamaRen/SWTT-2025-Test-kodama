git checkout main
git pull origin main

$months = @("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
$suffixes = @("a", "b")
$branches = @()

foreach ($month in $months) {
    foreach ($suffix in $suffixes) {
        $branches += "test/$month-$suffix"
    }
}

# 既存のブランチにmainの内容を反映させる
foreach ($branch in $branches) {
    # ブランチに切り替え
    git checkout $branch
    
    # mainの内容をマージ（差分をコミットとして保存）
    git merge main --no-ff -m "Merge main into $branch"
    
    # 変更をリモートにプッシュ
    git push origin $branch

    # mainに戻る
    git checkout main
}

Write-Host "すべてのブランチにmainの内容が反映され、リモートにプッシュされました。"
