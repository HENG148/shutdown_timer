import time
import threading
from datetime import datetime

from utils.logger import logger
from utils.history import save_history
from core.platform import execute_action

class ShutdownTimer:
  """
    Countdown timer that runs in a background thread.
    Callbacks:
      on_tick(remaining)  — called every second with remaining seconds
      on_done()           — called when the timer reaches zero
      on_c
  """
  
  def __init__(
    self,
    seconds: int, 
    action: str = "shutdown",
    on_tick=None,
    on_done=None,
    on_cancel=None,
  ):
    self.total_seconds = seconds
    self.remaining = seconds
    self.action = action
    self.on_tick = on_tick
    self.on_done = self.on_done
    self.on_cancel = on_cancel
    self._stop_event = threading.Event()
    self._thread = None
    self.started_at = None
    self.cancelled = False
    
  def start(self):
    """Start the countdown in a background daemon thread."""
    self.started_at = datetime.now()
    logger.info(
      f"Timer started: {self.total_seconds}s → action={self.action}"
    )
    self._thread = threading.Thread(target=self._run, daemon=True)
    self._thread.start()
 
    def cancel(self):
      """Cancel the running timer."""
      self.cancelled = True
      self._stop_event.set()
      logger.info("Timer cancelled by user.")
      if self.on_cancel:
        self.on_cancel()
 
    def _run(self):
      """Internal thread loop."""
      while self.remaining > 0 and not self._stop_event.is_set():
        if self.on_tick:
          self.on_tick(self.remaining)
          time.sleep(1)
          self.remaining -= 1
 
        if not self.cancelled:
          logger.info(f"Timer expired. Triggering: {self.action}")
          if self.on_done:
            self.on_done()
            save_history({
              "started_at": self.started_at.isoformat(),
              "duration_seconds": self.total_seconds,
              "action": self.action,
              "completed": True,
            })
            execute_action(self.action)
        else:
          save_history({
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "duration_seconds": self.total_seconds,
            "action": self.action,
            "completed": False,
            "cancelled_at_remaining": self.remaining,
          })