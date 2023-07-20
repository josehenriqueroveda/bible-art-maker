import logging
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from models.VerseRequest import VerseRequest
from models.VerseResponse import VerseResponse
from models.Bible import Bible
from helpers.constants import BOOKS_DIR, LIMITER

logger = logging.getLogger(__name__)

bible_router = APIRouter()


@bible_router.get("/bible/books", response_model=List[str], tags=["bible"])
@LIMITER.limit("60/minute")
async def get_books(request: Request):
    """
    Retrieves a list of all books in the Bible.

    Returns:
        List[str]: A list of all books in the Bible.
    """
    bible = Bible(f"{BOOKS_DIR}nvi.json")
    books = bible.get_books()
    logger.info("Books retrieved successfully.")
    return books


@bible_router.post("/bible/verse", response_model=VerseResponse, tags=["Bible"])
@LIMITER.limit("60/minute")
async def get_verse(verse_request: VerseRequest, request: Request) -> VerseResponse:
    """
    Retrieves the text of a specific verse or range of verses from the Bible.

    Args:
        verse_request (VerseRequest): The request object containing the book, chapter, and verse range.
        request (Request): The FastAPI request object.

    Returns:
        VerseResponse: The response object containing the requested verse(s) text.
    """
    bible = Bible(f"{BOOKS_DIR}{verse_request.version}.json")
    text = bible.get_text(verse_request)
    if text is None:
        logger.error("Invalid book, chapter, or verse range.")
        return VerseResponse(
            book=verse_request.book,
            chapter=verse_request.chapter,
            start_verse=verse_request.start_verse,
            end_verse=verse_request.end_verse,
            response="Invalid book, chapter, or verse range.",
        )

    logger.info("Verse retrieved successfully.")
    verse_response = VerseResponse(
        version=verse_request.version,
        book=verse_request.book,
        chapter=verse_request.chapter,
        start_verse=verse_request.start_verse,
        end_verse=verse_request.end_verse,
        response=text,
    )
    logger.info(verse_response)
    return verse_response
