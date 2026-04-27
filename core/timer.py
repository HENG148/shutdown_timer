import time
import threading
from datetime import datetime

from utils.logger import logger
from utils.history import save_history
from core.platform import execute_action

class ShutdownTimer:

    def __init__(self, seconds, action="shutdown", on_tick=None, on_done=None, on_cancel=None):
        self.total_seconds = int(seconds)
        self.remaining = int(seconds)
        self.action = action
        self.cb_tick = on_tick
        self.cb_done = on_done
        self.cb_cancel = on_cancel
        self._stop_event = threading.Event()
        self._thread = None
        self.started_at = None
        self.cancelled = False

    def start(self):
        self.started_at = datetime.now()
        logger.info(f"Timer started: {self.total_seconds}s action={self.action}")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def cancel(self):
        self.cancelled = True
        self._stop_event.set()
        logger.info("Timer cancelled.")
        if self.cb_cancel:
            self.cb_cancel()

    def _run(self):
        while self.remaining > 0 and not self._stop_event.is_set():
            if self.cb_tick:
                self.cb_tick(self.remaining)
            time.sleep(1)
            self.remaining -= 1

        if not self.cancelled:
            logger.info(f"Timer expired. Triggering: {self.action}")
            if self.cb_done:
                self.cb_done()
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