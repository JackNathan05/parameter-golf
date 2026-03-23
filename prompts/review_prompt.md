# Review prompt — candidate vs champion

Use after a training run to decide whether the result is trustworthy.

## Inputs

- **Champion:** `val_bpb`, artifact bytes, seed(s), commit hash, key hyperparameters
- **Candidate:** same fields + full diff vs champion

## Compare

1. **Metric:** Is `val_bpb` lower? By how much vs typical run-to-run noise?
2. **Validity:** Artifact size, crash-free log, evaluation protocol unchanged (unless declared)?
3. **Confounds:** Did we change multiple things at once? New eval path? Different data shard?

## Classification

- **Likely real:** Clear margin, single change, stable logs, artifact OK
- **Likely noisy:** Tiny margin, high variance regime, one seed only
- **Likely invalid:** Eval mismatch, oversize artifact, incomplete log, suspicious shortcut

## Recommendation

Pick one: **accept** | **reject** | **repeat** (more seeds) | **ablate** (isolate mechanism)

Add a one-sentence rationale and what to run next.
