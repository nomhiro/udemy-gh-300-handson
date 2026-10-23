"""一覧を整形して文字列にする。"""
from datetime import date

from booklib.catalog import Catalog
from booklib.loans import Loan
from booklib.models import Book


def format_book(book: Book) -> str:
    return f"{book.title}／{book.author}（{book.published}年）"


def format_catalog(books: list[Book]) -> str:
    return "\n".join(format_book(book) for book in books)


def format_overdue(loans: list[Loan], catalog: Catalog, today: date) -> str:
    lines = []
    for loan in loans:
        book = catalog.get(loan.book_id)
        title = book.title if book else f"（不明な蔵書 ID {loan.book_id}）"
        days = (today - loan.due_on).days
        lines.append(f"{title}：{days}日 延滞（利用者 ID {loan.member_id}）")
    return "\n".join(lines)


def format_titles(books: list[Book]) -> str:
    """蔵書のタイトルを読点で区切った文字列を返す。"""
    return "、".join(book.title for book in books)
