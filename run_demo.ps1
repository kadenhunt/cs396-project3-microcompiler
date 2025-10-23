param([string]$SourcePath = ".\source.txt")

# Build and start the containers (detached)
Write-Host "Starting containers (this may take a bit the first time)..."
docker compose up --build -d | Out-Null

# Wait for gateway /healthz with a fallback timeout
$max = 30
$i = 0
Write-Host "Waiting for gateway to report healthy (or timing out after $max seconds)..."
while ($i -lt $max) {
    try {
        $h = Invoke-RestMethod -Uri http://localhost:5000/healthz -Method Get -ErrorAction Stop
        if ($h -and $h.ok) { Write-Host "Gateway healthy."; break }
    } catch {
        # ignore and retry
    }
    Start-Sleep -Seconds 1
    $i++
}

if ($i -ge $max) {
    Write-Host "Gateway did not report healthy within $max seconds; proceeding anyway."
}

# Run compile and measure elapsed time
Write-Host "Running compile (this calls .\compile.ps1)"
$time = Measure-Command { powershell -ExecutionPolicy Bypass -File .\compile.ps1 -SourcePath $SourcePath }
Write-Host "Compile finished in $($time.TotalSeconds) seconds"

# Attempt to download the produced file
try {
    $outPath = ".\output\out.asm"
    Invoke-WebRequest -Uri http://localhost:5000/download -OutFile $outPath -ErrorAction Stop
    Write-Host "Saved $outPath"
} catch {
    Write-Host "Download failed: $($_.Exception.Message)"
}

Write-Host "Demo run complete. When finished, bring containers down with: docker compose down"
