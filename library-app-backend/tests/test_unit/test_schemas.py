import pytest
from pydantic import ValidationError
from schemas.book import BookCreateSchema

# --- 1. Валидация и очистка title ---

@pytest.mark.parametrize(
    "raw_title, expected_title",
    [
        ("Мастер", "Мастер"),
        ("  Мастер  ", "Мастер"),
    ],
)
def test_title_valid_and_trimmed(raw_title, expected_title):
    schema = BookCreateSchema(title=raw_title, author="Булгаков")
    assert schema.title == expected_title


@pytest.mark.parametrize("bad_title", ["", "   ", "\t\n"])
def test_title_rejects_empty(bad_title):
    with pytest.raises(ValidationError):
        BookCreateSchema(title=bad_title, author="Булгаков")


# --- 2. Валидация author ---

@pytest.mark.parametrize("bad_author", ["", "   "])
def test_author_rejects_empty(bad_author):
    with pytest.raises(ValidationError):
        BookCreateSchema(title="Мастер", author=bad_author)


# --- 3. Валидация rating (1..5 или None) ---

@pytest.mark.parametrize("valid_rating", [1, 5, None])
def test_rating_accepts_valid_values(valid_rating):
    schema = BookCreateSchema(title="Мастер", author="Булгаков", rating=valid_rating)
    assert schema.rating == valid_rating


@pytest.mark.parametrize("bad_rating", [0, 6, -1])
def test_rating_rejects_out_of_range(bad_rating):
    with pytest.raises(ValidationError):
        BookCreateSchema(title="Мастер", author="Булгаков", rating=bad_rating)


# --- 4. Валидация year ---

@pytest.mark.parametrize("bad_year", [-1, 3000])
def test_year_rejects_invalid_values(bad_year):
    with pytest.raises(ValidationError):
        BookCreateSchema(title="Мастер", author="Булгаков", year=bad_year)


# --- 5. Валидация и нормализация notes ---

@pytest.mark.parametrize(
    "raw_notes, expected_notes",
    [
        ("   ", None),
        ("", None),
        (None, None),
        ("  hello  ", "hello"),
    ],
)
def test_notes_trimmed_or_none(raw_notes, expected_notes):
    schema = BookCreateSchema(title="Мастер", author="Булгаков", notes=raw_notes)
    assert schema.notes == expected_notes


# --- 6. Валидация status ---

def test_status_rejects_unknown_value():
    with pytest.raises(ValidationError):
        BookCreateSchema(title="Мастер", author="Булгаков", status="foo")


# --- 7. Игнорирование лишних полей (extra='ignore') ---

def test_extra_fields_are_ignored():
    schema = BookCreateSchema(title="Мастер", author="Булгаков", foo="bar")
    assert not hasattr(schema, "foo")
    assert "foo" not in schema.model_dump()
