param([string]$SourcePath = ".\source.txt")

# Read the source file as a single string
$src = Get-Content $SourcePath -Raw

# Build a compact JSON payload and force the source value to a string
$payload = @{ source = [string]$src } | ConvertTo-Json -Compress

try {
  $result = Invoke-RestMethod -Uri http://localhost:5000/compile `
    -Method Post -Body $payload `
    -ContentType 'application/json; charset=utf-8'
}
catch {
  # Attempt to show server response body when available
  Write-Host "Request failed:" -ForegroundColor Red
  if ($_.Exception.Response -ne $null) {
    $stream = $_.Exception.Response.GetResponseStream()
    $reader = New-Object System.IO.StreamReader($stream)
    $body = $reader.ReadToEnd()
    Write-Host $body
  } else {
    Write-Host $_.ToString()
  }
  exit 1
}

if ($result.error) {
  Write-Host "ERROR ($($result.error.phase)): $($result.error.message)"; exit 1
}

Write-Host "`n--- MACHINE CODE ---`n$result.machine"
Write-Host "`nSaved to .\output\out.asm"
