import logging
import textwrap

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from PIL import Image, ImageDraw, ImageFont

from models.VerseRequest import VerseRequest
from models.Bible import Bible
from helpers.constants import (
    BOOKS_FILE,
    BACKGROUND_IMAGE,
    TEXT_COLOR,
    MAX_LINES_PER_IMAGE,
    LINE_SPACING,
    LIMITER,
)

logger = logging.getLogger(__name__)

art_maker_router = APIRouter()


def generate_verse_images(verse_request: VerseRequest) -> None:
    bible = Bible(BOOKS_FILE)
    verse_text = bible.get_text(verse_request)
    if verse_text is None:
        logger.error("Invalid book, chapter, or verse range.")
        return

    verse_info = f"{verse_request.book} {verse_request.chapter}:{verse_request.start_verse}-{verse_request.end_verse}"
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

    image_path = f"assets/{verse_request.book}_{verse_request.chapter}_{verse_request.start_verse}-{verse_request.end_verse}.jpg"
    image.save(image_path)

    logger.info("Image generation completed.")


@art_maker_router.post("/art_maker")
@LIMITER.limit("1/min")
async def art_maker(
    verse_request: VerseRequest, request: Request, response: JSONResponse
):
    generate_verse_images(verse_request)
    return JSONResponse(
        status_code=200, content={"message": "Image generation completed."}
    )
