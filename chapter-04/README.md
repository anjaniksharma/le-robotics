# Chapter 4 — Program it or Teach it? 🤔

An interactive HTML lesson that builds intuition for **why** robotics uses AI at all,
by contrasting learning with the other ways to control a robot — and landing on
"right tool for the job." Sits right before the learning chapters.

## How to use it
Open **`index.html`** in any browser. Self-contained, no internet needed.
Scroll or use **↓ / ↑**; the dots on the right jump between sections.

## What it teaches
1. **Two ways to give a robot a brain** — *program it* (write exact rules) vs.
   *teach it* (show examples / AI).
2. **The ladder of robot brains** — an interactive spectrum: playback → rules &
   sensors → classical control (IK/PID) → learning; click each rung for how it
   decides, when it shines, and when it breaks, with real robot examples.
3. **★ Playback vs. Learned** — two arms taught to grab a cube in the center; move
   the cube and run both: the **playback** arm blindly repeats and grabs empty air,
   the **learned** arm finds the cube. (Mirrors LeRobot's real `lerobot-replay` vs
   `lerobot-rollout`.)
4. **The wall rules hit** — why hand-writing rules explodes in the messy real world
   (any position, lighting, soft objects, perception from pixels); an interactive
   "rules pile up" counter.
5. **★ "Program it or Teach it?" sorter** — a decision game: pick the smarter
   approach for real tasks and get the reasoning; teaches the pattern.
6. **The honest answer** — a comparison table (rules/control are often *better*:
   cheaper, 100% reliable, explainable) → AI is for messy tasks → the SO-101's tasks
   *are* messy → so we go AI. Bridges into Chapter 5.
7. **Recap + quiz + homework.**

## Framing
Deliberately **"right tool for the job,"** not "AI good, rules bad." Kids learn that
engineers pick the simplest method that works, and climb toward learning only when a
task is too messy for rules — which the SO-101's tasks are.

## Accuracy notes
`lerobot-replay` (playback of a recording) and `lerobot-rollout` (run a trained
policy) are real LeRobot CLIs; classical control (inverse kinematics, PID) is the
SO-101's low-level control (Chapter 1). All scenes are **synthetic illustrations**.

Verified in-browser: the ladder, the playback-vs-learned demo (playback misses when
the cube moves, learned adapts), the rules-pile-up counter, and the sorter all work;
no console errors.
