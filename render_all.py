"""
render_all.py — render a webp for every minute of the day using pixlet.
Output: renders/HH_MM.webp (1440 files)
Run: python3 render_all.py
"""
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_DIR = "renders"
STAR_FILE = "app/author_clock.star"
WORKERS = 8

os.makedirs(OUTPUT_DIR, exist_ok=True)

def render(hour, minute):
    time_str = f"{hour:02d}:{minute:02d}"
    key = f"{hour:02d}_{minute:02d}"
    out = os.path.join(OUTPUT_DIR, f"{key}.webp")
    result = subprocess.run(
        ["pixlet", "render", STAR_FILE, f"time={time_str}", "-o", out],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return key, False, result.stderr.strip()
    return key, True, None

minutes = [(h, m) for h in range(24) for m in range(60)]

print(f"Rendering {len(minutes)} frames with {WORKERS} workers...")
failed = []

with ThreadPoolExecutor(max_workers=WORKERS) as pool:
    futures = {pool.submit(render, h, m): (h, m) for h, m in minutes}
    done = 0
    for future in as_completed(futures):
        key, ok, err = future.result()
        done += 1
        if not ok:
            failed.append((key, err))
        if done % 100 == 0 or done == len(minutes):
            print(f"  {done}/{len(minutes)} done...")

print(f"\nDone! {len(minutes) - len(failed)} succeeded, {len(failed)} failed.")
if failed:
    for key, err in failed:
        print(f"  FAILED {key}: {err}")
