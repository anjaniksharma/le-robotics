# Chapter 1 — The Muscles of a Robot 🤖

An interactive HTML lesson for a 9th-grade student, covering the motors behind the
**LeRobot SO-101** arm.

## How to use it
Just open **`index.html`** in any web browser (double-click it). No internet needed —
all images and code are self-contained in this folder.

- Scroll, or use the **↓ / ↑ arrow keys**, to move through the 9 sections.
- The dots on the right jump to any section.

## What it teaches
1. **The STS3215 motor** — what a smart serial-bus servo is and what's inside it.
2. **The motor family** — DC, hobby servo, stepper, brushless, and how they differ.
3. **Torque** 💪 — twisting strength, with a drag-the-load dial.
4. **Gear ratio** ⚙️ — trading speed for strength, with spinning gears.
5. **Degrees of freedom** — build up a robot arm one joint at a time.
6. **SO-101 map** — the 6 motors, their IDs, and what each joint does.
7. **Play!** — drive a live SO-101 simulator with 6 sliders (with real joint ranges).
8. **Recap + quiz + homework.**

## Interactive bits to try
- Torque dial: make the load too heavy and watch the motor "stall."
- Gear slider: see torque go up as speed goes down.
- Arm simulator: pose the arm and watch the **encoder count (0–4095)** update.

## Files
- `index.html` — the whole lesson (HTML + CSS + JS in one file).
- `assets/sts3215_motor.jpg` — real photo of the Feetech STS3215 servo.
- `assets/so101_follower.webp` / `so101_leader.webp` — real photos of the SO-101 arms.

## Sources
Motor numbering and gearing come from the open-source
[lerobot](https://github.com/huggingface/lerobot) project (`so_follower.py`, `so101.mdx`)
and Feetech STS3215 datasheets. Joint angle ranges are illustrative — every real arm is
fine-tuned during **calibration**.
