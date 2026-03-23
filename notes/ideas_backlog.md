# Ideas backlog (prioritized)

Pull one item at a time into `prompts/experiment_prompt.md`. Order follows Roadmap Phase 6 waves + quick wins.

## Tier A — quick wins (hyperparameters / dynamics)

- [ ] LR schedule sweep (warmup, warmdown length)
- [ ] Weight decay / Muon momentum endpoints
- [ ] SWA vs EMA timing (if not already fixed in your fork)
- [ ] `VAL_LOSS_EVERY` / logging cadence (does not change score; debugging only)

## Wave 1 — public leaderboard directions

- [ ] Mixed int6 / int8 quantization paths
- [ ] Larger MLP ratio with compression to fit 16MB
- [ ] BigramHash or similar representation tweak
- [ ] Deeper stack (10L–11L) if parameter budget allows

## Wave 2 — architecture efficiency

- [ ] Parameter tying / shared blocks
- [ ] KV asymmetry / GQA tweaks
- [ ] Thin-deep vs shallow-wide tradeoff

## Wave 3 — compression / artifact

- [ ] Packing layout, zstd level, QAT/STE thresholds
- [ ] Embedding precision vs width

## Wave 4 — training dynamics

- [ ] Token budget vs wall clock (iterations × batch)
- [ ] Context length tradeoff (train_seq_len)

## Wave 5 — representation / tokenizer

- [ ] Vocab / BPE settings (only if validity is clear)

## Wave 6 — eval (document everything)

- [ ] Sliding-window eval stride (if allowed for your claim)
- [ ] Any test-time protocol change — **must** be the explicit experiment

## Parked / risky

- [ ] Ideas that touch tokenizer + training in one run (split into two experiments)
