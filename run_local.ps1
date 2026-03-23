# Proxy training on Windows — single-process or torchrun as you prefer.
# Usage: .\run_local.ps1
# Optional: $env:RUN_ID = "my_run"; $env:NPROC = "1"

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$runId = if ($env:RUN_ID) { $env:RUN_ID } else { "local_proxy" }
$out = Join-Path "results/runs" $runId
New-Item -ItemType Directory -Force -Path $out | Out-Null

if (-not $env:DATA_PATH) { $env:DATA_PATH = "./data/datasets/fineweb10B_sp1024" }
if (-not $env:TOKENIZER_PATH) { $env:TOKENIZER_PATH = "./data/tokenizers/fineweb_1024_bpe.model" }
$nproc = if ($env:NPROC) { $env:NPROC } else { "1" }

$logFile = Join-Path $out "train.log"

if ($env:USE_MLX -eq "1") {
    python train_gpt_mlx.py 2>&1 | Tee-Object -FilePath $logFile
} else {
    torchrun --standalone --nproc_per_node=$nproc train_gpt.py 2>&1 | Tee-Object -FilePath $logFile
}

Write-Host "Log: $logFile"
