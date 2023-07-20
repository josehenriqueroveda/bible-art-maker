import logging
import textwrap

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from PIL import Image, ImageDraw, ImageFont

from models.VerseRequest import VerseRequest
from models.Bible import Bible
from helpers.constants import (
    BOOKS_DIR,
    BACKGROUND_IMAGE,
    TEXT_COLOR,
    LINE_SPACING,
    LIMITER,
)

logger = logging.getLogger(__name__)

art_maker_router = APIRouter()


def generate_verse_images(verse_request: VerseRequest) -> None:
    bible = Bible(f"{BOOKS_DIR}{verse_request.version}.json")
    verse_text = bible.get_text(verse_request)
    if verse_text is None:
        logger.error("Invalid book, chapter, or verse range.")
        return

    if verse_request.end_verse is None:
        verse_info = f"{verse_request.book} {verse_request.chapter}:{verse_request.start_verse} ({verse_request.version.upper()})"
        image_path = f"assets/{verse_request.book}_{verse_request.chapter}_{verse_request.start_verse}.jpg"
    else:
        verse_info = f"{verse_request.book} {verse_request.chapter}:{verse_request.start_verse}-{verse_request.end_verse} ({verse_request.version.upper()})"
        image_path = f"assets/{verse_request.book}_{verse_request.chapter}_{verse_request.start_verse}-{verse_request.end_verse}.jpg"

    font_text = ImageFont.truetype("arialbd.ttf", 40)
    font_info = ImageFont.truetype("arial.ttf", 32)

    image = Image.open(BACKGROUND_IMAGE)
    W, H = image.size
    draw = ImageDraw.Draw(image)

    wrapper = textwrap.TextWrapper(width=50)
    lines = wrapper.wrap(text=verse_text)
    verse_text = "\n".join(lines)

    border_color = (0, 0, 0)
    border_width = 3

    _, _, w1, h1 = draw.multiline_textbbox(
        (0, 0), verse_text, font=font_text, spacing=LINE_SPACING
    )
    draw.text(
        ((W - w1) / 2, (H - h1) / 2),
        verse_text,
        font=font_text,
        fill=TEXT_COLOR,
        spacing=LINE_SPACING,
        stroke_width=border_width,
        stroke_fill=border_color,
    )

    _, _, w2, h2 = draw.multiline_textbbox((0, 0), verse_info, font=font_info)
    draw.text(
        ((W - w2) / 2, (H - h2) / 2 + h1 + 50),
        verse_info,
        font=font_info,
        fill=TEXT_COLOR,
        stroke_width=2,
        stroke_fill=border_color,
    )

    image.save(image_path)

    logger.info("Image generation completed.")


@art_maker_router.post("/image/verse", tags=["Image"])
@LIMITER.limit("1/min")
async def art_maker(verse_request: VerseRequest, request: Request):
    """
    Generates an image with the requested Bible verse and returns a JSON response with a message indicating
    that the image generation has been completed.

    Args:
        verse_request (VerseRequest): The request object containing the book, chapter, and verse range.

    Returns:
        JSONResponse: A JSON response with a message indicating that the image generation has been completed.
    """
    generate_verse_images(verse_request)
    return JSONResponse(
        status_code=200, content={"message": "Image generation completed."}
    )
