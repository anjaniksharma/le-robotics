#!/usr/bin/env python3
"""
motor_bridge.py — a tiny local server that lets the browser drive a real
Feetech STS3215 bus servo (the motor used in the LeRobot SO-101).

How it fits the course:
    Browser  ──HTTP──▶  this Python bridge  ──USB/serial──▶  STS3215 motor
    (sliders)           (feetech-servo-sdk)                  (real motion)

It reuses the `feetech-servo-sdk` that came with `lerobot[feetech]`, so no new
packages are needed. If no motor is connected, it automatically runs in
SIMULATION mode so the web page still works.

Run it from the project root, inside your venv:

    source .venv/bin/activate
    python le-robotics/live-demo/motor_bridge.py          # auto-detect port
    python le-robotics/live-demo/motor_bridge.py --port /dev/tty.usbmodemXXXX
    python le-robotics/live-demo/motor_bridge.py --sim    # force simulation

Then open the page it prints, e.g.  http://localhost:8777
"""

import argparse
import glob
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# ---- STS3215 / SMS-STS control-table registers (from lerobot feetech tables) ----
ADDR_TORQUE_ENABLE = 40   # 1 byte
ADDR_ACCELERATION = 41    # 1 byte
ADDR_GOAL_POSITION = 42   # 2 bytes (0..4095 = one full turn)
ADDR_GOAL_SPEED = 46      # 2 bytes (0 = max)
ADDR_PRESENT_POSITION = 56  # 2 bytes
RESOLUTION = 4096         # 12-bit magnetic encoder → counts per revolution
STS_PROTOCOL_END = 0      # STS/SMS series use protocol_end = 0

HERE = Path(__file__).resolve().parent


class MotorBackend:
    """Talks to the real motor if possible, otherwise simulates one."""

    def __init__(self, baud=1_000_000):
        self.baud = baud
        self.lock = threading.Lock()
        self.sim = True
        self.port_name = None
        self.ids = []                      # motor ids that responded to a ping
        self.port = None
        self.packet = None
        # simulation state (per id): live position eases toward the goal
        self.sim_pos = {}
        self.sim_goal = {}
        self.sim_torque = {}
        self.sim_speed = {}
        for i in range(1, 7):
            self.sim_pos[i] = RESOLUTION // 2
            self.sim_goal[i] = RESOLUTION // 2
            self.sim_torque[i] = False
            self.sim_speed[i] = 600
        # background thread animates the simulated motor smoothly
        self._stop = False
        threading.Thread(target=self._sim_loop, daemon=True).start()

    # ---------- port discovery ----------
    @staticmethod
    def list_ports():
        pats = ["/dev/tty.usbmodem*", "/dev/tty.usbserial*",
                "/dev/ttyACM*", "/dev/ttyUSB*", "/dev/cu.usbmodem*", "/dev/cu.usbserial*"]
        found = []
        for p in pats:
            found.extend(glob.glob(p))
        return sorted(set(found))

    # ---------- connect ----------
    def connect(self, port=None, baud=None):
        """Try to open the real serial port and ping motors 1..6.
        Falls back to simulation on any failure."""
        if baud:
            self.baud = int(baud)
        self.disconnect()
        try:
            import scservo_sdk as scs
        except Exception as e:  # sdk missing → sim
            self.sim = True
            self.port_name = "(feetech-servo-sdk not found)"
            return self.status()

        candidates = [port] if port else self.list_ports()
        for cand in candidates:
            if not cand:
                continue
            try:
                ph = scs.PortHandler(cand)
                if not ph.openPort():
                    continue
                if not ph.setBaudRate(self.baud):
                    ph.closePort()
                    continue
                pk = scs.PacketHandler(STS_PROTOCOL_END)
                ids = []
                for mid in range(1, 7):
                    _, comm, err = pk.ping(ph, mid)
                    if comm == scs.COMM_SUCCESS and err == 0:
                        ids.append(mid)
                if ids:
                    self.port, self.packet, self.scs = ph, pk, scs
                    self.ids = ids
                    self.port_name = cand
                    self.sim = False
                    return self.status()
                ph.closePort()
            except Exception:
                continue
        # nothing answered → simulation
        self.sim = True
        self.ids = [1, 2, 3, 4, 5, 6]
        self.port_name = "simulation"
        return self.status()

    def disconnect(self):
        try:
            if self.port is not None:
                self.port.closePort()
        except Exception:
            pass
        self.port = self.packet = None

    # ---------- commands ----------
    def set_torque(self, mid, on):
        mid = int(mid)
        if self.sim:
            self.sim_torque[mid] = bool(on)
            return {"ok": True}
        with self.lock:
            self.packet.write1ByteTxRx(self.port, mid, ADDR_TORQUE_ENABLE, 1 if on else 0)
        return {"ok": True}

    def move(self, mid, pos, speed=None, accel=None):
        mid = int(mid)
        pos = max(0, min(RESOLUTION - 1, int(pos)))
        if self.sim:
            self.sim_goal[mid] = pos
            self.sim_torque[mid] = True
            if speed is not None:
                self.sim_speed[mid] = int(speed)
            return {"ok": True, "pos": pos}
        with self.lock:
            if accel is not None:
                self.packet.write1ByteTxRx(self.port, mid, ADDR_ACCELERATION, max(0, min(255, int(accel))))
            if speed is not None:
                self.packet.write2ByteTxRx(self.port, mid, ADDR_GOAL_SPEED, max(0, min(3000, int(speed))))
            self.packet.write2ByteTxRx(self.port, mid, ADDR_GOAL_POSITION, pos)
        return {"ok": True, "pos": pos}

    def read(self, mid):
        mid = int(mid)
        if self.sim:
            pos = int(round(self.sim_pos.get(mid, 0)))
        else:
            with self.lock:
                val, comm, err = self.packet.read2ByteTxRx(self.port, mid, ADDR_PRESENT_POSITION)
            pos = (val % RESOLUTION) if comm == self.scs.COMM_SUCCESS else -1
        deg = round(pos * 360.0 / RESOLUTION, 1) if pos >= 0 else None
        return {"id": mid, "pos": pos, "deg": deg}

    def status(self):
        return {
            "connected": True,
            "sim": self.sim,
            "port": self.port_name,
            "baud": self.baud,
            "ids": self.ids,
            "resolution": RESOLUTION,
        }

    # ---------- simulation animation ----------
    def _sim_loop(self):
        dt = 0.02
        while not self._stop:
            for i in range(1, 7):
                if not self.sim_torque.get(i):
                    continue
                cur = self.sim_pos[i]
                goal = self.sim_goal[i]
                # step scaled by "speed" (counts per second-ish)
                max_step = max(20, self.sim_speed.get(i, 600) * dt * 6)
                d = goal - cur
                if abs(d) <= max_step:
                    self.sim_pos[i] = goal
                else:
                    self.sim_pos[i] = cur + max_step * (1 if d > 0 else -1)
            time.sleep(dt)


