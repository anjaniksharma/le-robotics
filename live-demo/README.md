# Live Motor Control 🎛️ — drive a real STS3215 from the browser

An interactive demo where sliders in a web page move a **real** Feetech STS3215
servo (the motor in the LeRobot SO-101). The on-screen rotor mirrors the motor's
**actual encoder**, so students can watch the motor *chase* the target — a live
picture of **closed-loop control**.

```
   Browser  ──HTTP──▶  motor_bridge.py  ──USB / serial──▶  STS3215 motor
   (dial &              (feetech-servo-sdk)                 (real motion)
    sliders)   ◀──────  reads Present_Position  ◀──────────  (encoder)
```

## Why a small Python "bridge"?
A web page can't open a USB serial port on its own (safely). So a tiny local
Python program holds the port and exposes a few `localhost` commands the page
calls. Bonus: it reuses the exact `feetech-servo-sdk` that came with
`lerobot[feetech]` in Chapter 2 — no new installs.

## Run it (2 steps)

From the **project root** (`~/Documents/robotics`), with your venv active:

```bash
source .venv/bin/activate
python le-robotics/live-demo/motor_bridge.py
```

Then open the URL it prints:  **http://localhost:8777**

> Open the `http://localhost:8777` URL the server prints — **not** the
> `index.html` file directly. The page needs to talk to the bridge, and the
> bridge serves the page for you.

### Options
```bash
python le-robotics/live-demo/motor_bridge.py --port /dev/tty.usbmodemXXXX  # pick a port
python le-robotics/live-demo/motor_bridge.py --baud 1000000                # baud rate
python le-robotics/live-demo/motor_bridge.py --sim                         # no hardware
python le-robotics/live-demo/motor_bridge.py --http-port 9000              # different web port
```

## No motor? No problem — Simulation mode
If nothing answers on the serial bus, the bridge automatically runs a
**simulated** motor that eases toward your target. The web page shows an amber
**“Simulation mode”** badge. Plug a motor in, click **Connect**, and the badge
turns green (**“● Live hardware”**) — same page, now driving real hardware.

## Wiring a single motor for the demo
1. Connect one STS3215 to the Feetech **bus servo adapter** board.
2. Plug the adapter into the Mac with a **USB-C data cable**.
3. Plug the adapter's **DC power** in (the motor gets its muscle from here, not USB).
4. In the page: click **⟳ Ports**, pick the `/dev/tty.usbmodem…` port, **Connect**.
5. Detected motors (IDs that answer a ping) light up green in the **Motor** row.

> New motors ship as **ID 1**. To use IDs 1–6 on one bus, run
> `lerobot-setup-motors` first (see Chapter 2).

## What the controls do
| Control | Effect | Register |
| --- | --- | --- |
| **Dial / Target slider** | Sets goal angle (0–4095 counts = 0–360°) | `Goal_Position` (42) |
| **Torque switch** | Motor holds position (on) or goes limp (off) | `Torque_Enable` (40) |
| **Speed** | How fast it drives to the goal | `Goal_Speed` (46) |
| **Acceleration** | How gently it ramps up | `Acceleration` (41) |
| **Actual readout** | Live encoder position, polled ~10×/sec | `Present_Position` (56) |

**Teaching moment:** turn **Torque off**, move the motor by hand, and watch the
*Actual* readout still change — the encoder never stops sensing. Turn it back on
and the motor snaps to your target. That sense-compare-correct loop is exactly
what makes a servo a "servo."

## Safety
- Keep fingers/hair clear of the gears when torque is on.
- Start with a **single** motor and low speed while learning.
- If the arm behaves oddly, quit the bridge (`Ctrl+C`) — the motors hold their
  last position but stop taking commands.

## Two web pages, one bridge
The same `motor_bridge.py` serves both pages — pick from the URL it prints:

| URL | Page | What it does |
| --- | --- | --- |
| `http://localhost:8777/` | **Live Motor Control** | One dial drives **one** STS3215; live encoder readback. Great first contact. |
| `http://localhost:8777/arm.html` | **SO-101 Digital Twin** 🦾 | A **3D replica** of the whole arm with **six joint dials**. Move a dial → the real arm copies it. Flip to **Mirror** mode, turn torque off, pose the physical arm by hand, and the on-screen twin follows. |

### About the Digital Twin (`arm.html`)
- Built with pure **CSS 3D transforms** — a real articulated kinematic chain, no
  external libraries, fully offline. Drag to orbit, scroll to zoom.
- Joint dials use the **real SO-ARM101 URDF ranges** (shoulder_pan ±110°,
  shoulder_lift ±100°, elbow_flex ±97°, wrist_flex ±95°, wrist_roll −157…163°,
  gripper 0–100%).
- **"0°" = the pose the arm is in when you connect** (captured via `read_all`), or
  when you press **🏠 Set current pose as 0°** — so commands are relative and safe.
- **Drive mode** sends all six goals with one `/api/move_batch`; the twin then
  renders from the *actual* positions polled back, so it shows the real robot.
- **Mirror mode** reads the arm ~14×/sec and moves the dials + twin to match.

## Files
- `motor_bridge.py` — the local server (stdlib HTTP + `feetech-servo-sdk`).
- `index.html` — single-motor control panel.
- `arm.html` — the 3D SO-101 Digital Twin (six-joint control).

### API (for the curious)
`GET /api/status·/api/ports·/api/read?id=·/api/read_all?ids=1,2,3` ·
`POST /api/connect·/api/move·/api/move_batch·/api/torque`

Verified in **simulation** on macOS (Apple Silicon), Python 3.12.7,
`feetech-servo-sdk` from `lerobot[feetech]` 0.6.2. Register map from lerobot's
`STS_SMS_SERIES_CONTROL_TABLE`.
