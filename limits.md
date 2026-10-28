# Limits

Datasette's limits are mostly its design
seen from the other side, which makes
them easy to state and worth stating
before one of them surprises you.

## It does not edit — anything, ever

No row editing, no adding tables, no
fixing a typo through the web pages.
The server opens database files to read
them, and the query surface refuses
everything that is not a `SELECT`
(chapter 7 watched it). If your workflow
needs visitors to change the data,
Datasette is the wrong tool — not an
incomplete one. The companion pattern is
chapter 11's: another tool writes the
file, Datasette publishes it. Scheduled
that way — regenerate the file, restart
or simply leave the server running
against the new copy as your arrangement
dictates — it is a pattern many real
publications use, but the writing always
happens somewhere else.

## One file is the unit of scale

Datasette serves SQLite files, and
SQLite is a single-file database that
expects modest write traffic and rewards
read-mostly work. For browsing and
querying collections of thousands to
millions of rows it is quick and calm —
the lab's answers landed in single-digit
milliseconds — but it is not a
multi-writer database server like
PostgreSQL, and no arrangement of
Datasette makes it one. Facets and
search add their own costs on very large
tables, and the query time limit
(chapter 7) exists because one expensive
question is everyone's outage on a small
server. If the data outgrows one file's
honest capacity, the file is the thing
to change, not the server in front of
it.

## A bare server has no doors, only walls

Out of the box, anyone who can reach the
server can read everything in the files
it serves, and can run their own SQL
unless you switch `allow_execute_sql`
off. Datasette does have a permissions
and accounts system — actors, tokens,
per-database and per-table rules — and
this guide deliberately did not exercise
it, so treat this limit precisely: the
*default* is openness. Hosting data
privately behind Datasette is possible
and documented by the project; it is not
a thing to improvise from a chapter that
labels it documented-only. On a network
or the internet, the question *who can
reach this address* is your access
control until you have deliberately
built a better one.

## The index must exist before the search does

Search, facets with tidy labels,
canned answers — every convenience in
this guide was prepared by somebody:
the full-text index was built into the
file, the foreign keys were declared in
its schema, the facets and queries were
written into metadata. Datasette
surfaces structure beautifully and
invents none of it. A database with no
foreign keys browses as unrelated
tables; a file with no FTS index has no
search box; that flatness is the file
telling the truth about itself.

## Publishing is someone else's computer

`datasette publish` deploys to platforms
— Cloud Run, Heroku, plugin targets —
which means accounts, bills, and another
organisation's availability now bound
your publication's life. The command is
verified in this guide only as far as
its surface (chapter 9). The data is
yours; the venue is rented. Keep the
file and the metadata, and the
publication can always move house.

## The version on the page

The lab ran 0.65.5. Datasette also
develops in the open toward a 1.0 whose
details shift between alphas; flags,
defaults and page furniture may differ
in the version you install. The bones of
this guide — addresses, `.json`,
metadata, canned queries, read-only —
are the project's longstanding design,
but where a command matters, the
installed tool's own `--help` and the
project's documentation for your version
outrank any guide, this one included.
