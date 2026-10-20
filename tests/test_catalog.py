import pytest

from booklib.models import Book


def test_add_and_get(small_catalog):
    assert small_catalog.get(2).title == "はじめての Git"
    assert small_catalog.get(99) is None


def test_add_duplicate_id(small_catalog):
    with pytest.raises(ValueError):
        small_catalog.add_book(Book(1, "別の本", "誰か", "000", 2000))


def test_find_by_title(small_catalog):
    assert [b.id for b in small_catalog.find_by_title("Python")] == [1]
    assert small_catalog.find_by_title("存在しない") == []


@pytest.mark.parametrize("title", ["python", "PYTHON", "pYtHoN", "yTh"])
def test_find_by_title_case_insensitive(small_catalog, title):
    assert [b.id for b in small_catalog.find_by_title(title)] == [1]


def test_search_by_author_and_tag(small_catalog):
    assert [b.id for b in small_catalog.search(["青木 葵"])] == [1, 3]
    assert [b.id for b in small_catalog.search(["入門"])] == [1, 2]


def test_search_no_duplicates(small_catalog):
    assert [b.id for b in small_catalog.search(["Python", "入門"])] == [1, 2]


def test_load_catalog(full_catalog):
    assert len(full_catalog.all_books()) == 50
    assert full_catalog.get(1).tags == ["python", "入門"]
