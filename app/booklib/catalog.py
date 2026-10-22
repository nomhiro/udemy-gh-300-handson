"""蔵書の一覧と検索。"""
import csv
from pathlib import Path

from booklib.models import Book


class Catalog:
    def __init__(self) -> None:
        self._books: list[Book] = []

    def add_book(self, book: Book) -> None:
        if self.get(book.id) is not None:
            raise ValueError(f"蔵書 ID {book.id} はすでにあります")
        self._books.append(book)

    def get(self, book_id: int) -> Book | None:
        for book in self._books:
            if book.id == book_id:
                return book
        return None

    def all_books(self) -> list[Book]:
        return list(self._books)

    def find_by_title(self, title: str) -> list[Book]:
        # 大文字と小文字を区別せず、書名の部分一致で探す
        title = title.casefold()
        return [book for book in self._books if title in book.title.casefold()]

    def search(self, keywords: list[str]) -> list[Book]:
        # 書名・著者・タグのどれかにキーワードを含む本を探す
        results = []
        for keyword in keywords:
            for book in self._books:
                if keyword in book.title or keyword in book.author or keyword in book.tags:
                    if book not in results:
                        results.append(book)
        return results


def load_catalog(path: str | Path) -> Catalog:
    """CSV（id,title,author,isbn,published,tags）から蔵書を読み込む。"""
    catalog = Catalog()
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            catalog.add_book(
                Book(
                    id=int(row["id"]),
                    title=row["title"],
                    author=row["author"],
                    isbn=row["isbn"],
                    published=int(row["published"]),
                    tags=row["tags"].split(";") if row["tags"] else [],
                )
            )
    return catalog
