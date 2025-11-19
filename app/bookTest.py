# from typing import Optional, Dict
# from datetime import date
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field, field_validator
#
# app = FastAPI()
#
# books_db = {
#     1: {
#         "title": "Neuromancer",
#         "author": "William Gibson",
#         "genre": "Cyberpunk",
#         "year": 1984,
#     },
#     2: {
#         "title": "Snow Crash",
#         "author": "Neal Stephenson",
#         "genre": "Cyberpunk",
#         "year": 1992,
#     },
#     3: {
#         "title": "Do Androids Dream of Electric Sheep?",
#         "author": "Philip K. Dick",
#         "genre": "Science Fiction",
#         "year": 1968,
#     },
#     4: {
#         "title": "The Three-Body Problem",
#         "author": "Liu Cixin",
#         "genre": "Hard Sci-Fi",
#         "year": 2006,
#     },
#     5: {
#         "title": "The Hobbit",
#         "author": "J. R. R. Tolkien",
#         "genre": "Fantasy",
#         "year": 1937,
#     },
# }
#
#
# class BookBase(BaseModel):
#     title: str = Field(..., min_length=1, max_length=200, example="Neuromancer")
#     author: str = Field(..., min_length=1, max_length=100, example="William Gibson")
#     genre: str = Field(..., min_length=1, max_length=50, example="Cyberpunk")
#     year: int = Field(..., ge=0, lt=10000, example=1984)  # базовые ограничения
#
#     @field_validator("title", "author", "genre")
#     @classmethod
#     def strip_strings(cls, v: str) -> str:
#         # убираем лишние пробелы вокруг
#         return v.strip()
#
#     @field_validator("year")
#     @classmethod
#     def validate_year_not_in_future(cls, v: int) -> int:
#         current_year = date.today().year
#         if v > current_year:
#             raise ValueError(
#                 f"year ({v}) cannot be in the future (current year: {current_year})"
#             )
#         return v
#
#
# # @app.get("/books")
# # def list_books():
# #     return books_db
# #
# #
# # @app.get("/books/{book_id}")
# # def get_book(book_id: int):
# #     if book_id not in books_db:
# #         raise HTTPException(status_code=404, detail="Book not found")
# #     return books_db[book_id]
# #
# #
# # @app.post("/books/{book_id}")
# # def add_book(book_id: int, book: Book):
# #     if book_id in books_db:
# #         raise HTTPException(status_code=400, detail="Book already exists")
# #     books_db[book_id] = book.model_dump()
# #     return {"status": "created", "book": book}
# #
# #
# # @app.put("/books/{book_id}")
# # def update_book(book_id: int, book: Book):
# #     if book_id not in books_db:
# #         raise HTTPException(status_code=404, detail="Book not found")
# #     books_db[book_id] = book.model_dump()
# #     return {"status": "created", "book": book}
# #
# #
# # @app.delete("/books/{book_id}")
# # def delete_book(book_id: int):
# #     if book_id not in books_db:
# #         raise HTTPException(status_code=404, detail="Book not found")
# #     del books_db[book_id]
# #     return {"status": "deleted"}


from typing import Optional, Dict
from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

books_db: Dict[int, dict] = {
    1: {
        "title": "Neuromancer",
        "author": "William Gibson",
        "genre": "Cyberpunk",
        "year": 1984,
    },
    2: {
        "title": "Snow Crash",
        "author": "Neal Stephenson",
        "genre": "Cyberpunk",
        "year": 1992,
    },
    3: {
        "title": "Do Androids Dream of Electric Sheep?",
        "author": "Philip K. Dick",
        "genre": "Science Fiction",
        "year": 1968,
    },
    4: {
        "title": "The Three-Body Problem",
        "author": "Liu Cixin",
        "genre": "Hard Sci-Fi",
        "year": 2006,
    },
    5: {
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "genre": "Fantasy",
        "year": 1937,
    },
}


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Neuromancer")
    author: str = Field(..., min_length=1, max_length=100, example="William Gibson")
    genre: str = Field(..., min_length=1, max_length=50, example="Cyberpunk")
    year: int = Field(..., ge=0, lt=10000, example=1984)  # базовые ограничения

    @field_validator("title", "author", "genre")
    @classmethod
    def strip_strings(cls, v: str) -> str:
        # убираем лишние пробелы вокруг
        return v.strip()

    @field_validator("year")
    @classmethod
    def validate_year_not_in_future(cls, v: int) -> int:
        current_year = date.today().year
        if v > current_year:
            raise ValueError(
                f"year ({v}) cannot be in the future (current year: {current_year})"
            )
        return v


class BookCreate(BookBase):
    """
    Модель для запроса создания книги.
    Нужна, чтобы явно отделить входные данные (без id) от возвращаемой модели.
    """

    pass


class BookUpdate(BaseModel):
    """
    Модель для частичного обновления. Все поля опциональны.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    year: Optional[int] = Field(None, ge=0, lt=10000)

    @field_validator("title", "author", "genre", mode="before")
    @classmethod
    def strip_opt_strings(cls, v):
        if v is None:
            return v
        return v.strip()

    @field_validator("year")
    @classmethod
    def validate_year_not_in_future(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        current_year = date.today().year
        if v > current_year:
            raise ValueError(
                f"year ({v}) cannot be in the future (current year: {current_year})"
            )
        return v


class Book(BookBase):
    """
    Модель, возвращаемая клиенту. Дополнена id.
    """

    id: int = Field(..., example=1)


@app.get("/books", response_model=dict)
def list_books():
    # возвращаем "сырую" БД словаря — в реальном приложении лучше сериализовывать модели
    return books_db


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    data = books_db[book_id].copy()
    data["id"] = book_id
    return Book(**data)


@app.post("/books/{book_id}", response_model=Book, status_code=201)
def add_book(book_id: int, book: BookCreate):
    if book_id in books_db:
        raise HTTPException(status_code=400, detail="Book already exists")
    books_db[book_id] = book.model_dump()
    out = books_db[book_id].copy()
    out["id"] = book_id
    return Book(**out)


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")

    # текущая запись
    current = books_db[book_id].copy()

    # получаем словарь только с заданными полями (те, которые не None)
    updates = {k: v for k, v in book.model_dump().items() if v is not None}

    # если ничего не пришло — вернуть текущее состояние (или можно выбросить ошибку)
    if not updates:
        return Book(id=book_id, **current)

    # применяем изменения
    current.update(updates)
    books_db[book_id] = current
    out = current.copy()
    out["id"] = book_id
    return Book(**out)


@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return {"status": "deleted"}
