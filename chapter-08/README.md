# Chapter 8 — Training & Running the Policy 📉🤖

An interactive HTML lesson that closes the **record → train → run** loop: turn the
demonstrations from Chapter 7 into a trained ACT policy, then deploy it on the arm.

## How to use it
Open **`index.html`** in any browser. Self-contained, no internet needed.
Scroll or use **↓ / ↑**; the dots on the right jump between sections.

## What it teaches
1. **Training = the Chapter-5 loop at scale** — batch of frames → ACT predicts an
   action chunk → **L1 loss** vs your real actions → backprop → repeat ~100k times.
2. **Steps, batches & epochs** — `batch_size=8`, `steps=100_000` defaults; an
   interactive calculator (frames × steps → epochs / frames seen).
3. **★ The loss curve** — a live simulated training run: loss falls and flattens; a
   **learning-rate** slider (tiny → crawls, huge → diverges); an **overfit toggle**
   that shows training loss dropping while real-world performance *falls* (ties to
   Chapter 7's "object always in the same spot").
4. **Checkpoints** — saved every `save_freq=20_000` steps to
   `output_dir/checkpoints/`; resume, pick the best, deploy any. Interactive
   save-point timeline.
5. **Where to train + ☁️ cloud sub-section** — local Mac (MPS, slow) vs cloud GPU;
   the **HF Hub as the bridge** (record locally → push dataset → train on a cloud
   GPU → pull the policy back → run locally). Tabs for **Google Colab** (free GPU
   notebook) and **Hugging Face Jobs** (`--job.target=<gpu>`), with real commands.
6. **★ Deployment** — `lerobot-rollout` runs the trained policy on the arm
   (observe → predict chunk → move → repeat). Interactive "watch it run" with a
   **scene-mismatch toggle** (move the camera → it misses, closing the loop with Ch7).
7. **Reading failures** — a debugging table mapping symptoms → causes → fixes, each
   pointing back to data quality (Ch7) or training.
8. **The improvement flywheel** — record → train → run → spot failures → record more.

## The real commands it teaches
```bash
# Train (locally or in a Colab GPU notebook)
lerobot-train --dataset.repo_id=$HF_USER/grab_cube --policy.type=act \
  --output_dir=outputs/train/act_grab_cube --policy.device=cuda \
  --policy.repo_id=$HF_USER/act_grab_cube --wandb.enable=true

# Or dispatch to a Hugging Face Jobs GPU with one flag
lerobot-train ... --job.target=h200 --job.timeout=8h

# Deploy the trained policy on the real arm
lerobot-rollout --policy.path=$HF_USER/act_grab_cube \
  --robot.type=so101_follower --robot.port=/dev/tty.usbmodemXXXX \
  --robot.cameras="{front:{type:opencv,index_or_path:0,width:640,height:480,fps:30}}" \
  --task="Grab the cube" --duration=60
```

## Accuracy notes
Defaults and commands are from lerobot: `lerobot-train` (`steps=100_000`,
`batch_size=8`, `save_freq=20_000`, `--policy.type=act`, `--policy.device`,
`--policy.repo_id`, `--resume`), HF Jobs (`--job.target`, `hf jobs hardware`), the
Colab ACT training notebook, and `lerobot-rollout` for deployment (the record CLI
itself says "use lerobot-rollout for policy deployment"). The **loss curve and the
deployment run are simulated illustrations** (no GPU/dataset/hardware here); the
device times are rough and illustrative.

Verified in-browser: loss curve converges (~0.13) and diverges on huge LR; overfit
shows train-loss-down / real-perf-down; deployment grasps normally and misses under
scene mismatch; cloud tabs and checkpoints work; no console errors.

This chapter is **not** the course finale — more chapters are planned (e.g.,
language-conditioned / multi-task policies).
