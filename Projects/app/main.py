import sqlite3
from types import MethodType
from flask import Flask, request, jsonify, g

# Initialize Flask app
app = Flask(__name__)
DATABASE = "books.db"


# Helper function to connect to the database
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                published_date TEXT
            )
        """)
        db.commit()


# Initialize the database
init_db()


@app.route("/", methods=["GET"])
def greet_user():
    return jsonify({"message": "Hello guys how are you doing !! "})


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    published_date = data.get("published_date")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, author, genre, published_date)
        VALUES (?, ?, ?, ?)
    """,
        (title, author, genre, published_date),
    )
    db.commit()

    return jsonify({"message": "Book created successfully!"}), 201


# Route to get all books
@app.route("/books", methods=["GET"])
def get_books():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    return jsonify(
        [
            {
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "genre": row[3],
                "published_date": row[4],
            }
            for row in books
        ]
    )


# Route to get a specific book by id
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()

    if book is None:
        return jsonify({"message": "Book not found"}), 404

    return jsonify(
        {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "genre": book[3],
            "published_date": book[4],
        }
    )


# Route to update a book by id
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    published_date = data.get("published_date")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        UPDATE books
        SET title = ?, author = ?, genre = ?, published_date = ?
        WHERE id = ?
    """,
        (title, author, genre, published_date, book_id),
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Book not found"}), 404

    return jsonify({"message": "Book updated successfully!"})


# Route to delete a book by id
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"message": "Book not found"}), 404

    return jsonify({"message": "Book deleted successfully!"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
