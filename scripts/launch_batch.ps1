# Run one command per line from a queue file. Stops after $MaxFail consecutive failures.
# Uses cmd /c for each line — keep commands simple (trusted queue file only).
param(
    [string]$Queue = "scripts/experiment_queue.example.txt",
    [int]$MaxFail = 3
)
$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent)

if (-not (Test-Path $Queue)) {
    Write-Error "launch_batch: missing $Queue"
    exit 1
}

$script:line = 0
$script:fail = 0
Get-Content $Queue | ForEach-Object {
    $cmd = $_.Trim()
    $script:line++
    if ($cmd -eq "" -or $cmd.StartsWith("#")) { return }
    Write-Host "=== batch line $($script:line): $cmd ==="
    cmd /c $cmd
    if ($LASTEXITCODE -eq 0) {
        $script:fail = 0
    } else {
        $script:fail++
        Write-Host "launch_batch: command failed ($script:fail / $MaxFail)"
        if ($script:fail -ge $MaxFail) {
            Write-Error "launch_batch: stopping (too many consecutive failures)"
            exit 1
        }
    }
}
Write-Host "launch_batch: queue finished"