BACKEND = MotorBackend()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, obj, code=200, ctype="application/json"):
        body = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(b"", code=204, ctype="text/plain")

    def _body(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return {}

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            f = HERE / "index.html"
            if f.exists():
                self._send(f.read_bytes(), ctype="text/html; charset=utf-8")
            else:
                self._send({"error": "index.html not found"}, 404)
            return
        if u.path == "/favicon.ico":
            self._send(b"", code=204, ctype="image/x-icon"); return
        if u.path == "/api/status":
            self._send(BACKEND.status()); return
        if u.path == "/api/ports":
            self._send({"ports": BACKEND.list_ports()}); return
        if u.path == "/api/read":
            q = parse_qs(u.query)
            mid = int(q.get("id", ["1"])[0])
            self._send(BACKEND.read(mid)); return
        self._send({"error": "not found"}, 404)

    def do_POST(self):
        u = urlparse(self.path)
        b = self._body()
        try:
            if u.path == "/api/connect":
                self._send(BACKEND.connect(b.get("port"), b.get("baud"))); return
            if u.path == "/api/move":
                self._send(BACKEND.move(b["id"], b["pos"], b.get("speed"), b.get("accel"))); return
            if u.path == "/api/torque":
                self._send(BACKEND.set_torque(b["id"], b.get("on", True))); return
        except Exception as e:
            self._send({"ok": False, "error": str(e)}, 500); return
        self._send({"error": "not found"}, 404)


def main():
    ap = argparse.ArgumentParser(description="Browser → STS3215 motor bridge")
    ap.add_argument("--port", help="serial port (default: auto-detect)")
    ap.add_argument("--baud", type=int, default=1_000_000)
    ap.add_argument("--http-port", type=int, default=8777)
    ap.add_argument("--sim", action="store_true", help="force simulation mode")
    args = ap.parse_args()

    BACKEND.baud = args.baud
    if args.sim:
        BACKEND.sim = True
        BACKEND.ids = [1, 2, 3, 4, 5, 6]
        BACKEND.port_name = "simulation (forced)"
    else:
        BACKEND.connect(args.port, args.baud)

    st = BACKEND.status()
    mode = "SIMULATION" if st["sim"] else f"LIVE hardware on {st['port']}"
    print("=" * 60)
    print(f"  Motor bridge running in {mode}")
    if not st["sim"]:
        print(f"  Motors detected: {st['ids']}  @ {st['baud']} baud")
    else:
        print("  No motor detected — plug one in and click Connect, or")
        print("  just play in simulation. (Ping checks IDs 1-6.)")
    print(f"\n  ▶ Open in your browser:  http://localhost:{args.http_port}")
    print("  Press Ctrl+C to stop.")
    print("=" * 60)

    srv = ThreadingHTTPServer(("127.0.0.1", args.http_port), Handler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping…")
        BACKEND.disconnect()


if __name__ == "__main__":
    main()
