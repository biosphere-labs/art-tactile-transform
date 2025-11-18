# Non-Technical Run Guide

This walkthrough explains how to start the app, what to tweak, and what those tweaks do—without assuming any coding background.

## Before You Start
- **Computer:** Windows, macOS, or Linux.
- **Need a browser:** Chrome, Edge, Safari, or Firefox.
- **Choose one setup:** Either the simple launcher (recommended) or the manual install.

## Option A: Easiest One-Click Launch
1. Open the project folder.
2. Double-click `launch.bat` (Windows) or run `launch.sh` (macOS/Linux) from a terminal.
3. Wait until your browser opens to the app page (usually `http://localhost:7860`).
4. If the page does not open automatically, type `http://localhost:7860` into your browser.

**What this does:** Starts a ready-made container with everything configured, then opens the web app.

## Option B: Manual Install (no Docker)
1. Install Python 3.13+ and the **UV** package manager.
2. Open a terminal in the project folder.
3. Run `uv sync` to fetch everything the app needs.
4. Run `uv run art-tactile-gui` to start the app.
5. Open `http://localhost:7860` in your browser if it does not open automatically.

**What this does:** Installs the app on your machine and starts the same web interface without using Docker.

## Using the App (Plain Language)
1. **Upload a portrait photo** by dragging it onto the page.
2. **Adjust the sliders**:
   - **Size/Depth sliders:** Change how big and thick the tactile print will feel.
   - **Smoothness slider:** Softens rough areas; higher values = smoother touch.
   - **Detail sliders (Subject, Features, Edges):** Make the main face and important lines stand taller. Lower them to flatten details.
   - **Background slider:** Push the background down so the subject stands out. Lower values = flatter background.
3. **Preview the 3D model** by dragging to rotate it—this shows the exact shape you will print.
4. **Click “Download STL”** to save the print-ready file.

## Quick Fixes if Something Looks Off
- **Details feel too sharp or spiky:** Increase Smoothness slightly.
- **Face is too flat:** Raise Subject or Feature sliders.
- **Background competes with the subject:** Lower the Background slider.
- **Model looks blocky:** Increase Resolution, but note it may take a bit longer to process.

## Planning to Embed an STL Viewer Here
We plan to add a built-in STL viewer so you can spin the model directly inside the page without downloading it first. This will let you:
- Inspect the printable surface more closely before exporting.
- Share quick previews without extra software.

_No action is needed from you right now; the current preview will still show the relief shape until the STL viewer ships._
