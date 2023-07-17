from slowapi import Limiter
from slowapi.util import get_remote_address

LIMITER = Limiter(key_func=get_remote_address, default_limits=["1440 per day", "60 per hour"])
API_IP = "127.0.0.1"

BOOKS_FILE = "db/nvi.json"
BACKGROUND_IMAGE = "assets/background.jpg"
TEXT_COLOR = (255, 255, 255)  # White
MAX_LINES_PER_IMAGE = 4
LINE_SPACING = 10