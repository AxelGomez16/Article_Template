# Axel Gomez Article Template

A personal, multi-file LaTeX article/preprint template maintained by
**Axel Gomez** ([@AxelGomez16](https://github.com/AxelGomez16)).

The visual style (typography, two-column layout, header/footer,
author/affiliation blocks, caption style, bibliography formatting) is
adapted from the [Henriques Lab bioRxiv template](https://github.com/HenriquesLab/bioRxiv-template),
released for reuse. The class and files were renamed, reorganized into
multiple files, and stripped of bioRxiv-specific branding so the
template can be reused for any journal/preprint submission while
keeping the same clean design.

## Structure

```
AxelGomez_Article_Template/
├── main.tex                  # Document entry point: title, authors, \input of sections
├── sections/
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── methods.tex
│   ├── results.tex
│   ├── discussion.tex
│   ├── conclusions.tex
│   └── supplementary.tex
├── figures/
│   └── Figure_1.png           # example figure, replace/add your own
├── bib/
│   └── references.bib         # your bibliography (BibTeX)
└── style/
    ├── axelgomez-article.cls  # document class (layout, macros)
    └── axelgomez-bib.bst      # bibliography style (unsrtnat-based)
```

## Usage

1. Edit `main.tex` for title, authors, affiliations, keywords and
   correspondence email.
2. Write each section's content directly inside its file under
   `sections/`. Add new files and `\input{sections/your_file}` them
   from `main.tex` if you need more sections.
3. Add figures to `figures/` and reference them with
   `\includegraphics{your_figure}` (the graphics path is already set).
4. Add citations to `bib/references.bib` and cite with `\cite{key}`.
5. Compile `main.tex` with `pdflatex`/`latexmk` + `bibtex`/`biber`, e.g.:

   ```
   latexmk -pdf main.tex
   ```

## Customization

- `\journalname{...}` in `main.tex` controls the footer label (defaults
  to "Preprint").
- Pass `watermark` as a class option
  (`\documentclass[times, twoside, watermark]{style/axelgomez-article}`)
  to stamp pages with "DRAFT".
- `\leadauthor{...}` sets the surname shown in the running footer.

## Credits & License

- Original design/class: Ricardo Henriques, Henriques Lab
  (`r.henriques@ucl.ac.uk`), adapted from PNAS-style macros.
- `style/axelgomez-bib.bst` is `unsrtnat.bst` by Patrick W. Daly,
  distributed under the LaTeX Project Public License (LPPL).
- Adaptation, restructuring and rebranding: Axel Gomez, 2026.
