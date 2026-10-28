# Publishing and Sharing

Everything so far ran on one machine, for
an audience of one. This chapter is
about other people — and it is the
chapter where this guide's honesty
matters most, because **the lab did not
do most of it**. The lab has no cloud
account and published nothing. What
follows separates what is known from the
tool's verified behaviour in the lab
from what is known from the project's
documentation, and labels the second
kind every time.

## The gentle end: your own network

`datasette serve` answers whatever
address you tell it to. The lab used
`--host 127.0.0.1`, this machine only.
Starting it with `--host 0.0.0.0` instead
makes it answer on the machine's network
addresses too, so other machines on the
same network can browse it — a catalogue
on a home or office server, readable
from any browser in the building. That
is a decision, not a typo: the moment
the host widens, everyone who can reach
the machine can read **all** the data in
the file, because a bare Datasette has
no accounts and no per-table locks (the
permissions system exists, and is
documented-only in this guide; chapter
12 returns to it). Share on a network
you trust, with data you mean to share
with everyone on it.

Two supporting facts the lab did
verify, because they shape any sharing
arrangement: the server holds no state,
so it can be stopped and started at will
without ceremony; and the metadata, not
the database, carries the publication's
titles, licence and canned queries, so
what you share can be re-titled or
re-licensed by editing one file and
restarting.

## The far end: `datasette publish`

For data that should live on the
internet, Datasette ships a second
command family, `publish`, which wraps
your database files, metadata and chosen
settings into a deployment on a hosting
platform. What the bare tool offers can
be checked without an account — the lab
ran the command and kept the receipt
(transcript `t90`):

```text
$ datasette publish
Usage: datasette publish [OPTIONS] COMMAND [ARGS]...

  Publish specified SQLite database files to the internet along with a
  Datasette-powered interface and API

Options:
  --help  Show this message and exit.

Commands:
  cloudrun  Publish databases to Datasette running on Cloud Run
  heroku    Publish databases to Datasette running on Heroku
(exit code 2)
```

(The exit code is the command saying
*you must pick a target*; it is usage,
not failure.)

Everything beyond that listing is
**documented-only in this guide**,
stated here once and plainly:

- The bundled targets are Google's
  **Cloud Run** and **Heroku**. Each
  needs an account with that platform
  and that platform's own command-line
  tools installed and signed in;
  `datasette publish cloudrun …` and
  `… heroku …` then build and deploy a
  container running your Datasette, and
  print the public address it landed at.
- Further targets — Fly.io is the
  project's own example — arrive as
  **plugins**, separate packages that
  add their name to that Commands list.
  A bare install's short list is the
  plugin system working as designed, not
  a broken install (chapter 3's empty
  `datasette plugins` is the same fact
  seen from the other side).
- A published Datasette is the same
  server this guide ran, at a public
  address: same pages, same `.json`,
  same metadata, same read-only rule.
  Nothing about the data changes; what
  changes is who can reach it, which is
  why chapter 12's limits — decide what
  the file contains *before* it is
  public — belong in this chapter too.

The lab will not walk you through a
deployment it did not perform. The
project's documentation has the
walkthroughs, written against the same
commands whose surface is verified
above; follow them with the model of
chapters 2 and 8 in mind and the steps
will read as assembly, not discovery.

## The unglamorous middle: hand them the file

Do not overlook the option that needs no
chapter in anyone's documentation.
SQLite is one file; Datasette is one
command. Sending a colleague the `.db`
file and this guide's chapter 3 gives
them the entire publication — data,
browsing, API, search — on their own
machine, with no server of yours to run,
secure or feed. Half the sharing in the
world is exactly this, and Datasette's
design quietly assumes it: the file is
the publication; the server is just its
most sociable reader.
