# Chapter 3 — Calibration: Teaching Both Arms Where They Are 🎯

An interactive HTML lesson on **calibrating** the SO-101 leader and follower arms
so they share the same reference and can work together (teleoperation, training).

## How to use it
Open **`index.html`** in any browser. Self-contained, no internet needed.
Scroll or use **↓ / ↑**; the dots on the right jump between sections.

## What it teaches
1. **Why calibrate** — raw encoder counts (0–4095) are arbitrary per arm; two arms
   must be "tuned to the same pitch" before a command means the same pose on each.
2. **The four numbers** calibration records per motor: `homing_offset`,
   `range_min`, `range_max`, `drive_mode`.
3. **Step 1 — Set the center (half-turn homing):** move joints to the middle,
   press Enter → `homing_offset = present − 2048`, so the middle reads 0°.
   *(Interactive: set a center, watch the calibrated angle stay honest.)*
4. **Step 2 — Record the range:** torque off, sweep each joint stop-to-stop; the
   live `NAME | MIN | POS | MAX` table fills in. *(Interactive: sweep to unlock
   Finish, see raw counts map to −100…100.)*
5. **Both arms** — same process, different flags: follower `--robot.*`, leader
   `--teleop.*`. Animated terminal walks through a full run.
6. **Where it's saved** — a JSON per arm, keyed by `id`, reused automatically.
7. **The payoff** — a teleop mirror: move the leader's elbow, the follower copies.

## The real commands
```bash
# Follower (robot)
lerobot-calibrate --robot.type=so101_follower \
  --robot.port=/dev/tty.usbmodemXXXX --robot.id=my_follower_arm

# Leader (teleoperator)
lerobot-calibrate --teleop.type=so101_leader \
  --teleop.port=/dev/tty.usbmodemYYYY --teleop.id=my_leader_arm
```
Calibration is written to
`~/.cache/huggingface/lerobot/calibration/{robots,teleoperators}/<type>/<id>.json`
and loaded automatically by later `lerobot-teleoperate` / `lerobot-record` runs.

## Ties to the rest of the course
- Uses the **ports** found in Chapter 2 (`lerobot-find-port`).
- Assumes motor **IDs** were set with `lerobot-setup-motors` (Chapter 2).
- The **Digital Twin** (`live-demo/arm.html`) "Set current pose as 0°" button is a
  hands-on version of the homing step.

## Sources
Calibration steps, commands, and file paths are from the open-source
[lerobot](https://github.com/huggingface/lerobot) project (`motors_bus.py`,
`feetech/feetech.py`, `so101.mdx`, `utils/constants.py`).
