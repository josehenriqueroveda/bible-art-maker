from pydantic import BaseModel


class VerseResponse(BaseModel):
    book: str
    chapter: int
    start_verse: int
    end_verse: int | None = None
    response: str

    def __init__(self, **data):
        super().__init__(**data)
        self.book = self.book.title()
