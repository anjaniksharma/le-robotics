#!/usr/bin/env python3
"""
list_motors.py — scan a Feetech bus and print which motor IDs are present.

Read-only (just pings), safe to run any time the port is free. Reuses the
feetech-servo-sdk from lerobot[feetech].

    python le-robotics/live-demo/list_motors.py                       # default port below
    python le-robotics/live-demo/list_motors.py /dev/tty.usbmodemXXXX
"""
import sys
import scservo_sdk as scs

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/tty.usbmodem5B7B0096781"
BAUDS = [1_000_000, 500_000, 250_000, 128_000, 115_200, 57_600, 38_400]
STS_END = 0  # STS/SMS series
SO101 = {1: "shoulder_pan", 2: "shoulder_lift", 3: "elbow_flex",
         4: "wrist_flex", 5: "wrist_roll", 6: "gripper"}

ph = scs.PortHandler(PORT)
if not ph.openPort():
    print(f"❌ Could not open {PORT} — is the arm plugged in and the port free?")
    sys.exit(1)

pk = scs.PacketHandler(STS_END)
print(f"Scanning {PORT} …\n")
hit_baud = None
for baud in BAUDS:
    ph.setBaudRate(baud)
    found = []
    for mid in range(0, 21):            # IDs 0..20 (factory default is 1)
        model, comm, err = pk.ping(ph, mid)
        if comm == scs.COMM_SUCCESS:
            found.append((mid, model))
    if found:
        hit_baud = baud
        print(f"✅ Found {len(found)} motor(s) at {baud:,} baud:\n")
        print(f"   {'ID':>3}  {'MODEL':>6}  JOINT (SO-101 layout)")
        print(f"   {'--':>3}  {'-----':>6}  --------------------")
        for mid, model in found:
            print(f"   {mid:>3}  {model:>6}  {SO101.get(mid, '(id not in 1-6 — unexpected)')}")
        ids = sorted(m for m, _ in found)
        missing = [i for i in (1, 2, 3, 4, 5, 6) if i not in ids]
        print()
        if ids == [1, 2, 3, 4, 5, 6]:
            print("   🎉 All six IDs 1-6 present — the arm is fully configured.")
        elif missing:
            print(f"   ⚠️  Missing expected IDs: {missing} (not answering / not set).")
        break

ph.closePort()
if hit_baud is None:
    print("❌ No motors answered at any baud.\n"
          "   • Check the DC power and the USB data cable.\n"
          "   • Make sure nothing else (a bridge/teleop) is holding the port.\n"
          "   • Confirm the port with: lerobot-find-port")
