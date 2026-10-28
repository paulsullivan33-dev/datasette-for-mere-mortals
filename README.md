# Datasette for Mere Mortals

A **SQLite** database is a single file
that holds tables — rows and columns of
data, with a small database engine that
can answer questions about them. Files
like that are everywhere, but reading one
normally means opening a database tool
and typing **SQL**, the language
databases answer to. **Datasette** takes
such a file and turns it into two things
at once: a **website** you can browse —
click a table, filter its rows, follow a
link from a book to its author — and a
**JSON API**, the same pages answered as
structured data that other programs can
fetch. One command starts it; the
database file itself is never changed.

This guide explains how that works, how
to serve a small database on your own
machine, how to browse and filter its
tables, how every page becomes JSON by
adding `.json` to its address, how to
ask your own questions in SQL and save
the good ones as **canned queries** for
other people, and how a small
**metadata** file adds the titles,
descriptions, facets and licensing that
turn a raw file into a small publication.
The limits are stated plainly, including
the big one: Datasette only reads. It
will not edit your data, and this guide
does not pretend otherwise.

The lab behind this guide ran the real
thing: **Datasette 0.65.5**, installed
with pip into a fresh virtual environment
on a small Linux machine, serving a
fixture database the lab built for the
purpose — an invented library catalogue
of six authors and fourteen books, joined
by a foreign key. Against it the lab
captured the browsable pages and their
JSON twins, filtered rows by column value
and by size, searched titles through a
full-text index, ran its own SQL and a
canned query, followed the API's
pagination links to the second page, and
tried to delete a row through the query
box — Datasette refused, in writing, and
the row count afterwards proved nothing
had moved. The lab also broke its own
search on purpose the way real setups
break it, by building the search index
with the wrong kind of quote, and chapter
13 tells that story so you can recognise
it.

What the lab could not do, it did not
fake. Publishing to a cloud host needs an
account with that host, and the lab has
none, so `datasette publish` is shown
only as far as the command surface the
bare tool ships — its targets named, the
rest labelled documented-only wherever it
appears. Accounts, permissions and the
plugin ecosystem are likewise described
from the project's documentation, not
demonstrated. `criteria.md` keeps the
full ledger of what was run and what was
only read.

## What this guide covers

- [**What Datasette is**](what-datasette-is.md) —
  the mental model: one file in, a website
  and an API out, and why read-only is the
  point rather than a missing feature
- [**The moving parts**](the-moving-parts.md) —
  the server, databases, tables, rows and
  queries as addresses, the `.json` switch,
  metadata, and plugins, and which part
  holds what
- [**Installing Datasette**](installing-datasette.md) —
  the pip install into a virtual
  environment, the version check, and
  where the one command lives
- [**Your first database**](your-first-database.md) —
  building the lab's little catalogue,
  starting the server, and reading the
  homepage it answers with
- [**Browsing tables**](browsing-tables.md) —
  table pages, sorting, filters written
  into the address, following a foreign
  key to a name, and searching titles
- [**The JSON API**](the-json-api.md) —
  `.json` on every page, the shapes rows
  can arrive in, one row's own page, and
  pagination that hands you the next
  address instead of a page number
- [**Asking questions with SQL**](asking-questions-with-sql.md) —
  your own SELECT in the query box and
  through the API, canned queries saved
  in metadata, and the two guards —
  writes refused, slow questions stopped
- [**Facets and metadata**](facets-and-metadata.md) —
  counts that slice a table by genre or
  author, and the metadata file that adds
  titles, descriptions, licences and a
  default sort
- [**Publishing and sharing**](publishing-and-sharing.md) —
  from your own machine to other people:
  what serving wider means, and what
  `datasette publish` would do with a
  cloud account this lab does not have
- [**Recipes**](recipes.md) — explore a
  database file you were handed, share a
  catalogue with a colleague, keep a
  query's answer as a link, check what
  changed between two copies
- [**The neighbours**](the-neighbours.md) —
  the sqlite3 command line, sqlite-utils,
  DuckDB, and spreadsheets: what each does
  with the same file that Datasette
  doesn't, and vice versa
- [**Limits**](limits.md) — read-only by
  design, one file's worth of scale, no
  editing and no accounts in the core
  tool, stated plainly
- [**Troubleshooting**](troubleshooting.md) —
  the search that silently returns
  everything, the 404 with a JSON body,
  the query that took too long, and the
  port that is already taken
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Editing data through Datasette — there
is nothing to cover; the tool does not
do it, and chapter 12 explains what to
use instead. Building the database in
the first place gets one lab chapter
(the fixture) and pointers to the SQLite
guide and sqlite-utils; this guide
begins where a database file already
exists. Running Datasette as a public
service for strangers — hardening,
accounts, traffic — is pointed at, not
taught; this guide stays with one person
publishing data they have the right to
publish, mostly to people they know.

## How to use this guide

Read chapter 1 for the model, and
chapter 2 before installing anything —
knowing which part holds what turns
later confusion into a named problem.
Chapter 4 builds the lab's catalogue and
serves it in the same sitting as the
install, so keep a terminal open.
Chapters 5 to 7 are the daily tools:
browsing, JSON, SQL. Chapter 8 is the
one that turns a served file into a
publication — do not skip the metadata
file and wonder why your site looks
bare. The lab's fixture script and
metadata live in `datasette-lab/`; its
transcripts are `datasette-lab/transcripts/`,
and every output quoted in the chapters
came from those runs.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [SQLite for Mere Mortals](https://paulsullivan33-dev.github.io/sqlite-for-mere-mortals/)
- [DuckDB for Mere Mortals](https://paulsullivan33-dev.github.io/duckdb-for-mere-mortals/)
- [APIs for Mere Mortals](https://paulsullivan33-dev.github.io/api-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/datasette-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/datasette-for-mere-mortals/blob/main/LICENSE-CODE).
