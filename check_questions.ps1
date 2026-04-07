$folder = "C:\Users\A1\Desktop\Millione\المليون"
$files = Get-ChildItem "$folder\*.txt"
$totalIds = @()
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $m = [regex]::Matches($content, '"id"\s*:\s*(\d+)')
    $ids = $m | ForEach-Object { [int]$_.Groups[1].Value }
    Write-Host ($file.Name + ": " + $ids.Count + " question")
    $totalIds += $ids
}
$unique = ($totalIds | Sort-Object -Unique).Count
$dupes = $totalIds.Count - $unique
Write-Host ""
Write-Host ("Total IDs found: " + $totalIds.Count)
Write-Host ("Unique questions: " + $unique)
Write-Host ("Duplicate IDs: " + $dupes)
# Show which IDs are duplicated
$groups = $totalIds | Group-Object | Where-Object { $_.Count -gt 1 }
Write-Host ("Number of duplicate ID groups: " + $groups.Count)
