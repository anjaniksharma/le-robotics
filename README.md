# 🤖 LeRobot SO-101 — An Interactive Robotics Course

A hands-on, browser-based course that teaches how the **LeRobot SO-101** robot arm
works — from the motors in its joints all the way to the neural network that lets it
act on its own. Built for a curious **9th-grade** student: every chapter is a
self-contained interactive HTML page (animations, dials, live simulations) that runs
offline — just open `index.html`.

## The chapters

| # | Chapter | What you'll learn | Open |
|---|---------|-------------------|------|
| 1 | **The Muscles of a Robot** | STS3215 servos, torque, gear ratio, degrees of freedom; a driveable 6-motor arm | [chapter-01](chapter-01/index.html) |
| 2 | **Waking Up the Robot** | Python virtual env, installing LeRobot on a Mac, USB/serial wiring & ports | [chapter-02](chapter-02/index.html) |
| 3 | **Calibration** | Teaching both arms their center & range so leader and follower share one language | [chapter-03](chapter-03/index.html) |
| 4 | **How Machines Learn** | Neurons, loss, gradient descent, backprop — and a **real neural net you train live** | [chapter-04](chapter-04/index.html) |
| 5 | **From Words to Motion** | Text generation (next-token) → **ACT**, the robot's brain that predicts motions | [chapter-05](chapter-05/index.html) |
| 6 | **Collecting Good Data** | Cameras, resolution, fps, encoding, lighting & episodes; a live good-vs-bad data auditor | [chapter-06](chapter-06/index.html) |
| 7 | **Training & Running** | The loss curve, checkpoints, cloud training (Colab / HF Jobs), and deploying ACT on the arm | [chapter-07](chapter-07/index.html) |

## Live hardware demos (`live-demo/`)
Drive a **real STS3215 motor** — or a simulated one if none is plugged in — straight
from the browser. A tiny local Python bridge reuses the `feetech-servo-sdk` from
`lerobot[feetech]`.

```bash
source .venv/bin/activate
python le-robotics/live-demo/motor_bridge.py
# then open the printed URL
```
- `http://localhost:8777/` — **Live Motor Control** (one dial → one motor, live encoder readback)
- `http://localhost:8777/arm.html` — **SO-101 Digital Twin** (3D arm, six joint dials, drive or mirror the real arm)

See [live-demo/README.md](live-demo/README.md) for wiring and safety.

## The through-line
The course connects end to end: the **calibrated encoders** from Chapter 3 become the
**input numbers** to ACT (Chapter 5); your **teleoperation recordings** become its
**training data**; the **gradient descent** from Chapter 4 tunes its weights; and the
**motor targets** it outputs are the same 0–4095 counts you send by hand in the
Digital Twin. 🔗

## Setup
- Python **3.12** virtual environment at the project root (`.venv`), with
  `lerobot[feetech]` installed. See Chapter 2 for the full, verified steps.
- Everything else is plain HTML/CSS/JS — no build step, no internet needed.

## Credits & sources
Motor/arm photos: Feetech / Hugging Face LeRobot. Specs, commands, calibration steps,
joint ranges, and the ACT description come from the open-source
[lerobot](https://github.com/huggingface/lerobot) project and the
[SO-ARM101](https://github.com/TheRobotStudio/SO-ARM100) hardware repo.
