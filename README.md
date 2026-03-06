# Tidbyt Author Clock

A [Tidbyt](https://tidbyt.com) app that displays the current time as a literary quote — inspired by the [Literary Clock](https://github.com/JohannesNE/literature-clock) project.

![preview](final_preview.gif)

## How it works

Every minute, the display shows a quote from a novel that mentions the current time. The time phrase is highlighted in gold, surrounded by context (white before, grey after), with the author scrolling along the bottom.

If no quote exists for a given minute, the time is shown numerically as a fallback.

**Coverage**: 1399 of 1440 minutes (97%) have at least one literary quote.

## File structure

```
tidbyt-author-clock/
  prepare_data.py       # One-time script: downloads CSV and generates the app
  app/
    author_clock.star   # Generated Tidbyt app (do not edit manually)
    author_clock.webp   # Rendered preview
  final_preview.gif     # Animated preview
  hello_world.star      # Pixlet tutorial artifact
```

## Setup

### 1. Install pixlet

Follow the [pixlet install guide](https://tidbyt.dev/docs/build/installing-pixlet).

### 2. Generate the app

Downloads the source CSV and bundles all quote data directly into the Starlark app file:

```bash
python3 prepare_data.py
```

This writes `app/author_clock.star` (~540 KB). Re-run whenever you want to refresh the dataset.

### 3. Run locally

```bash
pixlet serve app/author_clock.star
```

Open [http://localhost:8080](http://localhost:8080) to preview.

To simulate the clock updating every minute, run this in a second PowerShell terminal:

```powershell
while ($true) { (Get-Item "$HOME\tidbyt-author-clock\app\author_clock.star").LastWriteTime = Get-Date; Start-Sleep 15 }
```

### 4. Push to device

```bash
pixlet render app/author_clock.star
pixlet push --installation-id author-clock app/author_clock.webp
```

## Data source

Quotes from [`litclock_annotated.csv`](https://raw.githubusercontent.com/JohannesNE/literature-clock/master/litclock_annotated.csv) by Johannes Nørgaard Erichsen. Only `sfw` and `unknown`-rated quotes are included; `nsfw` quotes are excluded.

## Display details

- **Canvas**: 64×32 pixels
- **Font**: `CG-pixel-3x5-mono`
- **Layout**: vertical scrolling quote (25px) + horizontal scrolling author (6px)
- **Scroll speed**: 150ms/frame
- **Colors**: white (before) · gold (time phrase) · grey (after) · dim grey (author)
