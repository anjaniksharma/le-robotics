# Chapter 9 — From One Task to Many: Language-Conditioned Robots (SmolVLA) 💬

An interactive HTML lesson introducing **VLAs** (Vision-Language-Action models) and
**SmolVLA** — robots you can give instructions to — building on Chapters 5–7.

## How to use it
Open **`index.html`** in any browser. Self-contained, no internet needed.
Scroll or use **↓ / ↑**; the dots on the right jump between sections.

## What it teaches
1. **The limit of one-task ACT** — a specialist that can't take words; a comparison
   with what a VLA adds.
2. **What a VLA is** — Vision + Language + Action: camera + joint state + a text
   **instruction** → an action chunk. **★ Instruction → action demo**: two cubes
   (red/blue) and two targets (box/shelf); pick or type an instruction and the mock
   arm picks the right cube and places it at the right target. Changing only the
   *words* changes the behavior.
3. **Foundation model: pretrain → fine-tune** — like GPT (Ch6), SmolVLA is
   pretrained (450M, `lerobot/smolvla_base`) then fine-tuned on ~50 of your
   episodes. Interactive: competence vs. episodes for ACT-from-scratch vs.
   SmolVLA-fine-tuned (SmolVLA is useful with far less data).
4. **How SmolVLA is wired (one light diagram)** — a vision-language model
   (SmolVLM) + an action expert; one line on flow matching.
5. **One brain, many tasks** — a multi-task switcher (same scene, change the
   instruction → different behavior) + the paper's data tip.
6. **Fine-tuning for real** — `pip install -e ".[smolvla]"`; `lerobot-train
   --policy.path=lerobot/smolvla_base --dataset.repo_id=... --batch_size=64
   --steps=20000`; ~4h on an A100 (cloud, Ch8); deploy with `lerobot-rollout
   --task="..."` where the instruction now matters.
7. **ACT vs SmolVLA** — a when-to-use-which comparison table.
8. **Recap, quiz, homework.**

## Accuracy notes
From lerobot's SmolVLA (`policies/smolvla`) and `smolvla.mdx` / the SmolVLA paper:
450M VLA = pretrained **SmolVLM** (SigLIP vision + a small language model) + an
**action expert**, actions via **flow matching**; fine-tune from
`lerobot/smolvla_base` with `.[smolvla]`, `--batch_size=64 --steps=20000`
(~4h/A100); data tip ~50 episodes with repeats per variation (paper: 5 positions ×
10; 25 was too few). Deployment via `lerobot-rollout` with a meaningful `--task`.

**The instruction → action demos are simplified, clearly-labeled mocks** (keyword
matching, not a real neural net) — a real 450M VLA can't run in a browser. Ch5's
net and Ch6's text model *are* real; this one is illustrative. Every command, size,
and default shown is real.

Verified in-browser: instruction demos parse and animate correctly (red→box,
blue→shelf, pick-only, and an "unknown" fallback); pretrain-vs-finetune shows the
data-efficiency gap (e.g., 20 episodes → ACT 8% vs SmolVLA 70%); no console errors.
Not the course finale.
