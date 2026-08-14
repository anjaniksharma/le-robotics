# Chapter 6 — From Words to Motion 💬🤖

An interactive HTML lesson connecting the training fundamentals from Chapter 5 to
**text generation** and then to the SO-101's own brain, **ACT**.

## How to use it
Open **`index.html`** in any browser. Self-contained, no internet needed.
Scroll or use **↓ / ↑**; the dots on the right jump between sections.

## What it teaches
1. **Same loop, three jobs** — a comparison table (image classifier / GPT / ACT):
   only the input, output, and loss change.
2. **Seeing (ResNet, briefly)** — images are grids of numbers; layers find edges →
   objects. Interactive edge-detector you slide across a scene.
3. **Next-token prediction** — text is tokens; the model outputs a probability for
   every next token (classification over a vocabulary); training is
   self-supervised (the answer is the next word in the text).
4. **★ Text generation** — a **real tiny next-token model** (trigram+bigram blend
   built live from a robot-themed corpus) with a **temperature** slider. Watch the
   probability bars reshape and a sentence build word by word (autoregression).
5. **Transformer in one line** — attention lets each token look back at the others;
   an attention sketch. (Deliberately minimal, per the brief.)
6. **★ ACT — the robot's brain** — ResNet vision + joint numbers → a **Transformer**
   → a **chunk of future motor targets**. The key contrast: GPT **classifies** the
   next token (cross-entropy); ACT **regresses** the next motions (L1). Training
   data = your own teleop recordings. A **Mock-ACT** demo "sees" a cube, predicts a
   chunk of 6-motor action vectors (shown as a live grid), and executes them.
7. **The whole course, connected** — Ch1 motors → Ch2 wiring → Ch3 calibration →
   record → Ch5 learning → Ch6 ACT — plus a quiz and homework.

## Accuracy notes
- **ACT = Action Chunking Transformer** (ResNet image encoder + Transformer,
  predicts a chunk of continuous actions), matching lerobot's `policies/act`
  (`modeling_act.py`): the training loss is **L1** (`F.l1_loss`), and the output is
  `(batch, chunk_size, action_dim)` continuous actions — **not** discrete tokens.
- The lesson honours the "motor digits" idea but makes the one correction that
  matters: ACT outputs **continuous numbers**, so it uses regression (L1), whereas
  text models classify a token (cross-entropy).
- The **Mock-ACT** demo is a clearly-labelled simplified stand-in (a scripted
  reach), not a trained network — used to visualize the input → action-chunk →
  motion loop. The **text generator is real** (a genuine small next-token model).

Verified in-browser: text generation works and temperature visibly sharpens
(top word 100% at low T) / flattens (37% at high T) the distribution; Mock-ACT
predicts and executes an 8-step chunk; no console errors.
