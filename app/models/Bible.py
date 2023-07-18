import json

from models.VerseRequest import VerseRequest


class Bible:
    def __init__(self, books_file):
        with open(books_file, "r", encoding="utf-8-sig") as file:
            self.bible_data = json.load(file)

    def get_books(self):
        return [data["name"] for data in self.bible_data]

    def get_text(self, verse_request: VerseRequest):
        book_data = next(
            (data for data in self.bible_data if data["name"] == verse_request.book),
            None,
        )
        if book_data is None:
            return None

        chapter_data = book_data["chapters"][verse_request.chapter - 1]
        if chapter_data is None:
            return None

        if verse_request.end_verse is None:
            verse_range = [verse_request.start_verse]
        else:
            verse_range = list(
                range(verse_request.start_verse, verse_request.end_verse + 1)
            )

        text = []
        for verse in verse_range:
            if verse <= len(chapter_data):
                verse_text = chapter_data[verse - 1]
                text.append(verse_text)

        return " ".join(text)
