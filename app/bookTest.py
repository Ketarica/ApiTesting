from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    id: int
    title: str
    author: str
    genre: str
    year: int


@app.get("/books")
async def get_all():
    return books_db


@app.get("/books/{book_id}")
def get_books_by_id(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]
