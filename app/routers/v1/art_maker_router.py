import os
import random
import logging
import textwrap

from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image, ImageDraw, ImageFont

from models.VerseRequest import VerseRequest
from models.Bible import Bible
from helpers.constants import (
    BOOKS_DIR,
    BACKGROUND_IMAGE_DIR,
    BACKGROUND_IMAGE_MOBILE_DIR,
    TEXT_COLOR,
    LINE_SPACING,
    LIMITER,
)

logger = logging.getLogger(__name__)

art_maker_router = APIRouter()


def generate_verse_images(verse_request: VerseRequest) -> str | None:
    bible = Bible(f"{BOOKS_DIR}{verse_request.version}.json")
    verse_text = bible.get_text(verse_request)
    if verse_text is None:
        logger.error("Invalid book, chapter, or verse range.")
        return

    if verse_request.end_verse is None:
        verse_info = f"{verse_request.book} {verse_request.chapter}:{verse_request.start_verse} ({verse_request.version.upper()})"
        image_path = f"temp/{verse_request.book}_{verse_request.chapter}_{verse_request.start_verse}.jpg"
    else:
        verse_info = f"{verse_request.book} {verse_request.chapter}:{verse_request.start_verse}-{verse_request.end_verse} ({verse_request.version.upper()})"
        image_path = f"temp/{verse_request.book}_{verse_request.chapter}_{verse_request.start_verse}-{verse_request.end_verse}.jpg"

    if verse_request.mobile:
        path = f"{BACKGROUND_IMAGE_MOBILE_DIR}/{random.randint(1, 4)}.jpg"
        image = Image.open(path)
        wrapper_width = 30
        font_size_verse = 28
        font_size_info = 22
        border_width = 2
    else:
        path = f"{BACKGROUND_IMAGE_DIR}/{random.randint(1, 4)}.jpg"
        image = Image.open(path)
        wrapper_width = 50
        font_size_verse = 40
        font_size_info = 32
        border_width = 3

    font_text = ImageFont.truetype("arialbd.ttf", font_size_verse)
    font_info = ImageFont.truetype("arial.ttf", font_size_info)
    W, H = image.size
    draw = ImageDraw.Draw(image)

    wrapper = textwrap.TextWrapper(width=wrapper_width)
    lines = wrapper.wrap(text=verse_text)
    verse_text = "\n".join(lines)

    border_color = (0, 0, 0)

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
        align="center",
    )

    _, _, w2, h2 = draw.multiline_textbbox((0, 0), verse_info, font=font_info)
    draw.text(
        ((W - w2) / 2, (H - h2) / 2 + h1 + 50),
        verse_info,
        font=font_info,
        fill=TEXT_COLOR,
        stroke_width=2,
        stroke_fill=border_color,
        align="center",
    )

    image.save(image_path)
    logger.info("Image generation completed.")

    return image_path


@art_maker_router.post("/image/verse", tags=["Image"])
@LIMITER.limit("1/min")
async def art_maker(
    verse_request: VerseRequest, request: Request, background_tasks: BackgroundTasks
):
    """
    Generates an image with the requested Bible verse.

    Args:
        verse_request (VerseRequest): The request object containing the book, chapter, and verse range.

    Returns:
        FileResponse: The image file.
    """
    image_path = generate_verse_images(verse_request)
    if image_path is None:
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid book, chapter, or verse range."},
        )

    def delete_image():
        try:
            os.remove(image_path)
        except OSError:
            pass

    background_tasks.add_task(delete_image)

    return FileResponse(
        image_path, media_type="image/jpeg", filename=os.path.basename(image_path)
    )
