# PARAMETER GOLF + AUTORESEARCH — FULL DEVELOPMENT TRACK
# From zero setup to final submission, using Karpathy-style autonomous research loops

## 0. Goal

Build a **Parameter Golf research system** that uses the **autoresearch workflow pattern** to repeatedly improve a model for OpenAI’s challenge:

- final artifact must fit in **16MB**
- leaderboard submissions must train in **under 10 minutes on 8xH100s**
- score is based on **FineWeb validation bits per byte (bpb)**, where lower is better :contentReference[oaicite:0]{index=0}

The `parameter-golf` repo currently centers around `train_gpt.py` / `train_gpt_mlx.py`, while `autoresearch` is built around a small setup where the agent edits **one training file**, follows human-written instructions from `program.md`, and keeps or discards experiments based on **`val_bpb`** under a fixed time budget. :contentReference[oaicite:1]{index=1}

---

## 1. High-level strategy

Do **not** use `autoresearch` as a literal drop-in replacement.

Use it as a **research operating system pattern**:

- one main editable training file
- one human-authored `program.md`
- one experiment loop
- one metric-driven accept/reject rule
- one persistent experiment log
- one git branch / snapshot trail for accepted ideas :contentReference[oaicite:2]{index=2}

For this challenge, adapt that pattern to:

- editable file: `train_gpt.py`
- metric: `val_bpb`
- hard constraints:
  - artifact size ≤ 16,000,000 bytes
  - realistic path to 10-minute / 8xH100 compliance
- decision rule: only keep changes that improve the constrained objective

---

## 2. Final system you are building

By the end, your project should look like this:

