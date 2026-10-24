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
6. **Ship the data** — why the Hub is required; `hf auth login` / `hf auth whoami`;
   Path A `hf upload <user>/grab_cube ~/.cache/huggingface/lerobot/<folder> --repo-type dataset`
   **plus** `hf repo tag create <user>/grab_cube v3.0 --repo-type dataset` (the trainer
   requires the codebase-version tag that `push_to_hub()` normally creates; without it the
   pod fails with "Your dataset must be tagged with a codebase version") for folders already
   recorded under a wrong namespace (`me/…`), Path B recording with
   `--dataset.repo_id=<user>/grab_cube` so `push_to_hub` (default true) uploads
   automatically, Path C the automatic private push that `--job.target` performs.
   Interactive **name → address** checker (repo ids → dataset/model/W&B URLs, flags a
   namespace that isn't yours).
7. **Launch on HF Jobs** — the full `lerobot-train … --job.target=a10g-small` command
   for the cube task, the `--job.*` table (target, image, timeout=2d, detach, tags), the
   seven things `submit_to_hf` does (login check, model repo created up front, dataset
   reachability, secrets forwarded, submit, stream, push), and the Ctrl+C-detaches /
   `hf jobs logs|ps|cancel` semantics. Interactive **job console** (submit, detach,
   re-attach, cancel, running cost).
8. **Observability with Weights & Biases** — what observability is, `wandb login`
   (key in `~/.netrc` is forwarded to the pod automatically), the `--wandb.*` table
   (enable, project, entity, notes, mode, disable_artifact), `log_freq=200`, the
   "Track this run --> https://wandb.ai/…" link, and a panel-by-panel reading guide
   (`train/loss`, `grad_norm`, `lr`, `samples_per_s`, `dataloading_s` vs `update_s`,
   `eval/eval_loss` via `--dataset.eval_split` + `--eval_steps`). Interactive **live
   dashboard mock** with four scenarios: healthy, LR too high, GPU starving, overfitting.
   Then **the three loss panels decoded**: `train/loss = train/l1_loss + kl_weight ×
   train/kld_loss` (ACT, `kl_weight=10.0`), what L1 (action error vs. the leader) and KLD
   (regularizer on the VAE latent) each measure, healthy shapes, and a real run's numbers
   (11 episodes, step 1 400: l1 0.70→0.33, kld 0.60→0.14, total 6.7→1.7). Interactive
   **loss decomposer** (sliders for l1, kld, kl_weight → total and each term's share).
9. **★ Deployment** — `lerobot-rollout` runs the trained policy on the arm
   (observe → predict chunk → move → repeat). Interactive "watch it run" with a
   **scene-mismatch toggle** (move the camera → it misses, closing the loop with Ch7).
10. **Reading failures** — a debugging table mapping symptoms → causes → fixes, each
   pointing back to data quality (Ch7) or training.
11. **The improvement flywheel** — record → train → run → spot failures → record more.

## The real commands it teaches
```bash
# Put the recorded episodes on the Hub (folder recorded as me/… → your namespace)
hf auth login && hf auth whoami
hf upload $HF_USER/grab_cube ~/.cache/huggingface/lerobot/me/grab_cube_20260926_121936 --repo-type dataset
hf repo tag create $HF_USER/grab_cube v3.0 --repo-type dataset   # version tag the trainer requires

# Train on a Hugging Face Jobs GPU with live W&B logging
wandb login                      # once; key is forwarded to the job
hf jobs hardware                 # pick a flavor
lerobot-train --dataset.repo_id=$HF_USER/grab_cube --policy.type=act --policy.device=cuda \
  --policy.repo_id=$HF_USER/act_grab_cube --output_dir=outputs/train/act_grab_cube \
  --steps=50000 --batch_size=8 --save_freq=10000 \
  --wandb.enable=true --wandb.project=so101 \
  --job.target=a10g-small --job.timeout=6h
hf jobs logs <id> | hf jobs ps | hf jobs cancel <id>

# After cloud training, before rollout: match the pod's (always-latest) LeRobot locally,
# or the policy config fails with "The fields `<name>` are not valid for ACTConfig"
git -C ~/Documents/robotics/lerobot pull && pip install -e "$HOME/Documents/robotics/lerobot[feetech]"

# Train (locally or in a Colab GPU notebook)
lerobot-train --dataset.repo_id=$HF_USER/grab_cube --policy.type=act \
  --output_dir=outputs/train/act_grab_cube --policy.device=cuda \
  --policy.repo_id=$HF_USER/act_grab_cube --wandb.enable=true

# Or dispatch to a Hugging Face Jobs GPU with one flag
lerobot-train ... --job.target=h200 --job.timeout=8h

# Deploy the trained policy on the real arm
lerobot-rollout --policy.path=$HF_USER/act_grab_cube \
  --robot.type=so101_follower --robot.port=/dev/tty.usbmodemXXXX --robot.id=my_follower_arm \
  --robot.cameras="{front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
  --task="Grab the cube" --duration=60
```

## Accuracy notes
Defaults and commands are from lerobot 0.6.2: `lerobot-train` (`steps=100_000`,
`batch_size=8`, `save_freq=20_000`, `log_freq=200`, `--policy.type=act`, `--policy.device`,
`--policy.repo_id`, `--resume`), `JobConfig` (`target`, `image=huggingface/lerobot-gpu:latest`,
`timeout=2d`, `detach`, `tags`) and `lerobot/jobs/hf.py::submit_to_hf` (login check, private
model repo staged up front, `ensure_dataset_available`, `HF_TOKEN` + `WANDB_API_KEY` secrets,
Ctrl-C detaches), `WandBConfig` (`enable`, `project=lerobot`, `entity`, `notes`, `mode`,
`disable_artifact`) ACT's loss in `policies/act/modeling_act.py` (`l1_loss + kl_weight * kld_loss`,
`kl_weight=10.0`, `use_vae=True`, `latent_dim=32`, `chunk_size=100`),
and the metrics in `MetricsTracker` (`loss`, `grad_norm`, `lr`,
`update_s`, `dataloading_s`, `samples_per_s`, `eval_loss` with `dataset.eval_split` +
`eval_steps`), `hf upload … --repo-type dataset` from the il_robots guide, HF Jobs
(`--job.target`, `hf jobs hardware`), the
Colab ACT training notebook, and `lerobot-rollout` for deployment (the record CLI
itself says "use lerobot-rollout for policy deployment"). The **loss curve, the job console, the W&B dashboard and the
deployment run are simulated illustrations** (no GPU/dataset/hardware here); the
device times and the job's running cost are rough and illustrative.

Verified in-browser: loss curve converges (~0.13) and diverges on huge LR; overfit
shows train-loss-down / real-perf-down; deployment grasps normally and misses under
scene mismatch; cloud tabs and checkpoints work; no console errors.

This chapter is **not** the course finale — more chapters are planned (e.g.,
language-conditioned / multi-task policies).
