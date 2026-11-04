from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookBaseSchema(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=200)
    year: int | None = Field(default=None, ge=0, le=2100)
    status: Literal['want', 'reading', 'read'] = 'want'
    rating: int | None = Field(default=None, ge=1, le=5)
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator('title', 'author')
    @classmethod
    def _strip_required(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('must not be empty or whitespace only')
        return v

    @field_validator('notes')
    @classmethod
    def _empty_notes_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


class BookCreateSchema(BookBaseSchema):
    model_config = ConfigDict(extra='ignore')


class BookUpdateSchema(BookBaseSchema):
    # полное обновление: title, author обязательны, status дефолтится в 'want'
    model_config = ConfigDict(extra='ignore')


class BookResponseModel(BookBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)