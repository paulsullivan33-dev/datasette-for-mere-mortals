# Glossary

**API** — a way for programs, rather
than people, to ask for things.
Datasette's API is its pages answered as
JSON when `.json` is added to the
address.

**Canned query** — a SQL question saved
in the metadata file with a name and
title, living at its own address, so
visitors can run it without writing SQL.

**Facet** — a column presented as
counted choices (genre: Fiction 4,
Mystery 2, …); choosing one filters the
table, and the counts are computed
before you choose.

**Filter argument** — a `name=value`
pair in an address that narrows a
table's rows: `?genre=Mystery`, or with
an operator, `?pages__gt=350`.

**Foreign key** — a column whose values
are primary keys of another table:
`books.author_id` holding an `id` from
`authors`. Datasette renders them as
links and labels them with the linked
row.

**FTS / full-text search** — SQLite's
machinery (FTS5) for indexing the words
in text columns so they can be searched
quickly. Datasette offers a search box
for tables that carry such an index.

**JSON** — a structured text format for
data, readable by nearly every
programming language: objects of named
fields, lists, numbers, strings.

**Metadata file** — the JSON file given
with `--metadata`, holding the
publication around the data: titles,
descriptions, licence, source, default
sorts, facets and canned queries.

**Plugin** — a separate package that
extends Datasette: extra publish
targets, displays, and features the core
tool leaves out.

**Primary key** — the column (or set)
whose value uniquely identifies a row,
usually named `id`. A row's address in
Datasette is its primary key's value.

**Query box** — the place on a database
page (and the `sql` argument of its
`.json` address) where a `SELECT`
statement can be typed and run.

**Read-only** — Datasette's defining
rule: it opens databases to read them
and refuses every statement that is not
a `SELECT`.

**`_search`** — the address argument
that runs a table's full-text search:
`/library/books?_search=ferryman`.

**`_shape`** — the address argument that
chooses how rows arrive in JSON:
`objects` for named fields, the default
arrays of values, `arrayfirst` for just
the first column, and others.

**`_size` and `next_url`** — the page
size argument, and the address of the
next page of rows that a paginated
answer hands back, position-marked
rather than page-numbered.

**SQL** — the language databases answer
to. A `SELECT` statement asks a
question; Datasette permits no other
kind through its doors.

**Table page / row page / database
page** — Datasette's three levels of
page: a database and its tables, a
table and its rows, one row and its
relations — each with a `.json` twin.
