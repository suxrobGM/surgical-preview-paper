# Localize, Don't Beautify

LaTeX source for the paper *"Localize, Don't Beautify: Region-Confined
Cosmetic-Surgery Previews with Off-the-Shelf Image Editors"* (IEEE conference
format), plus the analysis scripts that produce its tables and figures.

The short version of the paper: hosted image editors like GPT Image 2 can't be
trusted to edit only the part of the face you ask for, but if you mask and
composite the edit yourself on the client, they get surprisingly far. We measure
this with an identity metric and a region-localization metric over real
before/after surgery photos.

## How this repo works

One rule: **no number in the paper is typed by hand.** Everything comes out of
the experiment run data:

```
outputs/runs/*/results.csv  (experiment repo)
        │
        ▼
scripts/aggregate.py  ──►  data/canonical_rows.csv     every scored edit, traceable to its run
                           tables/main_results.tex     Table 1
                           tables/setup_models.tex     model lineup table
                           tables/numbers.tex          \newcommand macros the prose cites
scripts/make_figures.py ─► figures/generated/*.pdf     scatter, boxplots, strip plot
scripts/make_qualitative.py ► figures/generated/*.png  before/after image grids
```

If a result changes, re-run the scripts and the paper updates itself. Editing a
number in a `.tex` file under `tables/` is always the wrong move — it gets
overwritten.

The scripts expect the experiment repo at
`c:\Users\admin\source\repos\plastyvue-poc`; set `PLASTYVUE_POC` to point
somewhere else. Generated tables and figures are committed, so you can build the
PDF without the experiment data.

## Building

You need a TeX distribution with `latexmk` (MiKTeX or TeX Live) and
[uv](https://docs.astral.sh/uv/) for the Python scripts.

```sh
make numbers    # regenerate tables from run data
make figures    # regenerate figures
make pdf        # latexmk -> main.pdf
make all        # all of the above
```

Or skip Python entirely and just run `make pdf` with the committed artifacts.

### Overleaf

Upload the repo as a zip (`git archive -o paper.zip HEAD`), or connect it via
Overleaf's GitHub import. Compiler: pdfLaTeX, main file: `main.tex`. Overleaf
ignores the Python; the committed tables/figures make it compile as-is.

## Before submitting

Open items live in two places:

- `docs/real_face_checklist.md` — the face photos are from licensed before/after
  datasets; the final attribution wording still needs to be filled in.
- `refs.bib` — entries marked `UNVERIFIED` need their author lists / venues
  checked against the publisher pages.

`docs/novelty_notes.md` has the prior-work scan and the claims we deliberately
avoid making — read it before touching the intro or related-work sections.
