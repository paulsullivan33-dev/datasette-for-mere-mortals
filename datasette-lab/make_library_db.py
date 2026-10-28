"""Build the guide's fixture database, library.db.

A small invented library catalogue: two tables joined by a foreign
key (books.author_id -> authors.id), plus a full-text search table
for book titles. Every name and title here is invented for the lab.
Run it again any time to get a fresh copy; it deletes the old file.
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

AUTHORS = [
    (1, "Mara Ellison", 1968),
    (2, "Tomas Reyes", 1975),
    (3, "Ingrid Halvorsen", 1959),
    (4, "Felix Okafor", 1983),
    (5, "June Nakamura", 1971),
    (6, "Walter Pryce", 1944),
]

# title, author_id, year published, genre, pages
BOOKS = [
    (1, "The Salt Road Atlas", 1, 2011, "Fantasy", 384),
    (2, "A Cartographer's Daughter", 1, 2015, "Fantasy", 412),
    (3, "The Winter Bees", 1, 2020, "Fiction", 296),
    (4, "Signals from a Small Town", 2, 2009, "Fiction", 244),
    (5, "The Night Bus to Meridia", 2, 2018, "Mystery", 328),
    (6, "Fjord Light", 3, 2005, "Fiction", 212),
    (7, "The Herring Fleet", 3, 2013, "History", 356),
    (8, "Paper Boats", 4, 2021, "Poetry", 96),
    (9, "The Clockmaker's Garden", 4, 2016, "Fantasy", 368),
    (10, "Notes on Silence", 5, 2019, "Essays", 176),
    (11, "The Rice Paddy Letters", 5, 2007, "History", 304),
    (12, "Gardens of the Rain Coast", 5, 2023, "Fiction", 288),
    (13, "A Manual for Lighthouse Keepers", 6, 1998, "History", 264),
    (14, "The Last Ferryman", 6, 2003, "Mystery", 312),
]


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")
    db.execute(
        """
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            born INTEGER
        )
        """
    )
    db.execute(
        """
        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL REFERENCES authors(id),
            year INTEGER,
            genre TEXT,
            pages INTEGER
        )
        """
    )
    db.executemany("INSERT INTO authors VALUES (?, ?, ?)", AUTHORS)
    db.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?)", BOOKS)
    # Full-text search over book titles, kept in step with books.
    # Note the double quotes around the table name in content= :
    # Datasette only recognises the search table as belonging to
    # books when the CREATE statement spells it content="books".
    db.execute(
        'CREATE VIRTUAL TABLE books_fts USING fts5(title, content="books", content_rowid="id")'
    )
    db.execute("INSERT INTO books_fts(books_fts) VALUES ('rebuild')")
    db.commit()
    for table in ("authors", "books"):
        count = db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count} rows")
    db.close()
    print(f"wrote {os.path.basename(DB_PATH)}")


if __name__ == "__main__":
    main()
