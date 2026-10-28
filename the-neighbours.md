# The Neighbours

Datasette is not the only program that
opens a SQLite file, and choosing it
well means knowing what its neighbours
do instead. These characterisations are
from the tools' natures and this series'
own guides where they exist; they are
comparisons, not benchmarks, and none
was re-run for this chapter.

## The sqlite3 command line

SQLite ships with its own **command-line
shell**: you open the file, type SQL,
read text tables back. It is the deeper
tool — it can *change* the file, create
tables, run any SQL there is — and the
blunter one: no pages, no links, no
facets, nothing for a non-SQL reader.
Datasette begins where the shell's
audience ends. The two pair naturally:
build and repair with the shell (or the
next neighbour), publish with Datasette.
The SQLite guide in this series teaches
the shell and the language.

## sqlite-utils

Simon Willison — Datasette's author —
also maintains **sqlite-utils**, a
command-line tool for *building* SQLite
databases: turning CSV and JSON files
into tables, creating full-text search
indexes (the very machinery chapter 5
used, with its exacting opinions about
quotes), adding foreign keys after the
fact, and transforming tables. If
Datasette is the reading room,
sqlite-utils is the workshop next door,
and the standard pipeline is: shape the
file with sqlite-utils, serve it with
Datasette. This guide's fixture was
built with plain Python `sqlite3`
instead, to keep the lab to one
dependency — that is a lab economy, not
a recommendation against the pairing.

## DuckDB

DuckDB, covered by its own guide in
this series, is an analytical database
that queries CSV, JSON and Parquet files
in place and speaks a weightier SQL,
aimed at asking hard questions of large
data quickly. It serves no website and
no API. When the job is *analyse this
file*, DuckDB; when the job is *let
people browse this file*, Datasette.
They compete only in the drawer both
being labelled "tools that open data
files".

## A spreadsheet

For one person and one afternoon, a
spreadsheet opens a table's export and
is instantly familiar — sorting,
filtering, totals. It stops where
Datasette starts: the spreadsheet is a
copy that goes stale, has no addresses
to link to, no API, no foreign-key
names standing next to the numbers, and
no read-only promise for the original.
Exporting from Datasette *to* a
spreadsheet (every table page and query
can be fetched as data a spreadsheet
eats) is a fine workflow; replacing a
publication with one is a downgrade the
recipients feel first.

## A general web framework

Flask, Django and their kin can put any
database on the web, with accounts,
editing, exactly the pages you design —
once you have written and maintained
all of it. Datasette is the same idea
pre-built for the read-only case: the
pages are its opinions, not yours, and
in exchange the distance from *file* to
*website with an API* is one command.
When the data must be edited by its
visitors or the pages must look like
yours, you have outgrown the neighbour
on purpose and the framework is the
right tool; chapter 12 says the same
from the other side.
