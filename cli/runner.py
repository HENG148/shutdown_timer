from core.timer import ShutdownTimer
from core.platform import PLATFORM
from utils.history import load_history

def run_cli(args):
  seconds = int(args.minutes * 60)
  timer = ShutdownTimer(
    seconds=seconds,
    action=args.action,
    on_tick=lambda r: print(
      f"[{args.action.upper()}] in"
      f"{r // 3600:02d}:{(r % 3600) // 60:02d} : { r % 60:02d}"
      f"(Ctrl + C to cancel)",
      end="\r",
      flush=True
    ),
    on_done=lambda: print(f"\n Time's up! Executing: {args.action}"),
  )
  print(f"\n Shutdown Timer v2.0 - { PLATFORM.upper()}")
  print(f"  Action : {args.action}")
  print(f"  In     : {args.minutes} minute(s)\n")
  
  try:
    timer.start()
    timer._thread.join()
  except KeyboardInterrupt:
    timer.cancel()
    print("\n  Cancelled. Have a good session!")
    
  if args.history:
    show_history_cli()
    
def show_history_cli():
  history = load_history()
  if not history:
    print("\n No history found.")
    return
  print("\n ---- Recent Runs -------------------------")
  for h in reversed(history[-10:]):
    status = "completed" if h.get("completed") else "Cancelled"
    mins = h["duration_seconds"] // 60
    print(f" {h["started_at"][:16]} { mins}min {h["action"]} { status}")