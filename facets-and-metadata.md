# Facets and Metadata

A bare `datasette serve` gives you the
data and nothing else: the site is
called by its file names, tables open in
their own order, and visitors fend for
themselves. The **metadata file** is
where a served file becomes a
publication. This chapter takes the
lab's metadata apart piece by piece —
every piece was in force during the
lab's runs, and its fingerprints are on
the transcripts you have already seen.

## The metadata file

The lab's lives at
`datasette-lab/metadata.json` and is
handed to the server at startup:

```bash
datasette serve library.db --host 127.0.0.1 --port 8001 --metadata metadata.json
```

Its shape, trimmed to the parts this
chapter uses:

```json
{
  "title": "Harbour Street Library Catalogue",
  "description": "A small invented library catalogue used by the Datasette guide's lab. Every author and title is fictional.",
  "license": "CC0",
  "source": "The Datasette for Mere Mortals lab",
  "databases": {
    "library": {
      "tables": {
        "books": {
          "description": "Books in the catalogue. author_id points at the authors table.",
          "facets": ["genre", "author_id"],
          "sort_desc": "year"
        },
        "authors": {"description": "Authors of the books in the catalogue."}
      },
      "queries": {"books_with_authors": {"…": "chapter 7"}}
    }
  }
}
```

## What the top level does

`title` names the whole site — it is the
*Harbour Street Library Catalogue* of
the lab's homepage, not `library.db`.
`description` introduces it. `license`
and `source` are statements about the
data's terms and origin, and they do
more than decorate the homepage: chapter
6 watched them ride along inside API
answers (`"source": "The Datasette for
Mere Mortals lab", "license": "CC0"`), so
the terms travel with the data wherever
the data goes. If you publish data,
those two fields are the cheapest
honesty you will ever buy.

Per-table `description` fields appear
under each table's name for visitors,
and `sort_desc: year` on `books` is why
the table opened newest-first in chapter
5 — and why the JSON said so, in
`human_description_en`, rather than
letting the order look accidental.

## Facets: counted slices

A **facet** is a column presented as a
set of counted choices: *genre — Fiction
4, Fantasy 3, History 3, Mystery 2,
Essays 1, Poetry 1*. Clicking one is
just the filter of chapter 5 wearing a
friendlier face; what the facet adds is
the **counts**, computed before you
choose, so a visitor can see the shape
of the table at a glance and never click
into an empty answer.

Declaring `"facets": ["genre",
"author_id"]` for `books` made both
appear on the table page and — the
programmable half — in the table's JSON,
as `facet_results` (transcript `t03`).
Two details from the real answer deserve
attention:

- The facet results carry
  `filtered_table_rows_count`-style
  honesty: each choice lists its count,
  a `toggle_url` that applies or removes
  exactly that filter, and whether it is
  currently `selected`.
- The `author_id` facet does not list
  bare numbers. Its entries read
  `{"value": 1, "label": "Mara Ellison",
  "count": 3}` — the foreign key again,
  with Datasette labelling each id using
  the linked table's row. A facet over a
  foreign key is a list of *people*, with
  book counts. No other tool in the
  lab's kit does that from a bare file
  and a five-word declaration.

Facets are computed by queries against
the table, and on a very large table
they cost time; Datasette also
*suggests* facets for columns whose
values repeat often (the JSON's
`suggested_facets` field was empty in
the lab because the metadata had already
chosen). The metadata's declaration is
the deliberate version of that
suggestion: these are the slices this
publication thinks matter.

## Canned queries live here too

Chapter 7's `books_with_authors` is
defined in this same file, under the
database's `queries`. That placement is
the design in one line: the data lives
in the database file, and *everything
editorial* — what it is called, how it
is sorted, which slices are offered,
which questions are pre-asked — lives
in metadata, where the publisher can
change it without touching the data, and
the data can be replaced without losing
the publication around it.

## Changing metadata means restarting

One operational fact the lab confirmed
by construction: the server reads the
metadata file once, at startup. Edit it,
and nothing changes until the server is
restarted — which, chapter 4 showed, is
safe and instant, because the server
holds nothing of its own. If you adjust
a title and the site disagrees with you,
you are looking at the old process, not
a caching mystery.
