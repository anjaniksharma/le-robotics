# Chapter 2 — Waking Up the Robot 🐍🤖

An interactive HTML lesson for a 9th-grade student on setting up the **software**
side of the LeRobot SO-101: a Python virtual environment, installing the LeRobot
library on a Mac, and understanding how the kit's wiring connects to the code.

## How to use it
Open **`index.html`** in any web browser. Self-contained — no internet needed.
Scroll or use **↓ / ↑ arrow keys**; the dots on the right jump between sections.

## What it teaches
1. **What a virtual environment is** and why we use one (the "lunchbox" analogy).
2. **Why Python 3.12** — LeRobot requires ≥ 3.12; macOS ships an older 3.9 we avoid.
3. **Step-by-step setup** with real, copy-pasteable Terminal commands.
4. **The wiring** — an animated diagram tracing a command from Python → USB-C →
   bus servo adapter → TTL serial → the 6 daisy-chained STS3215 motors, plus the
   separate DC power supply.
5. **Finding the port** (`lerobot-find-port`) with a working simulator.
6. **The first three commands** (`setup-motors`, `calibrate`, `teleoperate`).
7. **Troubleshooting, recap, quiz, and homework.**

## The exact setup this lesson documents (verified on this Mac)
This Mac is Apple Silicon (arm64) with Python 3.12.7 available. The environment was
created at the **project root** (`~/Documents/robotics`, one level above this repo):

```bash
cd ~/Documents/robotics
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e "./lerobot[feetech]"
lerobot-info
```

**Verified result:**
- LeRobot **0.6.2**
- Python **3.12.7**, Platform macOS arm64
- PyTorch **2.11.0**, MPS (Apple GPU) **available ✅**
- Feetech servo SDK (`scservo_sdk`) working
- CLIs installed: `lerobot-find-port`, `lerobot-setup-motors`, `lerobot-calibrate`,
  `lerobot-teleoperate`, `lerobot-record`, …

> For recording datasets later, also run
> `brew install ffmpeg && pip install -e "./lerobot[feetech,core_scripts]"`.
> Not required just to move the motors.

## Sources
Commands and macOS port examples (`/dev/tty.usbmodem…`) come from the open-source
[lerobot](https://github.com/huggingface/lerobot) `installation.mdx` and `so101.mdx`
guides. Python version requirement (`>=3.12`) is from lerobot's `pyproject.toml`.
