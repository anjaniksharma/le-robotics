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
8. **The dataset on disk** — the real LeRobotDataset layout (`data/*.parquet`,
   `videos/observation.images.<cam>/*.mp4`, `meta/`). Interactive frame scrubber.
9. **★ Data-quality auditor** — toggle seven recording factors (camera moved,
   flickering light, object always same spot, jerky demos, too few episodes,
   dropped frames, wrong label) → a predicted task-success gauge and the specific
   failure mode each one causes.
10. **A printable good-data checklist, the real `lerobot-record` command, quiz &
    homework.**

## Accuracy notes
Defaults and the dataset layout come from lerobot's `lerobot-record` /
`DatasetRecordConfig` (`fps=30`, `episode_time_s=60`, `reset_time_s=60`,
`num_episodes=50`, `video=True`, `640×480` cameras) and `LeRobotDataset`
(`data/*.parquet` + `videos/*.mp4` + `meta/*.json`). The predicted "success %" in
the auditor is **illustrative**, not measured, and all scenes are **synthetic**
drawings (there's no camera/dataset on this machine).

Verified in-browser: auditor 100% (all careful) → 3% (all careless) with per-factor
failure modes; fps/size/episode calculators correct; no console errors.
