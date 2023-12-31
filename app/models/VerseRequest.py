from pydantic import BaseModel
from pydantic import validator


class VerseRequest(BaseModel):
    mobile: bool | None = None
    version: str = "nvi"
    book: str
    chapter: int
    start_verse: int
    end_verse: int | None = None

    def __init__(self, **data):
        super().__init__(**data)
        self.version = self.version.lower()
        self.book = self.book.title()
        if self.mobile is None:
            self.mobile = False

    @validator("end_verse", pre=True)
    def set_end_verse(cls, value, values):
        if value is None:
            return values["start_verse"]
        if value < values["start_verse"]:
            raise ValueError("end_verse must be greater than or equal to start_verse")
        return value
