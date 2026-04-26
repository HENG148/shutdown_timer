# Shutdown Timer Pro

A professional-grade shutdown scheduler with both GUI and CLI modes.

## Features

- **GUI Mode** — Tkinter-based dark interface with live countdown, progress bar, and history
- **CLI Mode** — Headless terminal mode with live countdown display
- **4 Actions** — Shutdown, Restart, Sleep, Hibernate
- **Quick Presets** — 15, 30, 60, 90, 120 minute presets
- **Run History** — Logs last 50 runs to `~/.shutdown_timer/history.json`
- **Cross-Platform** — Windows, macOS, Linux
- **Graceful Cancel** — Cancel anytime via button (GUI) or Ctrl+C (CLI)
- **Logging** — Full logs saved to `~/.shutdown_timer/shutdown_timer.log`

## Requirements

- Python 3.7+
- Tkinter (usually included with Python; install with `sudo apt install python3-tk` on Linux)

## Usage

### GUI (default)
```bash
python shutdown_timer.py
```

### CLI — 60 minute shutdown
```bash
python shutdown_timer.py --cli --minutes 60
```

### CLI — 30 minute restart
```bash
python shutdown_timer.py --cli --minutes 30 --action restart
```

### CLI — View history
```bash
python shutdown_timer.py --cli --history
```

## Notes

- On macOS/Linux, shutdown/restart require `sudo` privileges.
- Sleep and hibernate use `systemctl` on Linux (no sudo needed).
- History is stored at `~/.shutdown_timer/history.json`.
