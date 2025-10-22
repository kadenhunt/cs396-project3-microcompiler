param([string]$SourcePath = ".\source.txt")

$src = Get-Content $SourcePath -Raw
$result = Invoke-RestMethod -Uri http://localhost:5000/compile `
    -Method Post -Body (@{ source = $src } | ConvertTo-Json) `
    -ContentType "application/json"

if ($result.error) {
  Write-Host "ERROR ($($result.error.phase)): $($result.error.message)"; exit 1
}

Write-Host "`n--- MACHINE CODE ---`n$result.machine"
Write-Host "`nSaved to .\output\out.asm"
