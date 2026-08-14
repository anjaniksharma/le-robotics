# Chapter 5 — How Machines Learn 🧠

An interactive HTML lesson introducing deep-learning **training** from scratch for a
9th-grade student: neurons, weights, error/loss, gradient descent, and
backpropagation — building to a **real neural network you train live in the browser**.

## How to use it
Open **`index.html`** in any browser. Self-contained, no internet needed.
Scroll or use **↓ / ↑**; the dots on the right jump between sections.

## What it teaches
1. **The big idea** — a network is a *function with knobs*; training is the same
   5-step loop (data → guess → error → blame → nudge) for *every* model.
2. **The neuron** — weighted sum + activation: `y = f(w₁x₁ + w₂x₂ + b)`.
3. **Loss** — two flavors, both revisited in Chapter 6:
   distance/L1 `|ŷ−y|` (regression — what the robot uses) and
   surprise/cross-entropy `−log(p)` (classification — what text uses).
4. **Gradient descent** — slope points downhill; `w ← w − lr·slope`; the
   learning-rate trade-off (too big overshoots).
5. **Backpropagation** — the chain rule as "multiply the slopes along the path."
6. **Train a real network — live.**

## The interactive pieces (all real math, no libraries)
- **Perceptron playground** — turn the weight knobs to separate two clusters; the
  weights *are* the boundary line.
- **Loss meter** — drag a prediction toward a target; watch L1 & squared loss.
- **Gradient-descent ball** — press Step to roll downhill; crank the learning rate
  until it overshoots and flies out of the valley.
- **Backprop visual** — a real 1-2-1 net; each Train step nudges the weights and
  the loss drops toward 0.
- **★ Live-trained classifier** — a genuine 2-8-1 network running real
  gradient descent + backprop on **interlocking two-moons** data. With the hidden
  layer on it reaches **100%** (the boundary bends to fit); turn the hidden layer
  off and a single straight line **stalls near ~85–88%** — a hands-on proof of why
  depth matters.

## Notes on accuracy
The math shown (weighted sum, L1/squared/cross-entropy loss, the update rule, the
chain rule) is real and drives the demos. The L1 loss is highlighted deliberately
because it's exactly what the robot's **ACT** policy uses — the thread we pick up in
Chapter 6.

Verified in-browser: the live network converges (loss → ~0.006, accuracy → 100%
with a hidden layer; ~88% without), no console errors.
