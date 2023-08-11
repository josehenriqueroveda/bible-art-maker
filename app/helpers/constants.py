from slowapi import Limiter
from slowapi.util import get_remote_address

LIMITER = Limiter(
    key_func=get_remote_address, default_limits=["1440 per day", "60 per hour"]
)
API_IP = "127.0.0.1"

BOOKS_DIR = "db/"

BACKGROUND_IMAGE_DIR = f"assets/landscape"
BACKGROUND_IMAGE_MOBILE_DIR = f"assets/portrait"
TEXT_COLOR = (255, 255, 255)  # White
MAX_LINES_PER_IMAGE = 4
LINE_SPACING = 10
