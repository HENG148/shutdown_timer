import json
from pathlib import Path
 
LOG_DIR = Path.home() / ".shutdown_timer"
LOG_DIR.mkdir(exist_ok=True)
HISTORY_FILE = LOG_DIR / "history.json"
 
def save_history(entry: dict):
  """Append a timer run to history (keeps last 50 entries)."""
  history = load_history()
  history.append(entry)
  history = history[-50:]
  with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=2)
 
def load_history() -> list:
  """Load run history from disk."""
  if HISTORY_FILE.exists():
    with open(HISTORY_FILE) as f:
      return json.load(f)
  return []