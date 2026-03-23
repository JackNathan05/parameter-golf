# Build submission_package/<Name>/ (PowerShell). Optional second arg: path to train.log
param(
    [Parameter(Mandatory = $true)]
    [string]$Name,
    [string]$LogPath = ""
)
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

$out = Join-Path "submission_package" $Name
New-Item -ItemType Directory -Force -Path $out | Out-Null

Copy-Item -Force "train_gpt.py" (Join-Path $out "train_gpt.py")

$destLog = Join-Path $out "train.log"
if ($LogPath -ne "" -and (Test-Path $LogPath)) {
    Copy-Item -Force $LogPath $destLog
} elseif (Test-Path "train.log") {
    Copy-Item -Force "train.log" $destLog
} else {
    $runs = Get-ChildItem -Path "results/runs" -Recurse -Filter "train.log" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    if ($runs) { Copy-Item -Force $runs.FullName $destLog }
}

foreach ($f in @("final_model.int8.ptz", "final_model.int6.ptz")) {
    if (Test-Path $f) {
        Copy-Item -Force $f (Join-Path $out $f)
        break
    }
}

$gitTxt = Join-Path $out "git_commit.txt"
@(
    "$(git rev-parse HEAD 2>$null)"
    "packaged_utc: $([DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ'))"
    "machine: $env:COMPUTERNAME"
) | Set-Content -Encoding utf8 $gitTxt

if (Test-Path $destLog) {
    python parse_logs.py $destLog --json | Set-Content -Encoding utf8 (Join-Path $out "metrics.json")
    $ptz = Get-ChildItem $out -Filter "final_model.*.ptz" | Select-Object -First 1
    if ($ptz) {
        python artifact_check.py $ptz.FullName 2>&1 | Set-Content -Encoding utf8 (Join-Path $out "artifact_check.txt")
    } else {
        "no .ptz in package" | Set-Content (Join-Path $out "artifact_check.txt")
    }
} else {
    '{"error":"no train.log in package"}' | Set-Content -Encoding utf8 (Join-Path $out "metrics.json")
}

Write-Host "Wrote $out"
Get-ChildItem $out
