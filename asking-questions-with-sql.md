# Asking Questions with SQL

Browsing and filtering cover the
questions the pages anticipate. The
query box covers the rest: any question
that can be asked in a `SELECT`
statement, asked of the living data.
This chapter runs questions both ways —
typed in the browser and fetched through
the API — then shows how to save the
good ones as **canned queries**, and
meets the two guards that keep the box
safe to offer.

You do not need much SQL to follow this
chapter — a `SELECT` names the columns
you want, a table to take them from, and
optionally conditions and an order. The
SQLite guide teaches the language
properly; here it is a tool for asking,
used at the depth the answers need.

## Your question, through the API

The database page in a browser has a
query box; the same question travels
through the API by writing it into the
database's `.json` address, in the `sql`
argument. How many books per genre
(transcript `t05`):

```text
$ curl -s 'http://127.0.0.1:8001/library.json?sql=select+genre,+count(*)+as+n+from+books+group+by+genre+order+by+n+desc&_shape=objects'
{"ok": true, "database": "library", "query_name": null, "rows": [{"genre": "Fiction", "n": 4}, {"genre": "History", "n": 3}, {"genre": "Fantasy", "n": 3}, {"genre": "Mystery", "n": 2}, {"genre": "Poetry", "n": 1}, {"genre": "Essays", "n": 1}], "truncated": false, "columns": ["genre", "n"], "query": {"sql": "select genre, count(*) as n from books group by genre order by n desc", "params": {}}, "error": null, "private": false, "allow_execute_sql": true, "query_ms": 0.64, "source": "The Datasette for Mere Mortals lab", "license": "CC0"}
```

Note the shape of a successful answer:
`ok: true`, the rows, the columns, the
SQL as Datasette received it, how long
it took, and `error: null`. Note also
`allow_execute_sql: true` — whether
visitors may run their own SQL is a
setting the publisher controls, and
chapter 12 is honest that on a public
site you might turn it off and keep only
the canned queries below.

## Canned queries: questions with names

A question worth asking twice is worth
saving. The metadata file can carry
**canned queries** — SQL with a name, a
title and a description, living at their
own address under the database. The
lab's metadata defines `books_with_authors`,
a join across the foreign key:

```sql
select books.title as title, authors.name as author,
       books.year as year, books.genre as genre
from books join authors on authors.id = books.author_id
order by books.year
```

It answers at `/library/books_with_authors`
as a page, and at
`/library/books_with_authors.json` as
data (transcript `t05`) — every book
with a person's name where the raw table
keeps a number:

```json
{"ok": true, "database": "library", "query_name": "books_with_authors", "rows": [{"title": "A Manual for Lighthouse Keepers", "author": "Walter Pryce", "year": 1998, "genre": "History"}, {"title": "The Last Ferryman", "author": "Walter Pryce", "year": 2003, "genre": "Mystery"}], "columns": ["title", "author", "year", "genre"]}
```

(excerpted — the answer holds all
fourteen books, oldest first.)

Two honest observations from the lab.
First, a canned query is where SQL
knowledge can be *given away*: the
author of the metadata writes the join
once, and every visitor after that just
opens a link. Second, canned queries
are not table pages in disguise — the
table machinery of `_size` does not
apply to them the same way. The lab
asked this one for `_size=3` and got
all fourteen rows, the argument politely
treated as a spare parameter (it is
echoed in the answer's `params`, unused).
Canned queries answer whole, up to
Datasette's overall row ceiling; design
them with that in mind.

## Guard one: writes are refused

The query box will not change data. The
lab tried, in the plainest way
(transcript `t90`):

```text
$ curl -s 'http://127.0.0.1:8001/library.json?sql=delete+from+books+where+id+%3D+1'
{"ok": false, "error": "Statement must be a SELECT", "status": 400, "title": "Invalid SQL"}
```

And then counted the books, to make the
refusal a fact rather than a promise:

```text
$ curl -s 'http://127.0.0.1:8001/library/books.json' | python3 -c 'import json,sys; print(json.load(sys.stdin)["filtered_table_rows_count"])'
14
```

This is not a permissions setting that a
clever address can talk its way around;
the server only ever opens the file to
read it. INSERT, UPDATE, DELETE, DROP —
all the same answer.

## Guard two: slow questions are stopped

A `SELECT` can still be a bad idea — a
question whose answer takes forever to
work out. Datasette gives every query a
time limit (one second by default) and
interrupts it past that. The lab fed it
an endless counting query, which SQLite
would happily have run until the heat
death of the universe (transcript `t90`):

```text
$ curl -s --max-time 10 'http://127.0.0.1:8001/library.json?sql=with+recursive+cnt(x)+as+(select+1+union+all+select+x%2B1+from+cnt)+select+count(*)+from+cnt'
{"ok": false, "error": "<p>SQL query took too long. The time limit is controlled by the sql_time_limit_ms configuration option.</p> …", "status": 400, "title": "SQL Interrupted"}
```

(the error text continues with a copy of
the query, trimmed here.) The answer
arrived in about a second, the server
unharmed and still answering. The limit
is a setting (`sql_time_limit_ms`) the
publisher can raise for a heavy internal
dataset — but notice what it protects:
not the data, which was never at risk,
but the server and everyone else using
it.

## Broken questions fail in the open

A misspelled question gets a JSON answer
too, carrying SQLite's own words
(transcript `t90`):

```text
$ curl -s 'http://127.0.0.1:8001/library.json?sql=select+from+where'
{"ok": false, "database": "library", "query_name": null, "rows": [], "columns": [], "query": {"sql": "select from where", "params": {}}, "error": "near \"from\": syntax error", "private": false, "allow_execute_sql": true, "query_ms": 1.00}
```

(field order trimmed for the page.)
Everyone who has used SQL knows that
`near "from": syntax error` is the whole
of the help a database gives; the point
here is only that the API delivers it in
the same structured envelope as a
success, so a script can show it to a
human instead of dying on it.
