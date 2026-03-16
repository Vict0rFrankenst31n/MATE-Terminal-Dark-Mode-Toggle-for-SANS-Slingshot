# MATE Terminal Dark Mode Toggle for SANS Slingshot

**Quickly switch MATE Terminal to a proper dark theme (black background + white text)  
and toggle back to your previous settings — with one command.**

This small Python script is especially useful in the **SANS Slingshot** Linux distribution (used in many SANS Institute penetration testing and cyber defense courses), where the default MATE Terminal profile is typically light-themed — making long hours of terminal work much harder on the eyes.

As of late 2024 / early 2025, newer Slingshot releases include an official dark mode option in MATE Terminal — but many students and instructors still run older images or prefer a reliable one-click toggle that remembers and restores their original palette.

## Features

- Toggles between **dark mode** (pure black background + white foreground) and your previous settings
- Remembers whether you were using system theme colors or custom colors
- Automatically backs up your current profile settings (`~/.config/mate-terminal-toggle.json`)
- Supports non-default profiles via `--profile <name>`
- Handles both `rgb(…)` and 16-bit hex color formats used by different MATE versions
- Very lightweight — no extra dependencies beyond standard Python 3 + `gsettings`

## Why this exists

SANS course participants (FOR508, SEC560, SEC504, PEN-200 / OSCP-style work, etc.) often spend many hours staring at terminals during labs.  
The default light background in older Slingshot VMs causes significant eye strain — especially in low-light hotel rooms or late-night studying sessions.

This script gives you instant dark mode without manually navigating Edit → Profiles → Colors every time.

## Requirements

- **MATE Desktop Environment** (default in SANS Slingshot)
- `gsettings` command (comes with MATE / GLib)
- Python 3.6+

**Tested on:**
- SANS Slingshot (various versions)
- Ubuntu MATE
- Linux Mint MATE

## Installation

### Option 1: Quick one-liner (recommended)

```bash
wget https://raw.githubusercontent.com/Vict0rFrankenst31n/MATE-Terminal-Dark-Mode-Toggle-for-SANS-Slingshot/main/mate-terminal-dark.py -O ~/bin/mate-terminal-dark
chmod +x ~/bin/mate-terminal-dark
```
After this, you can run it from anywhere simply as:
```bash
mate-terminal-dark
```
Note: If ~/bin is not in your $PATH, add it with:
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
# or restart your terminal
```
Option 2: Clone the full repository
```bash
git clone https://github.com/Vict0rFrankenst31n/MATE-Terminal-Dark-Mode-Toggle-for-SANS-Slingshot.git
cd MATE-Terminal-Dark-Mode-Toggle-for-SANS-Slingshot
```
Then run directly:
```bash
python3 mate-terminal-dark.py
```
Or move/symlink for convenience:
```bash
mv mate-terminal-dark.py ~/bin/mate-terminal-dark
chmod +x ~/bin/mate-terminal-dark
# or create symlink:
# ln -s "$(pwd)/mate-terminal-dark.py" ~/bin/mate-terminal-dark
```
Usage
```bash
# Toggle dark mode on/off (uses the 'default' profile)
mate-terminal-dark

# Or using the full script name
python3 mate-terminal-dark.py

# Specify a different profile
mate-terminal-dark --profile CustomProfile
mate-terminal-dark --profile=Work
```
First run → switches to dark mode and saves your current settings
Second run → restores your previous colors

Important:
After running the script, open a new terminal tab or window — existing ones usually do not refresh the palette automatically.
Example output
```text
✔ MATE Terminal profile 'default' switched to dark mode.
 Open a NEW tab/window to ensure colors refresh.
```
or
```text
✔ Restored previous settings for profile 'default'.
 Open a NEW tab/window to ensure colors refresh.
```
How it decides which direction to toggle

If the current background is already very dark (heuristic: perceived brightness < ~60), it assumes you're already in dark mode → restores previous settings
Otherwise → saves current settings and applies dark mode

## Limitations / Notes

-Only changes background and foreground colors (does not modify the 16-color ANSI palette)

-Forces simple black + white for maximum readability — does not attempt to guess or apply "pretty" color schemes

-If no backup exists when restoring, falls back to use-theme-colors=true

-Color detection is intentionally conservative — may rarely misclassify very exotic color schemes

## Contributing
Feel free to open issues or pull requests!
Popular requested improvements:

-Support for changing the 16-color palette

-Automatic detection/listing of all available profiles

-Desktop entry / keyboard shortcut integration

-Explicit toggle flags (--dark / --light)
