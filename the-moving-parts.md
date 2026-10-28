# The Moving Parts

Datasette has few parts, and most
confusion about it is really confusion
about which part holds what. This
chapter names them before any procedure
depends on them.

## The server

`datasette serve` starts a **web
server**: a program that waits at an
address and answers requests. It runs
in the foreground of your terminal until
you stop it, and it holds no data of its
own between runs — stop it, start it
again, and everything is as it was,
because everything lives in the database
file. The lab started it like this:

```bash
datasette serve library.db --host 127.0.0.1 --port 8001 --metadata metadata.json
```

`--host 127.0.0.1` means *answer only
this machine*. That is the safe default
for learning, and this guide never
widens it: serving data to other
machines is a decision chapter 9 talks
about openly rather than a flag flipped
in passing.

## Databases, tables, rows

One server can serve several database
files at once; each file keeps its own
name as the first part of its addresses.
The lab served one, `library.db`, so its
addresses begin `/library`. Inside a
database:

- A **table** page (`/library/books`)
  shows the rows as a grid, with the
  tools of chapters 5 and 8 around it.
- A **row** page (`/library/books/5`)
  shows one row, found by its **primary
  key** — the column, usually called
  `id`, whose value is unique to the row.
- A **foreign key** is a column that
  points at another table's primary key.
  The lab's `books.author_id` points at
  `authors.id`, and Datasette uses that
  fact everywhere: the number renders as
  a link, the author's name appears next
  to it, and filters and facets can speak
  in names instead of numbers.

Nothing about this structure is
Datasette's invention — it is read out
of the database file itself, which is
why a file you have never seen before
still arrives fully browsable.

## The `.json` switch

Add `.json` to almost any address and
the same content arrives as JSON instead
of a page: `/library/books.json`,
`/library/books/5.json`, the database
page, even the home page. What changes
is the shape of the answer, not its
content: the JSON carries the rows, the
counts, the filters that produced them,
and the SQL Datasette actually ran.
Chapter 6 takes the JSON API apart.

## Queries

Above the tables sit **queries** —
questions in SQL. Some are yours, typed
into the query box on the database page
or written into an address (chapter 7).
Some are **canned queries**: SQL saved
ahead of time in the metadata file,
given a name and a title, so a visitor
can run *books with their authors*
without knowing any SQL at all. Both
kinds are read-only and both are
guarded: a question that runs too long
is stopped, and anything that is not a
`SELECT` is refused.

## Metadata

A **metadata file** — JSON given with
`--metadata` — describes the publication
around the data: the site's title, a
description and licence for the whole
thing and for individual tables, each
table's default sort, which columns
become **facets** (the counted slices of
chapter 8), and the canned queries.
Datasette itself is software, not a
publisher; the metadata is where the
publishing lives.

## Plugins

Features Datasette does not have are
added as **plugins** — separate Python
packages that hook into the server.
Publishing targets beyond the two
bundled ones, extra ways to display
data, map views, and more live there.
The lab installed no plugins and this
guide teaches none; where a chapter
depends on the plugin ecosystem merely
existing, it says so and labels it
documented-only. The command
`datasette plugins` lists what is
installed; in the lab it answered with
an empty list, `[]`.

## Which part holds what

| Question | The part that answers |
|---|---|
| Who may connect? | The `--host` and `--port` you started the server with |
| What data is shown? | The database file — Datasette adds nothing and changes nothing |
| Why does this column link to a name? | The foreign key stored in the file |
| Why is the site called that? | The metadata file |
| Why does this table open sorted by year? | The metadata file |
| Where did that saved question come from? | The metadata file's canned queries |
| Why can't I edit this row? | The design — see chapter 12 |
| How would I put this on the internet? | `datasette publish` and its targets — chapter 9 |
