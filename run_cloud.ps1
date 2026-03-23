# Tier B: promoted run (e.g. 8x GPU). Writes results/runs/<RUN_ID>/train.log and run_meta.txt
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$runId = if ($env:RUN_ID) { $env:RUN_ID } else { "cloud_promoted" }
$out = Join-Path "results/runs" $runId
New-Item -ItemType Directory -Force -Path $out | Out-Null

$meta = Join-Path $out "run_meta.txt"
@(
    "commit: $(git rev-parse HEAD 2>$null)"
    "date_utc: $([DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ'))"
    "machine: $env:COMPUTERNAME"
    "cuda_visible: $env:CUDA_VISIBLE_DEVICES"
) | Set-Content -Encoding utf8 $meta

if (-not $env:DATA_PATH) { $env:DATA_PATH = "./data/datasets/fineweb10B_sp1024" }
if (-not $env:TOKENIZER_PATH) { $env:TOKENIZER_PATH = "./data/tokenizers/fineweb_1024_bpe.model" }
$nproc = if ($env:NPROC) { $env:NPROC } else { "8" }

$logFile = Join-Path $out "train.log"
torchrun --standalone --nproc_per_node=$nproc train_gpt.py 2>&1 | Tee-Object -FilePath $logFile
Write-Host "Log: $logFile meta: $meta"
