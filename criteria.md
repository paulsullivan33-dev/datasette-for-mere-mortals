# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's catalogue is invented, authors, titles and all.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 12 names what the tool
   cannot do: no editing by design, one file's worth of scale,
   no access control in a bare server, conveniences that exist
   only where somebody prepared the structure, and publishing
   that rents someone else's computer.
8. **The sharing rule is in the text, early.** Chapter 1 and the
   README state the position plainly — serve on your own
   machine first, publish only data you have the right to
   publish, and treat widening who can reach the server as a
   decision, not a default — before any chapter shows how to
   widen it, and chapter 9 returns to it at the exact point
   where the address stops being private.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a small Ubuntu 24.04 sandbox. Datasette
**0.65.5** was installed with pip into a fresh virtual
environment of its own (Python 3.12.3) and exercised against a
fixture database built for this guide (`datasette-lab/
make_library_db.py`): two tables joined by a foreign key — six
invented authors, fourteen invented books — plus a full-text
search index over the titles. The server ran on loopback only,
port 8001, with the lab's metadata file (`datasette-lab/
metadata.json`). All transcripts live in
`datasette-lab/transcripts/`.

Run for real, with transcripts as evidence:

- Install and version; `datasette plugins` answering `[]` on
  the bare install (t00, and chapter 3).
- Fixture build; the foreign key read back out of the file
  with SQLite's own pragma (t01).
- Serving with metadata, and the homepage and table-page
  titles proving the metadata's title and default sort were in
  force; the database page as JSON, with table counts, both
  directions of the foreign key, the hidden machinery tables
  counted, and `books` naming its search table (t02).
- A table's JSON: the SQL it ran, the filtered count, the
  pagination fields, and the metadata-declared facet results
  for genre and author_id, with foreign-key labels (authors'
  names) inside the facet for author_id (t03).
- Filters in the address: equality on a text column and on the
  foreign key, and the `__gt` operator on pages; full-text
  search returning exactly the matching titles (t04).
- A custom aggregate query through the API and the canned
  query from metadata, join included — including the canned
  query honestly misbehaving with `_size`, which returned all
  fourteen rows and echoed the argument as an unused parameter
  (t05).
- A single row's JSON, the `_shape` argument in its objects
  and arrayfirst forms, and pagination followed verbatim
  through the server's own `next_url` to a correct second page
  (t06).
- The guards and the errors, all firsthand: a DELETE refused
  with "Statement must be a SELECT" and the row count re-read
  to prove nothing moved; an unknown table's structured 404;
  a syntax error delivered in the JSON envelope; an unbounded
  recursive query interrupted by the default time limit; and
  the bare `datasette publish` command surface, exit code and
  all (t90).
- Stopping the server and proving the address closed — curl's
  exit code 7 (t91).
- The lab's own trap, also run for real: the first fixture
  build declared its search index with `content='books'` in
  single quotes, Datasette declined to recognise it
  (`fts_table: null`), and `_search` silently returned the
  whole table. Rebuilding with `content="books"` fixed it;
  chapter 13 and the fixture script both carry the lesson.

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- `datasette publish` beyond its command surface: actually
  deploying to Cloud Run or Heroku needs an account with the
  platform and its CLI tools, neither of which the lab has.
  Plugin-provided targets such as Fly.io are likewise named,
  not used.
- Serving beyond loopback (`--host 0.0.0.0`) and every
  consequence of it; the lab never widened the host.
- Accounts, actors, tokens and the permissions system; the
  guide states the bare server's openness as a limit and does
  not teach the machinery that lifts it.
- The plugin ecosystem beyond the fact of its existence and
  the empty `datasette plugins` result.
- The Docker and Homebrew install routes and any non-pip
  packaging; they converge on the same command.
- The comparison tools in chapter 11 are characterised, not
  benchmarked.

Fixtures are this guide's own and deliberately generic: an
invented library catalogue whose six authors and fourteen
books exist nowhere else. No example is modelled on any real
person, library, network, service or organisation, and the
server was only ever pointed at the lab's own file on the
lab's own loopback address.
