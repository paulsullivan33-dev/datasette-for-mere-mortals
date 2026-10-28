# Troubleshooting

Every problem below either happened in
this guide's lab or follows in one step
from something that did. They are
ordered roughly by how likely you are to
meet them.

## Search returns everything, whatever you type

The lab's first fixture build had this
exact disease: `_search=ferryman`
returned all fourteen books instead of
the one whose title matches. Nothing
errored. The database page held the
clue: the `books` table reported
`"fts_table": null` — Datasette had not
recognised the search index as belonging
to `books` at all, so the search
argument was ignored and the table came
back unfiltered.

The cause was one character class in the
index's creation statement. Datasette
recognises an external-content search
table by the way it was declared,
looking for the content table named in
double quotes:

```sql
CREATE VIRTUAL TABLE books_fts
USING fts5(title, content="books", content_rowid="id")
```

The lab had written `content='books'`
with single quotes — perfectly valid
SQL, an index that worked flawlessly
when queried directly, and invisible to
Datasette. **The check:** ask the
database page's JSON whether your table
names an `fts_table`. If it says `null`
and you built the index yourself, read
your `CREATE VIRTUAL TABLE` statement
before you read anything else. The fix
is to rebuild the index with the double
quotes (and rebuild its contents) and
restart the server. Search then returned
exactly one book (transcript `t04`).

## "Table not found" for a table that exists

The API's answer is structured and the
HTTP status agrees (transcript `t90`):

```json
{"ok": false, "error": "Table not found", "status": 404, "title": null}
```

Before doubting the database, doubt the
address: table names are case-sensitive
in the URL, names with spaces or other
special characters arrive URL-encoded,
and the database's own name in the
address comes from the *file* name —
serve `Library-Export.db` and your
addresses begin `/Library-Export`, not
`/library`. The database page's JSON
lists the true names; copy from there.

## "SQL query took too long"

Your question exceeded the time limit —
one second by default — and Datasette
interrupted it rather than letting it
run (transcript `t90`, where the lab's
endless counting query earned exactly
this). Almost always the question, not
the server, is the problem: an unbounded
recursive query, a join with no
condition marrying every row to every
row, an aggregation over an enormous
table with no index. Rewrite the
question tighter. If the question is
legitimately heavy and the site is
yours, the limit is a setting,
`sql_time_limit_ms`, raisable at
startup — know that you are then
letting one visitor's question hold the
server for that long, every time.

## "Statement must be a SELECT"

Not a malfunction: the write guard of
chapter 7 doing its one job. The data
cannot be changed through Datasette by
anyone, including you. Change it with
the tool that built the file, then let
Datasette serve the result.

## The port is already taken

Start a second server on a port the
first still holds and the newcomer
fails to bind and exits, naming the
address it could not have. Pick another
`--port`, or find the first server —
often a terminal you forgot, which is
also why chapters in this guide keep
saying *leave that terminal alone*.
Stopping is CTRL+C there, or the
process number as in transcript `t91`;
a `curl` that answers exit code 7
(connection refused) afterwards is the
all-clear.

## You edited the metadata and nothing changed

The server read the metadata once, at
startup (chapter 8). Restart it. A
restart loses nothing, because the
server holds nothing; if the site still
disagrees with the file afterwards, you
are editing a different file from the
one the running server was started with
— check the `--metadata` path in the
command that started it.

## Rows arrive as lists and your script wanted objects

The API's default shape is lists of
values in column order. Add
`&_shape=objects` (chapter 6) and each
row arrives with named fields. The
`TypeError: list indices must be
integers` in a fresh script against this
API is nearly a rite of passage; the lab
performed it so the guide could warn
you cheaply.
