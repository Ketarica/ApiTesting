from fastapi import FastAPI, HTTPException
# from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from fastapi import FastAPI, Form

app = FastAPI()

books_db = {
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


class Book(BaseModel):
    title: str
    author: str
    genre: str
    year: int


@app.get("/books")
def list_books():
    return books_db


@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]


@app.post("/books/{book_id}")
def add_book(book_id: int, book: Book):
    if book_id in books_db:
        raise HTTPException(status_code=400, detail="Book already exists")
    books_db[book_id] = book.model_dump()
    return {"status": "created", "book": book}


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = book.model_dump()
    return {"status": "created", "book": book}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del books_db[book_id]
    return {"status": "deleted"}
