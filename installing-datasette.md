# Installing Datasette

Datasette is a Python program, and it is
installed the ways Python programs are:
with pip, from an operating system's
packages, in a Docker container, or with
the project's other packaged routes.
This guide's lab used pip into a
**virtual environment** — a private
folder holding the program and its
libraries, so the install touches
nothing else on the machine and can be
deleted by deleting the folder. That is
the route taught here; whichever route
you take, you end at the same single
command, `datasette`.

## The pip install

You need Python 3.8 or newer. On a
Debian or Ubuntu machine:

```bash
sudo apt install python3 python3-venv
python3 -m venv ~/datasette-venv
~/datasette-venv/bin/pip install datasette
~/datasette-venv/bin/datasette --version
```

The lab ran the last command against
**Datasette 0.65.5** on Python 3.12.3
(transcript `t00` in the lab folder):

```text
$ datasette --version
datasette, version 0.65.5
```

On Windows and macOS the same pip route
works from a terminal with Python
installed; in the venv route the command
lives in the venv's `bin` folder
(`Scripts` on Windows). Either call it
by its full path, as the commands above
do, or activate the environment first
and plain `datasette` will work. Every
later chapter writes plain `datasette`
and means whichever of those you chose.

## Checking the moving parts

Two more commands are worth meeting now,
while nothing can go wrong yet:

```bash
datasette --help
datasette plugins
```

The first lists the subcommands —
`serve` is the one this guide lives in,
and `publish` gets its chapter later.
The second lists installed plugins. A
fresh install has none that add commands
of their own, and in the lab it printed
an empty list:

```text
$ datasette plugins
[]
```

That emptiness matters in chapter 9:
publishing targets beyond the bundled
two arrive as plugins, so a `publish`
that seems to offer very little is not
broken — it is unextended.

## The other routes, honestly

The official documentation also offers a
Docker image and a Homebrew package, and
operating-system packagers carry their
own builds. The lab used none of them
and this guide does not pretend
otherwise; they end at the same
`datasette` command with the same
behaviour, and everything after this
chapter applies unchanged. If the
version you install differs from the
lab's 0.65.5, expect small differences
in page furniture, not in the model of
chapter 2 — addresses, `.json`, metadata
and read-only are the tool's bones, not
one release's decoration.
