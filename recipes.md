# Recipes

Each recipe is a small job the lab's
verified pieces assemble into. Commands
are the ones the chapters proved; where
a recipe leans on something
documented-only, it says so in its own
text.

## Explore a database file you were handed

Someone sends you `mystery.db` and a
shrug. Serve it before you study it:

```bash
datasette serve mystery.db --host 127.0.0.1 --port 8001
```

Open the homepage: tables and row counts
at a glance. Open the database's JSON
(`/mystery.json`) for the machine's-eye
version — every table's columns, primary
keys, and the foreign keys between them,
which is the file's own account of how
its parts connect. Facets will suggest
themselves on repetitive columns; the
query box answers *what is the biggest /
oldest / most common* questions in
minutes. You now know the file's shape
well enough to write real code or real
SQL against it. Stop the server with
CTRL+C; the file is untouched, because
it always was going to be.

## Share a catalogue with a colleague

The lab's own arrangement, minus the
lab: give them `library.db`,
`metadata.json`, and two lines.

```bash
pip install datasette
datasette serve library.db --metadata metadata.json
```

They get the titled site, the facets,
the canned query — the publication, not
just the data. If they only need the
data, the `.db` file alone suffices; if
they need it on the building's network,
chapter 9 covers the `--host` decision
and what it does and does not protect.

## Keep a question's answer as a link

Any filter, search or query is an
address, so an answer you will want
again is a bookmark, not a procedure.
*The long books* is
`/library/books?pages__gt=350`; *this
author's books, as JSON, for the
spreadsheet script* is
`/library/books.json?author_id=1&_shape=objects`.
When the answer changes because the
data changed, the link is still right —
it asks the question afresh each time.
For questions too complex for a filter,
make them a canned query (chapter 7) and
link to that instead: the link stays
short, and the SQL can be improved later
without breaking anyone's bookmark.

## Watch a table change between two copies

Serve yesterday's copy and today's on
two ports:

```bash
datasette serve old.db --port 8001
datasette serve new.db --port 8002
```

and fetch the same table's JSON from
both into two files, then `diff` them.
Because the JSON is stable, sorted the
way you ask it to be (the `_sort_desc`
argument that chapter 6's pagination
links carry does in the address what
the metadata did in chapter 8),
the diff shows rows, not noise: what
arrived, what left, what changed. For
anything bigger this becomes a script
against chapter 6's pagination — the
shape of the job does not change.

## Publish the club's open data (with the honest caveat)

The pieces: a database file you are
allowed to publish, a metadata file with
a title, a description, a `license` that
says what others may do with the data,
and canned queries for the questions
everyone asks. The last step — an actual
`datasette publish` to Cloud Run or
Heroku — is **documented-only in this
guide**, because the lab holds no cloud
account; chapter 9 shows the verified
command surface and names what the
project's documentation must supply.
What this guide can certify is that
everything on your side of that step is
real and ready: if it serves correctly
on `127.0.0.1`, it is the same server
the world would meet.
