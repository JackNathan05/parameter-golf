# Restore train_gpt.py from results/best/<TAG>/train_gpt.py
param(
    [Parameter(Mandatory = $true)]
    [string]$Tag
)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$src = Join-Path (Join-Path "results/best" $Tag) "train_gpt.py"
if (-not (Test-Path $src)) {
    Write-Error "revert_last: missing $src"
}
Copy-Item -Force $src "./train_gpt.py"
Write-Host "restored train_gpt.py from $src"
$meta = Join-Path (Join-Path "results/best" $Tag) "git_commit.txt"
if (Test-Path $meta) {
    Write-Host "snapshot commit: $((Get-Content $meta -Raw).Trim())"
}
