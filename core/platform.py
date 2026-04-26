import sys
import subprocess
from utils.logger import logger


def get_platform() -> str:
  """Detect and return the current OS as a string."""
  if sys.platform.startswith("win"):
    return "windows"
  elif sys.platform.startswith("darwin"):
    return "macos"
  else:
    return "linux"

PLATFORM = get_platform()

SHUTDOWN_COMMANDS = {
  "windows": {
    "shutdown":  ["shutdown", "/s", "/t", "0"],
    "restart":   ["shutdown", "/r", "/t", "0"],
    "hibernate": ["shutdown", "/h"],
    "sleep":     ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
    "cancel":    ["shutdown", "/a"],
  },
  "macos": {
    "shutdown":  ["sudo", "shutdown", "-h", "now"],
    "restart":   ["sudo", "shutdown", "-r", "now"],
    "hibernate": ["pmset", "sleepnow"],
    "sleep":     ["pmset", "sleepnow"],
    "cancel":    None,
  },
  "linux": {
    "shutdown":  ["sudo", "shutdown", "-h", "now"],
    "restart":   ["sudo", "shutdown", "-r", "now"],
    "hibernate": ["systemctl", "hibernate"],
    "sleep":     ["systemctl", "suspend"],
    "cancel":    ["sudo", "shutdown", "-c"],
  },
}

def execute_action(action: str):
  """Execute a shutdown/sleep/restart action based on current platform."""
  cmd = SHUTDOWN_COMMANDS[PLATFORM].get(action)
  if not cmd:
    logger.warning(f"Action '{action}' not supported on {PLATFORM}.")
    return
  logger.info(f"Executing: {action} → {' '.join(cmd)}")
  try:
    subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    logger.error(f"Command failed: {e}")
  except FileNotFoundError:
    logger.error(f"Command not found: {cmd[0]}")