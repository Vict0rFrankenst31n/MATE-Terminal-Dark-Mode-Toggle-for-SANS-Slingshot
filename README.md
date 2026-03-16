# MATE Terminal Dark Mode Toggle for SANS Slingshot

**Quickly switch MATE Terminal to a proper dark theme (black background + white text) and toggle back to your previous settings.**

This small Python script is especially useful in the **SANS Slingshot** Linux distribution (used in many SANS Institute penetration testing and cyber defense courses), where the default MATE Terminal profile is typically light-themed — making long hours of terminal work harder on the eyes.

As of late 2024 / early 2025, newer Slingshot releases include an official dark mode option in MATE Terminal — but many students and instructors still run older images or prefer a reliable one-click toggle that remembers your original palette.

## Features

- Toggles between **dark mode** (pure black background + white foreground) and your previous settings
- Remembers whether you were using system theme colors or custom colors
- Backs up your current profile settings automatically (`~/.config/mate-terminal-toggle.json`)
- Supports non-default profiles via `--profile <name>`
- Handles both `rgb(…)` and 16-bit hex color formats used by different MATE versions
- Very lightweight — no extra dependencies beyond standard Python 3 + `gsettings`

## Why this exists

Many SANS course participants spend hours staring at terminals during labs (FOR508, SEC560, SEC504, PEN-200 / OSCP-style work, etc.).  
The default light background in older Slingshot VMs causes eye strain, especially in low-light hotel rooms or late-night studying.

This script gives you instant dark mode without manually digging through Edit → Profiles → Colors every time.

## Requirements

- **MATE Desktop Environment** (default in SANS Slingshot)
- `gsettings` command (comes with MATE / GLib)
- Python 3.6+

Tested on:
- SANS Slingshot (various versions)
- Ubuntu MATE
- Linux Mint MATE

## Installation

```bash
# Option 1: Quick one-liner (recommended)
wget https://raw.githubusercontent.com/yourusername/mate-terminal-toggle-dark/main/mate_terminal_toggle_dark.py -O ~/bin/mate-terminal-dark
chmod +x ~/bin/mate-terminal-dark

# Option 2: Clone the repo
git clone https://github.com/yourusername/mate-terminal-toggle-dark.git
cd mate-terminal-toggle-dark
# Optionally move or symlink the script to ~/bin or /usr/local/bin
