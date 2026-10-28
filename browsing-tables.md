# Browsing Tables

A table page is where most visitors will
spend their time, and everything on it
is an address doing a job. This chapter
works through the books table of the
lab's catalogue — sorting, filtering,
following the foreign key, and
searching — and every behaviour below
was run against the lab's server, in a
browser's terms and in `curl`'s.

## The table page

`http://127.0.0.1:8001/library/books`
shows all fourteen books as a grid.
Its title says what you are looking at
(transcript `t02`):

```text
$ curl -s http://127.0.0.1:8001/library/books | grep -o '<title>[^<]*</title>'
<title>library: books: 14 rows sorted by year descending</title>
```

*Sorted by year descending* is not the
default for a bare table — it comes from
the metadata file, which chapter 8
covers. Strip the metadata away and the
same page opens in the table's own
order. Keep that in mind whenever a page
surprises you: the metadata is part of
what you are looking at.

Two things to notice in the grid. First,
`author_id` values are links, and the
author's name is printed beside the
number — Datasette follows the foreign
key stored in the file and labels the
number with the matching `authors` row,
so a column of bare numbers reads as a
column of people. (The check is crude
but real: the lab's books page contains
the name *Mara Ellison*, although the
books table itself holds no such text.)
Second, the page offers **facets** down
the side — counted slices of the table —
which are chapter 8's subject proper.

## Filtering: the address is the filter

Above the grid sit filter boxes, but
what they really do is write into the
address. Choose *genre is Mystery* and
the address becomes:

```text
http://127.0.0.1:8001/library/books?genre=Mystery
```

That is the whole mechanism, and it
works from any tool. Through the JSON
door (transcript `t04`), with a count
and the titles pulled out:

```text
$ curl -s 'http://127.0.0.1:8001/library/books.json?genre=Mystery&_shape=objects' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["filtered_table_rows_count"], [r["title"] for r in d["rows"]])'
2 ['The Night Bus to Meridia', 'The Last Ferryman']
```

The same spelling works on every column:
`?author_id=1` finds Mara Ellison's
three books without her name appearing
anywhere in the request. And equality is
only the first of the **filter
arguments**: add two underscores and a
test to the column name. Books longer
than 350 pages:

```text
$ curl -s 'http://127.0.0.1:8001/library/books.json?pages__gt=350&_shape=objects' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["filtered_table_rows_count"], [r["title"] for r in d["rows"]])'
4 ["The Clockmaker's Garden", "A Cartographer's Daughter", 'The Herring Fleet', 'The Salt Road Atlas']
```

The family includes `__gt` and `__lt`
(greater / less than), `__gte` and
`__lte` (or equal to), `__contains`,
`__like`, `__in` for a list of values,
`__isnull` and more. Because filters are
just addresses, filters combine — add
another `&name=value` — and a filtered
view can be bookmarked, linked and
fetched by a script exactly as you see
it. That is chapter 1's claim, now with
its working parts showing.

## Searching the titles

The books table has a search box,
because the database carries a
**full-text search** index — a separate
structure, built by SQLite's FTS5
machinery, that knows which titles
contain which words. Searching is
another address argument, `_search`:

```text
$ curl -s 'http://127.0.0.1:8001/library/books.json?_search=lighthouse&_shape=objects' | python3 -c 'import json,sys; d=json.load(sys.stdin); print([r["title"] for r in d["rows"]])'
['A Manual for Lighthouse Keepers']
```

One word, one book, out of fourteen.
The JSON even confesses how: the query
it ran reads `where rowid in (select
rowid from books_fts where books_fts
match ...)`. Search looks only at the
columns the index was built over — here,
titles — and only exists at all when the
database was built with such an index.
Datasette does not invent one. If your
table has no search box, that is why;
and if search seems to *ignore* what you
type and return everything, chapter 13
has the lab's own story about that,
which is subtler and easier to fall
into.

## One row

Click a row's `id` — or write its
address, `/library/books/5` — and you
get that book alone, with its author's
name linked onward to the author's own
row page, from which *their* books are
one more click. Browsing a database this
way, table to row to related row, is
the experience Datasette exists to give,
and it needs no preparation beyond the
foreign keys the file already holds.
