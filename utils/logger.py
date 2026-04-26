import sys 
import logging
from pathlib import Path

LOG_DIR = Path.home() / ".shutdown_timer"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "shutdown_timer.log"

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s",
  handlers=[
    logging.FileHandler(LOG_FILE),
    logging.StreamHandler(sys.stdout),
  ]
)

logger = logging.getLogger(__name__)