```text
parameter-golf-lab/
  README.md
  program.md
  train_gpt.py
  train_gpt_mlx.py
  requirements.txt
  run_local.sh
  run_cloud.sh
  evaluate_candidate.py
  parse_logs.py
  estimate_runtime.py
  artifact_check.py
  results/
    experiments.csv
    accepted/
    rejected/
    best/
  prompts/
    system_prompt.md
    experiment_prompt.md
    review_prompt.md
  notes/
    baseline.md
    ideas_backlog.md
    leaderboard_notes.md
  scripts/
    snapshot_best.sh
    revert_last.sh
    launch_batch.sh
    package_submission.sh

3. Development phases

You should build this in 9 phases.

PHASE 1 — Understand the challenge and lock the objective
Objective

Make sure your whole system optimizes the right thing.

What you need to internalize

The challenge is not “train a good tiny model” in a vague sense. It is:

valid training run
valid self-contained artifact under 16MB
valid runtime path under the challenge budget
minimize FineWeb validation bpb
keep the approach reproducible and submission-friendly
Deliverables

Create these files first:

notes/baseline.md

Include:

challenge objective
allowed innovation areas
hard constraints
what counts as a “winning” improvement
what would make a result invalid
notes/leaderboard_notes.md

Copy down observed winning patterns from the public leaderboard, such as:

mixed low-bit quantization
larger MLP ratios
BigramHash / tokenizer-ish tricks
SWA
Muon / weight-decay tweaks
sliding window eval
QAT variants
deeper stacks like 10L / 11L
Exit criteria

You can explain in one paragraph:

what the score is
what the hard limits are
what your system will optimize
what you are not allowed to break
PHASE 2 — Build the repo and environment from scratch
Objective

Get the official code running before adding any autonomous loop.

Actions
Fork openai/parameter-golf
Clone your fork locally
Create a clean Python environment
Install repo dependencies
Run the official baseline path first
If on Apple Silicon, use the MLX path first because the repo explicitly provides train_gpt_mlx.py for local iteration on Apple hardware.
Required first milestone

You must successfully do:

dependency install
one local training run
one evaluation output
one artifact generation
one size measurement
Deliverables

Create:

README.md

Document:

setup steps
local machine specs
whether you are using MLX or CUDA locally
where logs are saved
how to re-run the baseline
results/experiments.csv

Columns:

run_id,timestamp,branch,seed,mode,change_summary,val_bpb,artifact_bytes,train_seconds,status,accepted,notes
Exit criteria

You can reproduce one baseline run end-to-end with no hand fixing.

PHASE 3 — Recreate the autoresearch pattern for Parameter Golf
Objective

Turn the challenge repo into a controlled research loop.

Why this matters

autoresearch is deliberately minimal:

agent edits one file: train.py
human edits program.md
training runs on a fixed budget
metric is val_bpb
experiments are compared and kept/reverted automatically

You want the same behavior, but adapted to parameter-golf.

Your adaptation

Use:

editable file: train_gpt.py
human policy file: program.md
experiment evaluator: evaluate_candidate.py
persistent ledger: results/experiments.csv
Build these files
program.md

This is the core human-written instruction file for the coding agent.
It should say:

edit only train_gpt.py unless explicitly allowed
optimize constrained val_bpb
never break artifact-size validity
prefer one hypothesis per run
keep diffs small and attributable
log every run
if change worsens score or breaks constraints, revert
if two ideas tie, keep the simpler one
do not silently change evaluation methodology unless the experiment is explicitly about evaluation
do not introduce hidden external dependencies
prioritize ideas in this order:
architecture efficiency
compression / quantization
training dynamics
tokenizer / representation tricks if valid
eval-time improvements only if clearly allowed and honestly reported
evaluate_candidate.py

Responsibilities:

read training logs
extract val_bpb
measure artifact file size
read wall-clock time
assign status
decide accept / reject
append row to results/experiments.csv
artifact_check.py

Responsibilities:

locate produced artifact
compute exact bytes
fail if > 16,000,000 bytes
parse_logs.py

Responsibilities:

robustly parse logs even if format changes slightly
return JSON-like record:
{
  "val_bpb": ...,
  "train_seconds": ...,
  "artifact_path": ...,
  "artifact_bytes": ...,
  "status": "ok" | "crash" | "oversize" | "timeout" | "parse_error"
}
Exit criteria

You can:

modify train_gpt.py
run one experiment
automatically log results
automatically accept or reject the change
PHASE 4 — Establish a trustworthy baseline and control system
Objective

Before searching, create a stable baseline so you can tell what actually helped.

Actions

Run multiple baseline seeds.

Recommended:

3 to 5 baseline runs with no code changes
identical environment
only seed changes
What you want to learn
typical baseline val_bpb
run-to-run variance
normal artifact size
normal train time
whether your local proxy is stable enough to guide search
Deliverables
notes/baseline.md

Add:

baseline mean / min / max
artifact size range
runtime range
observed instability notes
results/best/

Store:

best clean baseline checkpoint
logs
exact code snapshot
Acceptance rule for future experiments

Do not accept a candidate unless it beats:

the current champion
or a rolling mean threshold if variance is high

Suggested rule:

accept if val_bpb improves by meaningful margin and constraints remain valid
if margin is tiny, require repeat confirmation
Exit criteria

You have one locked baseline champion and know what “noise” looks like.

PHASE 5 — Build the two-tier search system
Objective

Separate cheap local search from expensive true-validation runs.

Why

The official challenge is judged under a strict 10-minute / 8xH100 setup. Local iteration is for idea discovery, not final truth.

Tier A — local proxy loop

Purpose:

rapid idea screening
code debugging
trend detection
sanity checking

Examples:

Apple Silicon + MLX
smaller GPU rental
shortened evaluation subset if clearly marked as proxy
smaller repeat budget
Tier B — true or near-true validation

Purpose:

validate only top candidates
estimate whether local gains transfer
prepare real submission evidence
Build these files
estimate_runtime.py

Should estimate:

whether current config likely fits challenge runtime
expected scaling from your test device to target device
a conservative “safe / risky / invalid” label
run_local.sh

Purpose:

launch cheap proxy experiments
store outputs in predictable folder structure
run_cloud.sh

Purpose:

launch promoted experiments on stronger hardware
preserve exact env / command / commit hash
Promotion policy

Only promote a local candidate if:

it is valid locally
artifact is under budget
gain is repeated or clearly large
idea is interpretable enough to debug if it fails on larger hardware
Exit criteria

You have a real funnel:

many cheap runs
few promoted runs
one champion queue
PHASE 6 — Structured research roadmap
Objective

Do not let the agent mutate randomly. Search in organized waves.

Wave 1 — Reproduce known good public directions

Start with ideas already visible on the leaderboard:

mixed low-bit quantization
int6 / int5 variants
larger MLP expansion
SWA
Muon + weight decay changes
deeper stacks
eval-window changes
BigramHash or other representation tweaks

Goal:

learn which public ideas transfer into your fork
gain confidence in your loop
Wave 2 — Architecture efficiency

Search:

aggressive parameter tying
shared block weights
recurrent depth reuse
tied projections
KV-head asymmetry
reduced unique parameter count with repeated compute
norm sharing
compact feedforward variants
gated MLP variants
thin-deep vs shallow-wide tradeoffs
Wave 3 — Compression and artifact optimization

Search:

mixed precision packing
int8 embeddings + int6 blocks
QAT / STE paths
zstd packaging variations if allowed by repo flow
layout choices that compress better
shared tables / codebooks
low-rank factorization that reduces stored bytes
Wave 4 — Training dynamics

Search:

LR schedule
warmup / warmdown
weight decay
SWA timing
EMA if allowed and helpful
total token allocation
context length tradeoffs
batch size tradeoffs
Wave 5 — Representation / tokenizer innovations

Only do this if you fully understand validity and comparability.
Possible directions:

byte-friendly tokenizer settings
hashed ngram features
hybrid token + byte strategies
vocab-size / compression tradeoffs
Wave 6 — Eval-time compute and creative tricks

Only pursue if clearly within challenge spirit and honestly disclosed:

sliding window evaluation
test-time adaptation
small adapters / LoRA-style TTT if valid
extended context at eval if train/eval remain fair

The leaderboard already shows examples like sliding-window eval and test-time training style ideas, so this is a real direction, but it must be carefully documented.

Exit criteria

You have a prioritized backlog, not a pile of random experiments.

PHASE 7 — Prompt system for the coding agent
Objective

Use the coding agent productively instead of letting it thrash.

Create these prompt files
prompts/system_prompt.md

Core role:

you are a careful ML research engineer
you optimize constrained val_bpb
you must preserve reproducibility
you must keep changes small, testable, and reversible
you must not edit files outside allowed scope
you must log every hypothesis and result
prompts/experiment_prompt.md

Template:

current champion metrics
current allowed scope
one target research wave
one hypothesis bucket
maximum allowed diff size
command to run evaluation
required output format:
hypothesis
exact changes
expected mechanism
risk
success criteria
revert condition
prompts/review_prompt.md

Template:

compare candidate vs champion
identify whether gain is likely real, noisy, or invalid
identify accidental confounds
recommend:
accept
reject
repeat
ablate
Agent operating rules

The agent should:

inspect current champion
choose one hypothesis
modify train_gpt.py
run experiment
parse result
decide whether to keep or revert
append result to ledger
propose next best experiment
Exit criteria

You can hand the repo + program.md + prompts to a coding agent and get disciplined iterations.

PHASE 8 — Experiment management and research hygiene
Objective

Keep the project scientifically clean enough that your final result is credible.

Rules
One meaningful change per experiment
Never change training code and evaluation methodology in the same run unless that is the entire point
Every accepted run must have:
commit hash
diff summary
metric
artifact bytes
runtime
seed
Any surprising gain must be repeated
Any huge gain must be ablated
Required folders
results/accepted/

Store:

code snapshot
logs
metrics json
artifact copy
results/rejected/

Store:

minimal metadata only
no need to preserve all artifacts unless debugging
results/best/

Store:

current champion only
latest reproducibility notes
Add these scripts
scripts/snapshot_best.sh

Should:

copy current best code and artifact into results/best/
save git hash
save metrics json
scripts/revert_last.sh

Should:

reset working copy to previous accepted champion
scripts/launch_batch.sh

Should:

run a small queue of experiments, one at a time
stop on repeated failures
Exit criteria

Your lab can run for hours without becoming messy or ambiguous.

PHASE 9 — Submission engineering
Objective

Turn your best research result into a valid challenge submission.

What needs to be true

Your candidate must have:

valid score
valid artifact size
valid training runtime path
reproducible commands
clear writeup of what changed
sufficient evidence if you claim leaderboard-worthy improvement
Build this file
scripts/package_submission.sh

It should:

collect final artifact
verify exact bytes
collect logs
collect training command
collect git commit hash
collect summary notes
package everything into a clean submission folder
Create final writeup template

Make:

submission_summary.md

Sections:

title
author / handle
score
artifact size
train runtime
hardware used for validation
core idea
exact changes from baseline
why it works
risks / caveats
reproducibility steps
Before submission, run this checklist
Validity checklist
 artifact is under 16,000,000 bytes
 code is self-contained
 run is reproducible from clean checkout
 logs parse correctly
 final score is from the intended setup
 no accidental dependency on local files
 no hidden extra training outside declared procedure
 final summary matches what code actually does
Exit criteria

You could hand the package to someone else and they could understand and rerun it.

4. Suggested timeline
Day 1
fork repo
run baseline
create logging + artifact check
create program.md
Day 2
recreate autoresearch loop
baseline multiple seeds
lock champion
build local proxy flow
Day 3–4
wave 1 experiments
reproduce public-style ideas
confirm loop quality
Day 5–7
wave 2 architecture search
wave 3 compression search
Day 8–10
wave 4 training dynamics
begin larger validation runs
Day 11–13
wave 5 representation search
ablations on top 3 candidates
Day 14+
wave 6 creative tricks
final validation
submission packaging
5. Exact acceptance policy

Use this decision tree for every run:

Reject immediately if:
run crashes
logs are incomplete
artifact is oversized
candidate is obviously too slow
gain comes from an invalid evaluation mismatch
Accept immediately if:
candidate beats champion by meaningful margin
constraints are satisfied
diff is understandable
no confound is detected
Repeat before accepting if:
gain is small
variance is high
multiple mechanisms changed at once
result looks too good to trust
Prefer simpler candidate if:
score difference is tiny
code complexity increases a lot
reproducibility gets worse
6. Recommended experiment order

Run these in this order:

clean baseline reproduction
learning-rate / weight-decay / SWA tuning
MLP expansion ratio search
layer depth search
mixed precision / quantization search
parameter tying / recurrent block reuse
eval-window / context-length experiments
tokenizer / hashing experiments
creative eval-time compute
final ablations and combinations

Reason:
This gets you quick wins first, then deeper structural ideas later.

7. Minimal first version of program.md

Use this as your initial draft:

# Parameter Golf Research Program

You are optimizing `train_gpt.py` for OpenAI's Parameter Golf challenge.

Primary objective:
- minimize validation bits per byte (`val_bpb`)

Hard constraints:
- final artifact must be <= 16,000,000 bytes
- candidate must remain plausibly compatible with the challenge runtime budget
- preserve reproducibility
- do not add hidden dependencies
- do not edit files outside the allowed scope unless explicitly instructed

Allowed scope:
- `train_gpt.py` only

Research behavior:
- propose one hypothesis at a time
- make small, attributable diffs
- after each run, record:
  - hypothesis
  - exact change
  - val_bpb
  - artifact size
  - runtime
  - accept/reject decision
- if the candidate worsens the objective or violates constraints, revert it
- if two candidates are similar, keep the simpler one

Priority search order:
1. training hyperparameters
2. architecture efficiency
3. compression / quantization
4. parameter tying / recurrence
5. representation / tokenizer ideas
6. eval-time improvements only if honestly documented

Do not:
- silently change evaluation protocol unless that is the explicit experiment
- make broad rewrites
- optimize for aesthetics over score
- keep a change that cannot be explained
8. Minimal first implementation tasks

Do these first before anything fancy:

Task 1

Get baseline run working.

Task 2

Write artifact_check.py.

Task 3

Write parse_logs.py.

Task 4

Write evaluate_candidate.py.

Task 5

Create results/experiments.csv.

Task 6

Write first program.md.

Task 7

Run one manual “agent-style” experiment yourself.

Task 8

Only after that, start using a coding agent to automate loops.

9. What success looks like

A good final system is one where:

you can launch experiments quickly
every run is logged
bad runs are automatically rejected
good runs are easy to compare
your agent is constrained enough to be useful
your best candidate is always packaged and reproducible
you can explain exactly why your score improved

That is the right way to combine parameter-golf with the autoresearch pattern:

use OpenAI’s repo as the challenge substrate
use Karpathy’s repo as the research-loop template
build a strict, constrained, reproducible experiment engine around train_gpt.py and program.md