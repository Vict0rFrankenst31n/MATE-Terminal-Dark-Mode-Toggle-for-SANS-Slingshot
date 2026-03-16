#!/usr/bin/env python3
"""
mate_terminal_toggle_dark.py
Toggle MATE Terminal dark mode on/off and remember your previous settings.

Default profile path: /org/mate/terminal/profiles/default/
Stores a backup here: ~/.config/mate-terminal-toggle.json
Usage:
  python3 mate_terminal_toggle_dark.py
  python3 mate_terminal_toggle_dark.py --profile Custom
"""
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
CONFIG_PATH = Path.home() / ".config" / "mate-terminal-toggle.json"
def run(cmd: str) -> subprocess.CompletedProcess:
    # This line previously had non-breaking spaces (U+00A0) for indentation.
    # They have been replaced with standard ASCII spaces (U+0020).
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)
def gs_get(schema_path: str, key: str) -> str:
    # Returns the raw string without surrounding quotes
    cmd = f"gsettings get {schema_path} {shlex.quote(key)}"
    p = run(cmd)
    if p.returncode != 0:
        raise RuntimeError(f"gsettings get error: {p.stderr.strip() or p.stdout.strip()}")
    val = p.stdout.strip()
    # Drop leading/trailing single quotes if present
    if len(val) >= 2 and ((val[0] == "'" and val[-1] == "'") or (val[0] == '"' and val[-1] == '"')):
        val = val[1:-1]
    return val
def gs_set(schema_path: str, key: str, value: str) -> None:
    # If value contains spaces or special chars, wrap in single quotes
    if not (value.startswith("'") and value.endswith("'")) and any(c.isspace() for c in value):
        value = f"'{value}'"
    cmd = f"gsettings set {schema_path} {shlex.quote(key)} {value}"
    p = run(cmd)
    if p.returncode != 0:
        raise RuntimeError(f"gsettings set error: {p.stderr.strip() or p.stdout.strip()}")
def load_backup() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return {}
def save_backup(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))
def detect_schema_path(profile_name: str) -> str:
    # MATE Terminal profile schema path format:
    # org.mate.terminal.profile:/org/mate/terminal/profiles/<ProfileName>/
    base = f"/org/mate/terminal/profiles/{profile_name}/"
    return f"org.mate.terminal.profile:{base}"
def is_dark_color(value: str) -> bool:
    """
    Very light heuristic to detect if a color is 'dark':
    - Handles 'rgb(r,g,b)' form
    - Handles 16-bit per channel hex '#rrrrggggbbbb' (MATE sometimes uses this)
    """
    v = value.strip().lower()
    if v.startswith("rgb(") and v.endswith(")"):
        try:
            r, g, b = (int(x) for x in v[4:-1].split(","))
            # Perceived brightness (simple) — tweak threshold if needed
            brightness = 0.2126*r + 0.7152*g + 0.0722*b
            return brightness < 60 # black/very dark
        except Exception:
            return False
    if v.startswith("#") and len(v) == 13:
        # 16-bit per channel: #rrrrggggbbbb -> map to 0..255
        try:
            r = int(v[1:5], 16) // 257
            g = int(v[5:9], 16) // 257
            b = int(v[9:13], 16) // 257
            brightness = 0.2126*r + 0.7152*g + 0.0722*b
            return brightness < 60
        except Exception:
            return False
    return False
def to_hex16(rgb: tuple[int, int, int]) -> str:
    # Convert (0..255) to 16-bit per channel hex string expected by some MATE builds
    r, g, b = rgb
    return f"#{r*257:04x}{g*257:04x}{b*257:04x}"
def set_dark(schema_path: str) -> None:
    # Ensure terminal isn’t inheriting theme colors, then set black bg / white fg
    gs_set(schema_path, "use-theme-colors", "false")
    # Try rgb(...) first; if it fails on some setups, follow-up with hex16
    try:
        gs_set(schema_path, "background-color", "rgb(0,0,0)")
        gs_set(schema_path, "foreground-color", "rgb(255,255,255)")
    except RuntimeError:
        gs_set(schema_path, "background-color", f"'{to_hex16((0,0,0))}'")
        gs_set(schema_path, "foreground-color", f"'{to_hex16((255,255,255))}'")
def restore_previous(schema_path: str, backup: dict, profile_name: str) -> bool:
    key = f"profile:{profile_name}"
    if key not in backup:
        return False
    prev = backup[key]
    if "use_theme_colors" in prev:
        gs_set(schema_path, "use-theme-colors", "true" if prev["use_theme_colors"] else "false")
    if not prev.get("use_theme_colors", False):
        # Only restore explicit colors when we weren weren’t using theme colors before
        if "background_color" in prev:
            gs_set(schema_path, "background-color", f"'{prev['background_color']}'")
        if "foreground_color" in prev:
            gs_set(schema_path, "foreground-color", f"'{prev['foreground_color']}'")
    return True
def main():
    # Parse optional --profile argument
    profile = "default"
    for i, arg in enumerate(sys.argv[1:], start=1):
        if arg == "--profile" and i+1 <= len(sys.argv)-1:
            profile = sys.argv[i+1]
            break
        if arg.startswith("--profile="):
            profile = arg.split("=", 1)[1]
            break
    schema_path = detect_schema_path(profile)
    # Read current state
    try:
        use_theme = gs_get(schema_path, "use-theme-colors") # 'true' or 'false'
    except RuntimeError as e:
        print(f"Error: {e}\nTip: If your profile name isn’t 'default', run with --profile <Name>")
        sys.exit(1)
    # If we're using theme colors, we can't directly know the actual colors, but we can remember that fact.
    fg = bg = None
    if use_theme.strip().lower() == "false":
        try:
            bg = gs_get(schema_path, "background-color")
            fg = gs_get(schema_path, "foreground-color")
        except RuntimeError:
            pass
    # Load backup
    backup = load_backup()
    key = f"profile:{profile}"
    # Decide direction: if current background looks dark (or we’re already on a black bg), go back; else go dark
    going_dark = True
    if use_theme.strip().lower() == "false" and bg and is_dark_color(bg):
        going_dark = False
    if going_dark:
        # Save current settings before switching to dark
        backup[key] = {
            "use_theme_colors": (use_theme.strip().lower() == "true")
        }
        if bg is not None:
            backup[key]["background_color"] = bg
        if fg is not None:
            backup[key]["foreground_color"] = fg
        save_backup(backup)
        set_dark(schema_path)
        print(f"✔ MATE Terminal profile '{profile}' switched to dark mode.")
        print(" Open a NEW tab/window to ensure colors refresh.")
    else:
        restored = restore_previous(schema_path, backup, profile)
        if restored:
            print(f"✔ Restored previous settings for profile '{profile}'.")
            print(" Open a NEW tab/window to ensure colors refresh.")
        else:
            # No backup found — best effort: re-enable theme colors
            gs_set(schema_path, "use-theme-colors", "true")
            print(f"ℹ No saved backup found. Enabled theme colors for profile '{profile}'.")
if __name__ == "__main__":
    main()
