# Chapter 7 — Collecting Good Data 📷

An interactive HTML lesson on how to record demonstrations for the SO-101 so the
ACT policy (Chapter 6) can actually learn: cameras, resolution, fps, image
encoding, lighting/scene setup, episodes, the dataset format, and — the
centerpiece — a hands-on **good-vs-bad data auditor**.

## How to use it
Open **`index.html`** in any browser. Self-contained, no internet needed.
Scroll or use **↓ / ↑**; the dots on the right jump between sections.

## What it teaches
1. **Garbage in, garbage out** — ACT imitates you, so it copies your data's flaws.
2. **One frame** = a synchronized snapshot: `observation.images.<cam>`,
   `observation.state` (6 joints), `action` (6 targets), `timestamp`, `task`.
3. **Cameras: position & resolution** — a fixed front/top view + a wrist cam;
   keep it still and identical at deploy; default `640×480`. Interactive camera
   sim with an occlusion toggle (arm hides the cube from the front cam → wrist cam
   still sees it) and a resolution/pixelation slider.
4. **Frames per second** — `fps=30` default; the loop must keep up or frames drop.
   Interactive fps sampler (choppy vs smooth); `frames = fps × seconds`.
5. **Image encoding** — frames stored as compressed **MP4 video** (not raw), ~10–100×
   smaller. Interactive dataset-size estimator (cameras × resolution × episodes).
6. **Lighting, background & object** — the consistency ↔ variety balance: hold the
   camera/lighting/background steady; vary the object position and approach.
7. **Episodes** — same home start, tight `episode_time_s`, `reset_time_s` between,
   many `num_episodes`. Interactive episode timeline + total-frames calculator.
8. **The recording session** — anatomy of the real `lerobot-record` command
   (`--robot.*` = follower, `--teleop.*` = leader, `--dataset.*` = what to save) with a
   flag/default/meaning table for each group; the terminal log of a session
   (`Recording episode 0` → `Reset the environment` → … → `Stop recording`); the key
   controls (`n`/→ next, `r`/← re-record, `q`/Esc save-and-quit, Ctrl+C = episode lost)
   and *when* an episode is actually written (only after its reset phase). Interactive
   10×-speed **session simulator** that mirrors the loop in `lerobot_record.py`.
9. **The dataset on disk** — the real v3 LeRobotDataset layout under
   `~/.cache/huggingface/lerobot/<repo_id>_<timestamp>/` (`meta/`, `data/chunk-*/`,
   `videos/observation.images.<cam>/chunk-*/`), several episodes per file. Interactive
   frame scrubber.
10. **Viewing the episodes** — find the session folder, count episodes from
    `meta/info.json`, open one in Rerun with
    `lerobot-dataset-viz --repo-id me/grab_cube_<timestamp> --episode-index 0`
    (camera panels + `observation.state`/`action` plots on one timeline), what to look
    for, and `lerobot-replay` to play it back on the arm.
11. **★ Data-quality auditor** — toggle seven recording factors (camera moved,
   flickering light, object always same spot, jerky demos, too few episodes,
   dropped frames, wrong label) → a predicted task-success gauge and the specific
   failure mode each one causes.
12. **A printable good-data checklist, the real `lerobot-record` command, quiz &
    homework.**

## Accuracy notes
Defaults and the dataset layout come from lerobot's `lerobot-record` /
`DatasetRecordConfig` (`fps=30`, `episode_time_s=60`, `reset_time_s=60`,
`num_episodes=50`, `video=True`, `push_to_hub=True`, time-stamped `repo_id` unless
`no_stamp`, `640×480` cameras) and `LeRobotDataset` v3
(`data/chunk-*/file-*.parquet` + `videos/<cam>/chunk-*/file-*.mp4` + `meta/`).
The session loop, key bindings and the "saved only after reset" rule were read from
`lerobot_record.py` / `keyboard_input.py` / `VideoEncodingManager` and checked against a
real session on the SO-101 (an early Ctrl+C left a folder holding only `meta/info.json`).
The camera dictionary needs a space after each colon (`type: opencv`); `type:opencv`
fails to parse. The predicted "success %" in
the auditor is **illustrative**, not measured, and all scenes are **synthetic**
drawings (there's no camera/dataset on this machine).

Verified in-browser: auditor 100% (all careful) → 3% (all careless) with per-factor
failure modes; fps/size/episode calculators correct; no console errors.
