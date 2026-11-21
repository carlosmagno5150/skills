# Wiki Schema — {{DOMAIN}}

This file tells the LLM agent how this wiki works. The LLM and the user co-evolve it.

## Purpose
{{DOMAIN}} knowledge base. The user curates sources and asks questions; the LLM writes and maintains `wiki/`.

## Layers
- `raw/` — immutable sources. Never modify. Images live in `raw/assets/`.
- `wiki/` — LLM-owned markdown. The user reads, the LLM writes.
- This file — conventions and workflows.

## Directory layout
- `wiki/index.md` — catalog of all pages (link + one-line summary), by category. Updated on every ingest.
- `wiki/log.md` — append-only log. Entry format: `## [YYYY-MM-DD] <op> | <title>`.
- `wiki/overview.md` — evolving top-level synthesis.
- `wiki/sources/` — one summary page per source.
- `wiki/entities/` — people, organizations, places, products...
- `wiki/concepts/` — ideas, themes, topics.
- `wiki/analyses/` — filed-back answers, comparisons, charts.

## Page conventions
- YAML frontmatter: `type`, `tags`, `created`, `updated`, `sources` (list).
- `[[wikilinks]]` for all internal references; filenames lowercase-hyphenated.
- Every factual claim traces to a source page or is labeled as synthesis.
- Contradictions are kept visible: cite both sources, mark with a callout, never silently overwrite.

## Ingest workflow
1. Save source to `raw/` (unmodified). 2. Read fully. 3. Discuss takeaways with the user.
4. Write `wiki/sources/<slug>.md`. 5. Update/create entity + concept pages, overview, cross-links.
6. Update `index.md`. 7. Append to `log.md`. 8. Report changes and contradictions.
Mode: one source at a time with user review (change to "batch" if preferred).

## Query workflow
Read `index.md` → read relevant pages → answer with `[[citations]]` → offer to file reusable answers into `wiki/analyses/`.

## Lint workflow
Check contradictions, stale claims, orphans, missing pages/cross-refs, data gaps. Fix safe items; ask before merging/deleting. Log it.

## Domain-specific notes
(Add entity types, templates, emphasis, and preferences here.)
