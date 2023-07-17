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
    font_text = ImageFont.truetype("arial.ttf", 32)
    font_info = ImageFont.truetype("arial.ttf", 24)

    image = Image.open(BACKGROUND_IMAGE)
    W, H = image.size
    draw = ImageDraw.Draw(image)

    wrapper = textwrap.TextWrapper(width=50)
    lines = wrapper.wrap(text=verse_text)
    verse_text = "\n".join(lines)

    border_color = (0, 0, 0)
    fill_color = (255, 255, 255)
    border_width = 1

    # Draw black border
    for x in range(-border_width, border_width + 1):
        for y in range(-border_width, border_width + 1):
            draw.text(
                (W / 2 + x, (H - 32) / 2 + y),
                verse_text,
                font=font_text,
                fill=border_color,
                spacing=LINE_SPACING,
            )

    # Draw white fill
    draw.text(
        (W / 2, (H - 32) / 2),
        verse_text,
        font=font_text,
        fill=fill_color,
        spacing=LINE_SPACING,
    )

    # _, _, w, h = draw.multiline_textbbox((0, 0), verse_text, font=font_text, spacing=LINE_SPACING)
    # draw.text((W/2, (H-h)/2), verse_text, font=font_text, fill=TEXT_COLOR, spacing=LINE_SPACING)

    _, _, w, h = draw.multiline_textbbox((0, 0), verse_info, font=font_info)
    draw.text(
        ((W - w) / 2, (H - h) / 2 + 200), verse_info, font=font_info, fill=TEXT_COLOR
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
