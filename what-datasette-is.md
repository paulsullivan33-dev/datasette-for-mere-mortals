# What Datasette Is

Take a **SQLite database**: one file on a
disk, holding **tables** — grids of rows
and columns, like a spreadsheet that
keeps its promises about what kind of
thing goes in each column. Programs keep
their data in such files, governments
publish open data as such files, and
chances are your computer already holds
dozens. The usual ways in are a database
program, where you type **SQL** — the
query language databases speak — or a
script someone wrote against the file.

**Datasette is a program that serves
such a file as a website and an API at
the same time.** You point it at a
database file and start it:

```bash
datasette serve library.db
```

It answers on a web address. A person
opening that address in a browser gets
pages: a home page listing the database
and its tables with their row counts, a
page per table with the rows in a grid,
a page per row, filters and search boxes
and links that follow the connections
between tables. A program asking for the
same addresses with `.json` on the end
gets the same content as **JSON** —
structured text a script can pull apart
field by field. Same data, two doors:
one for eyes, one for code.

## The one idea to keep

Everything in Datasette is an **address**.
A table is an address. A row is an
address. A filtered view of a table —
only the mystery books, say — is the
table's address with the filter written
into it, after a `?`. A question you ask
in SQL is an address with the question
written into it. That sounds like a
detail; it is the whole design. Because
the state lives in the address, you can
bookmark a filter, send a colleague a
link that lands on exactly the rows you
were looking at, and fetch the same rows
from a script by asking for the same
address with `.json` added.

## Read-only, on purpose

Datasette never writes to the databases
it serves. There is no edit button
because editing is not a feature that
failed to ship; it is a line the tool
draws. Serving is safe to try against a
file you care about in a way that
pointing a general database tool at it
is not: the worst a visitor — or you,
clicking around — can do is ask an
expensive question, and chapter 7 shows
the guard that stops even that. When
the lab tried to delete a row through
the query box, the answer came back in
plain JSON:

```json
{"ok": false, "error": "Statement must be a SELECT", "status": 400, "title": "Invalid SQL"}
```

The row was still there afterwards. The
table's row count said so.

## Why anyone would do this

- **Exploring.** Someone hands you a
  database file and you want to know
  what is in it before you write any
  code against it. Ten minutes of
  clicking beats an afternoon of
  guess-the-table-name in a SQL prompt.
- **Sharing.** A club's catalogue, a
  project's measurements, a town's
  published figures: data other people
  should be able to look through without
  installing database tools or being
  handed the raw file and good wishes.
- **Feeding programs.** The same pages
  a person browses answer as JSON, so a
  script, a spreadsheet or another
  website can pull the data through the
  same addresses — no separate API to
  build or keep in step.
- **Publishing.** With a small metadata
  file — titles, descriptions, a
  licence, saved queries — a served file
  becomes a small publication with your
  name and terms on it. Chapter 8 is
  about that step, and chapter 9 about
  putting it where other people can
  reach it.

## What you need

A database file, or chapter 4's twenty
minutes to build the lab's. A machine to
run one command on. Nothing else: no
accounts, no other services, and the
server runs happily on the same machine
you browse from, which is exactly how
the lab ran it — every address in this
guide is `127.0.0.1`, the address that
means *this machine*, on port 8001.
