import logging
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from models.VerseRequest import VerseRequest
from models.VerseResponse import VerseResponse
from models.Bible import Bible
from helpers.constants import BOOKS_FILE, LIMITER

logger = logging.getLogger(__name__)

bible_router = APIRouter()


@bible_router.get("/bible/books", response_model=VerseResponse, tags=["bible"])
@LIMITER.limit("60/minute")
async def get_books(request: Request) -> List[str]:
    bible = Bible(BOOKS_FILE)
    books = bible.get_books()
    logger.info("Books retrieved successfully.")
    return books


@bible_router.post("/bible/verse", response_model=VerseResponse, tags=["bible"])
@LIMITER.limit("60/minute")
async def get_verse(verse_request: VerseRequest, request: Request) -> VerseResponse:
    bible = Bible(BOOKS_FILE)
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
        book=verse_request.book,
        chapter=verse_request.chapter,
        start_verse=verse_request.start_verse,
        end_verse=verse_request.end_verse,
        response=text,
    )
    logger.info(verse_response)
    return verse_response
