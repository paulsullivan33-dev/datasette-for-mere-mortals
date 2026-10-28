# The JSON API

Everything the browser shows, a program
can have as data. This chapter takes the
`.json` switch apart: what a table's
JSON actually contains, the shapes rows
can arrive in, one row's JSON, and how
to walk a table bigger than one page.

## `.json` on everything

The rule from chapter 1 holds without
exceptions in the lab's runs: the home
page, the database page (`/library.json`,
seen in chapter 4), every table, every
row, every query — add `.json`. The
answer is a JSON object describing the
page, not merely the rows in it.
A table's answer (transcript `t03`,
trimmed here to its skeleton) carries:

```json
{
  "database": "library",
  "table": "books",
  "human_description_en": "sorted by year descending",
  "rows": [[12, "Gardens of the Rain Coast", 5, 2023, "Fiction", 288], [8, "Paper Boats", 4, 2021, "Poetry", 96], [3, "The Winter Bees", 1, 2020, "Fiction", 296]],
  "filtered_table_rows_count": 14,
  "columns": ["id", "title", "author_id", "year", "genre", "pages"],
  "primary_keys": ["id"],
  "query": {"sql": "select id, title, author_id, year, genre, pages from books order by year desc limit 4", "params": {}},
  "facet_results": { "…": "chapter 8" },
  "next": "2020,3",
  "next_url": "http://127.0.0.1:8001/library/books.json?_size=3&_next=2020%2C3&_sort_desc=year"
}
```

Three habits worth forming. The answer
tells you the **SQL it ran** — when a
result surprises you, that field is the
first place to look. It tells you the
**count after filtering**
(`filtered_table_rows_count`), which is
a different number from the rows it
happened to send. And when there are
more rows than it sent, it tells you
where they live: `next_url`, below.

## Shapes: how rows arrive

By default `rows` is a list of lists —
values in column order, with `columns`
carried separately, as in the excerpt
above. Programs usually prefer each row
as an object with named fields. That is
what `_shape` is for:

- **`_shape=objects`** — every row an
  object: `{"id": 14, "title": "The Last
  Ferryman", "author_id": 6, …}`. Most of
  this guide's examples use it, and most
  of yours will too.
- **`_shape=arrayfirst`** — just the
  first column's values, as one flat
  list. The lab asked a whole table for
  its ids in display order and got
  `[12, 8, 3, 10, 5, 9, 2, 7, 1, 4, 11,
  6, 14, 13]` — the sort (year,
  descending) visible in the numbers
  themselves.
- There are more (`object`, `arrays`,
  `array`) for single-column and
  key-by-id cases; they are variations on
  the two above, and the reference
  documentation enumerates them.

The lab's first probe script assumed
rows would be objects, indexed them by
name, and died with `TypeError: list
indices must be integers`. That error
has caught many first scripts; now it
will not catch yours. Ask for the shape
you mean.

## One row as JSON

A row page takes `.json` like anything
else (transcript `t06`):

```text
$ curl -s 'http://127.0.0.1:8001/library/books/5.json'
{"database": "library", "table": "books", "rows": [[5, "The Night Bus to Meridia", 2, 2018, "Mystery", 328]], "columns": ["id", "title", "author_id", "year", "genre", "pages"], "primary_keys": ["id"], "primary_key_values": ["5"], "units": {}, "query_ms": 1.11, "source": "The Datasette for Mere Mortals lab", "license": "CC0"}
```

Note `source` and `license` riding along
at the end — the metadata file's fields,
attached to every answer the API gives.
Chapter 8 explains putting them there;
for now, register that the API does not
let data travel without its terms.

## Pagination: follow `next_url`

Tables can be bigger than a page. Ask
for five rows at a time with `_size=5`
and the answer's `next_url` is the
address of the next five — not a page
number, but a position marker built
from the sort order (here, the year and
id of the last row sent). The lab
followed it verbatim (transcript `t06`):

```text
$ curl -s 'http://127.0.0.1:8001/library/books.json?_size=5&_shape=objects' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d["rows"]), d["next_url"])'
5 http://127.0.0.1:8001/library/books.json?_size=5&_shape=objects&_next=2018%2C5&_sort_desc=year
$ curl -s '<the next_url from the line above>' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d["rows"]), [r["title"] for r in d["rows"]])'
5 ["The Clockmaker's Garden", "A Cartographer's Daughter", 'The Herring Fleet', 'The Salt Road Atlas', 'Signals from a Small Town']
```

The second five are exactly the years
2016 down to 2009, continuing where the
first page (2023 down to 2018) stopped.
That is the pattern to program against:
fetch, read `next_url`, fetch again,
stop when `next_url` is `null`. Because
the marker encodes position in the sort
rather than a count of pages, rows
inserted by someone else between your
fetches cannot silently shift you a page
— one more thing the address-based
design buys without asking.

## Errors are JSON too

Ask for a table that does not exist and
the API answers in kind (transcript
`t90`):

```text
$ curl -s -w '\nhttp: %{http_code}\n' 'http://127.0.0.1:8001/library/nope.json'
{"ok": false, "error": "Table not found", "status": 404, "title": null}
http: 404
```

A script never has to guess whether an
answer is data or a complaint: `ok`
says so, and the HTTP status agrees.
Chapter 7 adds the query errors to this
picture, and chapter 13 rounds up the
whole family.
