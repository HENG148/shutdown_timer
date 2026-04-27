import sys
import os 
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

def parse_args():
  parser = argparse.ArgumentParser(
    description="Advanced Shutdown Timer — CLI & GUI",
    formatter_class=argparse.RawTextHelpFormatter,
  )
  parser.add_argument("--cli", action="store_true", help="Run in headless CLI mode (no GUI)")
  parser.add_argument("--minutes", type=float, default=60, help="Duration in minutes (CLI mode, default: 60)")
  parser.add_argument(
    "--action",
    choices=["shutdown", "restart", "sleep", "hibernate"],
    default="shutdown",
    help="Action to perform when timer expires (default: shutdown)",
  )
  parser.add_argument("--history", action="store_true", help="Show run history after timer (CLI mode)")
  return parser.parse_args()

if __name__ == "__main__":
  args =parse_args()
  if args.cli:
    from cli.eeee import run_cli
    run_cli(args)
  else:
    from gui.app import run_gui
    run_gui()