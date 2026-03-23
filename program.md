# Parameter Golf Research Program

You are optimizing `train_gpt.py` for OpenAI's Parameter Golf challenge.

## Primary objective

- Minimize validation bits per byte (`val_bpb`).

## Hard constraints

- Final artifact must be **<= 16,000,000** bytes (as produced by the repo’s training/export path).
- Candidate must remain plausibly compatible with the **challenge runtime budget** (10 minutes on 8×H100 for record-track claims).
- Preserve **reproducibility**; do not add hidden dependencies.
- Do not edit files outside the allowed scope unless explicitly instructed.

## Allowed scope

- **`train_gpt.py` only** for automated research loops (unless a task explicitly allows other files).

## Research behavior

- Propose **one hypothesis at a time**; keep diffs small and attributable.
- After each run, record: hypothesis, exact change, `val_bpb`, artifact size, runtime, accept/reject.
- If the candidate **worsens** the objective or **violates** constraints, **revert**.
- If two candidates are similar, keep the **simpler** one.

## Priority search order

1. Training hyperparameters  
2. Architecture efficiency  
3. Compression / quantization  
4. Parameter tying / recurrence  
5. Representation / tokenizer ideas  
6. Eval-time improvements **only** if honestly documented  

## Do not

- Silently change evaluation protocol unless that **is** the experiment.  
- Broad rewrites or style-only churn.  
- Optimize for aesthetics over score.  
- Keep a change that cannot be explained.
