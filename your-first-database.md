# Your First Database

This chapter delivers the guide's first
outcome: a database you built, served by
Datasette, answering in a browser and to
`curl` — with a check at each step so
you know it worked.

## The fixture: a small library catalogue

The lab's database is invented and
deliberately ordinary: a library
catalogue with two tables. **authors**
holds six writers (`id`, `name`,
`born`). **books** holds fourteen books
(`id`, `title`, `author_id`, `year`,
`genre`, `pages`), and `author_id` is a
**foreign key** — each value is the `id`
of a row in `authors`, which is how the
database itself says *this book is by
that person*. There is also a hidden
third structure, a full-text search
index over the titles, which chapter 5
puts to work.

The script that builds it is
`make_library_db.py` in the lab folder
(`datasette-lab/`). Run it from that
folder:

```text
$ python3 make_library_db.py
authors: 6 rows
books: 14 rows
wrote library.db
```

It deletes any old copy and builds a
fresh one, so you can run it whenever
the file needs resetting. Check the
foreign key landed — the database should
report the connection between the
tables in its own words (transcript
`t01`):

```text
$ python3 -c 'import sqlite3; db = sqlite3.connect("library.db"); print(db.execute("pragma foreign_key_list(books)").fetchall())'
[(0, 0, 'authors', 'author_id', 'id', 'NO ACTION', 'NO ACTION', 'NONE')]
```

Read that as: column `author_id` of
`books` refers to column `id` of
`authors`. Datasette will read the same
fact out of the file; nothing needs
telling twice.

## Starting the server

From the same folder:

```bash
datasette serve library.db --host 127.0.0.1 --port 8001 --metadata metadata.json
```

The metadata file (also in the lab
folder) is chapter 8's subject; using it
from the start means the pages carry the
catalogue's proper title instead of bare
file names. The server announces itself:

```text
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
```

Leave that terminal alone — the server
runs in it, in the foreground, until you
press CTRL+C or close it. Work in a
second terminal from here on.

## The homepage

Open `http://127.0.0.1:8001/` in a
browser. What the lab's server answered
can be checked without one, by asking
for the page's title (transcript `t02`):

```text
$ curl -s http://127.0.0.1:8001/ | grep -o '<title>[^<]*</title>'
<title>Harbour Street Library Catalogue: library</title>
```

The title is the metadata's doing. The
page itself lists the one database,
`library`, and inside it the two tables
with their row counts, and the canned
query the metadata defines. Follow the
`library` link and you are on the
database page; chapter 5 takes the table
pages apart.

## The same page, as data

Before browsing further, meet the one
trick the whole guide leans on. Ask for
the database page as JSON:

```text
$ curl -s http://127.0.0.1:8001/library.json | python3 -c 'import json,sys; d=json.load(sys.stdin); print([(t["name"], t["count"], t["fts_table"]) for t in d["tables"] if not t["hidden"]])'
[('authors', 6, None), ('books', 14, 'books_fts')]
```

The full answer (transcript `t02`) says
more: each table's columns and primary
keys, the foreign keys in both
directions — `authors` is told which
table points *at* it, `books` which
table it points *to* — and a
`hidden_count` of 5: the search index
keeps helper tables of its own, which
Datasette knows are machinery and keeps
off the stage. The `books` entry names
its search table, `books_fts`; chapter
5's search and chapter 13's cautionary
tale both hang on that one field.

## Stopping

CTRL+C in the server's terminal, or —
the way the lab did it once the server
ran detached — kill it by process
number, and confirm the address is
closed (transcript `t91`):

```text
$ curl -s --max-time 3 http://127.0.0.1:8001/
curl exit code: 7
```

Exit code 7 is curl's *could not
connect*: nothing is listening, the
server is really stopped, and the
database file is exactly as it was —
because it was never anything but read.
