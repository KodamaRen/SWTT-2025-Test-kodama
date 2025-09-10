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

# 各ブランチを作成してmainの内容を反映させ、リモートにプッシュ
foreach ($branch in $branches) {
    git checkout -b $branch

    git push origin $branch

    git checkout main

    git branch -d $branch
}

Write-Host "すべてのブランチが作成され、リモートにプッシュされました。"
