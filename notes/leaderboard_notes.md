# Public leaderboard patterns (from OpenAI `parameter-golf` README)

Observed themes in top **record-track** runs (March 2026 snapshot). Use as **hypothesis backlog**, not guaranteed transfers.

## Quantization and packing

- **Mixed low-bit weights** (e.g. int6 blocks, int8 embeddings), often with **QAT** or STE-style paths.
- **zstd** (e.g. level 22) on top of quantized payloads; total **submission byte count** is the real constraint.

## Architecture

- **Deeper stacks** (e.g. 10L–11L) when parameter budget allows.
- **Larger MLP expansion ratios** (e.g. 3×) when paired with compression.
- **XSA / partial attention** on a subset of layers; **GQA**-style KV reduction.

## Training dynamics

- **SWA** or **EMA** for late-training weight averaging.
- **Muon** optimizer variants and **weight decay** tuning.
- **Warmdown** and late-phase **QAT** thresholds.

## Representation / tokenizer

- **BigramHash** or similar hashed n-gram features (vocab/table tradeoffs).
- **Sliding-window evaluation** (stride e.g. 64) when disclosed — improves reported `val_bpb` via eval protocol; only use when your experiment explicitly targets eval.

## Misc

- **RoPE** variants (e.g. partial RoPE), **layer norm scaling**, **SmearGate**-style gating in some entries.

## How to use this file

When proposing a change in `program.md`, **tie ideas to one primary knob**, log whether it’s quantization vs architecture vs dynamics vs eval, and **revert** if `val_bpb` worsens or the artifact blows the budget.
