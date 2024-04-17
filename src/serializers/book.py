from src.models.book import BookOut


def to_book_out(db_book) -> BookOut:
    return BookOut(
        _id=str(db_book["_id"]), 
        title=db_book["title"], 
        author=db_book["author"], 
        description=db_book["description"]
    )


def to_books_out(db_books: list) -> list[BookOut]:
    return [to_book_out(b) for b in db_books]
