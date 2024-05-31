# Python (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient
from fastapi.responses import RedirectResponse

app = FastAPI()


# All books must match this format
class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: str
    price: float


# Dictionary to hold all the books
books: dict[int:Book] = {}


# Initially opens on the home page
@app.get("/")
def get_homepage():
    return RedirectResponse(url="/books", status_code=302)


# Returns all books as JSON
@app.get("/books", status_code=200)
def getbooks():
    return books


# Book must exist
# Returns the book specified as JSON
@app.get("/books/{book_id}", status_code=200)
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found, create it first.")
    return {book_id: books[book_id]}


# Book must not exist
# Returns the book created as JSON
@app.post("/books", status_code=201)
def create_book(book: Book):
    if book.id in books:
        raise HTTPException(
            status_code=400,
            detail="Book has already been created, try editing it or change the id.",
        )
    books[book.id] = book
    return {book.id: book}


# Book must exist
# Returns the book edited as JSON
@app.put("/books/{book_id}", status_code=200)
def update_book(book_id: int, book: Book):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found, create it first.")
    books[book_id] = book
    return {book_id: book}


# Book must exist
# Returns the remaining books as JSON
@app.delete("/books/{book_id}", status_code=200)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found, create it first.")
    del books[book_id]
    return books


# Test app
client = TestClient(app)


# Tests
def test_create_book():
    response = client.post(
        "/books",
        json={
            "id": 1,
            "title": "Book 1",
            "author": "Author 1",
            "published_date": "2022-01-01",
            "price": 9.99,
        },
    )
    assert response.status_code == 201


def test_get_book():
    response = client.get("/books/1")
    assert response.status_code == 200


def test_update_book():
    response = client.put(
        "/books/1",
        json={
            "title": "Updated Book 1",
            "author": "Updated Author 1",
            "published_date": "2022-01-02",
            "price": 19.99,
        },
    )
    assert response.status_code == 200


def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200


def test_getbooks():
    response = client.get("/books")
    assert response.status_code == 200
