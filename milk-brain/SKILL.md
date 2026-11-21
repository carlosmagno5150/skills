---
name: milk-brain
description: Build and maintain a persistent, LLM-written personal knowledge base (an interlinked markdown "wiki") that compounds over time instead of re-retrieving from raw documents on every question. Use this skill whenever the user wants to set up a wiki / second brain / knowledge base / research notebook / book companion / team wiki, ingest a new source (article, paper, transcript, note, journal entry) into an existing wiki, ask a question against their wiki, file an answer back into it, or lint / health-check it. Also trigger on "milk-brain", "LLM wiki", "update my wiki", "add this to my notes", "ingest this", "what does my wiki say about...", or "check my wiki for contradictions" — even if the user never says the word "skill".
---

# milk-brain: a persistent, compounding LLM wiki

## The core idea

Normal RAG rediscovers knowledge from raw documents on every question. Nothing accumulates.
milk-brain is different: **you (Claude) incrementally build and maintain a wiki** — a structured,
interlinked folder of markdown files sitting between the user and their raw sources. When a source
arrives, don't just index it: read it, extract the key information, and **integrate it into the
existing wiki** — update entity pages, revise topic summaries, flag contradictions with older claims,
strengthen or challenge the evolving synthesis. Knowledge is compiled once and kept current.

The wiki is a persistent, compounding artifact. Cross-references are already there, contradictions
already flagged, synthesis already reflects everything read.

**Division of labor:** the user sources, explores, and asks good questions. You do the grunt work —
summarizing, cross-referencing, filing, bookkeeping. The user rarely (or never) edits the wiki by hand.

## Three layers

| Layer | What | Who owns it |
|---|---|---|
| `raw/` | Source documents (articles, papers, images, data). **Immutable.** Read, never modify. | User |
| `wiki/` | LLM-generated markdown: source summaries, entity pages, concept pages, comparisons, overview, synthesis. | You, entirely |
| Schema (`CLAUDE.md` / `AGENTS.md`) | Conventions + workflows for this specific wiki. | Co-evolved |

Default layout (adapt to the domain; record any change in the schema):

```
my-wiki/
├── CLAUDE.md          # the schema (or AGENTS.md for non-Claude agents)
├── raw/               # immutable sources
│   └── assets/        # downloaded images
└── wiki/
    ├── index.md       # content catalog
    ├── log.md         # append-only chronological log
    ├── overview.md    # evolving top-level synthesis
    ├── sources/       # one summary page per ingested source
    ├── entities/      # people, orgs, places, products, characters...
    ├── concepts/      # ideas, themes, topics
    └── analyses/      # filed-back answers, comparisons, charts
```

## First: figure out which situation you're in

1. **No wiki yet** → run *Setup*.
2. **Wiki exists** (look for `CLAUDE.md`/`AGENTS.md` + `wiki/index.md`) → **read the schema and
   `index.md` and the last ~5 log entries first**, then do what the user asked: *Ingest*, *Query*, or *Lint*.
3. Wiki exists but the user's files are in an upload folder or not in the container → copy/work
   in a writable folder, and at the end give the user the updated wiki (zip it, or present changed files).

Always follow the wiki's own schema if it differs from the defaults here. The schema wins.

## Setup

1. Ask (briefly, max 2–3 questions; infer the rest) what the domain is: personal, research topic,
   book companion, team/business, competitive analysis, trip, course notes, hobby.
2. Run `python scripts/wiki_tools.py init <dir> --domain "<domain>"` to scaffold folders, `index.md`,
   `log.md`, `overview.md`, and a starter schema (from `assets/schema-template.md`).
3. Tailor the schema: add domain-specific entity types, page templates, and emphasis
   (read `references/domain-patterns.md` for ideas per domain).
4. Log the setup: `## [YYYY-MM-DD] setup | Wiki created`.
5. Tell the user where to put sources and how to ingest. Mention that the folder is plain
   markdown, so it opens nicely in Obsidian and works as a git repo.

## Operation 1 — Ingest

Trigger: user adds a source ("ingest this", "add this article", pastes text, uploads a file).

Default workflow (one source at a time, user in the loop — the schema may say otherwise, e.g. batch mode):

1. **Place the source** in `raw/` unmodified (if the user pasted text, save it as a markdown file there
   with a sensible name; never edit existing raw files).
2. **Read it fully.** For PDFs/docx/images, use the appropriate file-reading approach first.
3. **Discuss key takeaways** with the user in a few lines — what's new, what's surprising,
   what contradicts the wiki. Ask what to emphasize only if it truly matters.
4. **Write a source summary page** in `wiki/sources/` (see `references/page-formats.md`).
5. **Update existing pages** — this is the real work. A single source commonly touches 10–15 pages:
   - Create or update **entity** and **concept** pages mentioned in the source.
   - Revise topic summaries and `overview.md` if the synthesis shifts.
   - **Flag contradictions** explicitly where new data disagrees with old claims
     (keep both claims, cite both sources, mark the status — don't silently overwrite).
   - Add `[[wikilinks]]` both ways between related pages.
6. **Update `index.md`** (add new pages; refresh one-line summaries of changed ones).
7. **Append to `log.md`**: `## [YYYY-MM-DD] ingest | <Source title>` + 2–4 lines listing pages created/updated.
8. **Report back concisely**: what was added, what changed, any contradictions or open questions.

Rules of thumb:
- Every claim on a wiki page should trace to a source page (`[[sources/...]]`) or be marked as synthesis/speculation.
- Prefer updating an existing page over creating a near-duplicate. Search the index first.
- Don't invent facts. If the source is ambiguous, say so on the page.
- Images: if the source has local images, read the text first, then view the relevant images separately.

## Operation 2 — Query

Trigger: user asks a question about the knowledge in the wiki.

1. Read `index.md` to find candidate pages (use `scripts/wiki_tools.py search "<terms>"` if the wiki is larger
   than the index can handle).
2. Read the relevant pages (and drill into source pages when precision matters).
3. Synthesize an answer **with citations** to wiki pages (`[[page]]`). Choose the form that fits:
   markdown, comparison table, timeline, chart (matplotlib), slide deck (Marp markdown), etc.
4. Be explicit about gaps: what the wiki doesn't know, what's contradicted, what a web search could fill.
5. **File good answers back.** If the answer is a reusable synthesis, comparison, or discovered connection,
   offer to save it (or just save it if the schema says so) as a page in `wiki/analyses/`, add it to
   `index.md`, link it from related pages, and log it: `## [YYYY-MM-DD] query | <Question>`.
   Explorations should compound just like ingested sources do.

## Operation 3 — Lint

Trigger: user asks for a health check, or periodically after many ingests.

Run `python scripts/wiki_tools.py lint <wiki-dir>` for the mechanical checks (broken links, orphans, pages
missing from the index, missing frontmatter), then do the judgment-based checks yourself:

- Contradictions between pages
- Stale claims superseded by newer sources
- Important concepts mentioned repeatedly but lacking their own page
- Missing cross-references
- Thin pages that deserve expansion
- Data gaps that a web search or new source could fill

Fix the safe stuff directly (links, index entries, obvious cross-refs). **Ask before** resolving
contradictions or deleting/merging pages. End with a short list of suggested new questions and sources
to look for. Log it: `## [YYYY-MM-DD] lint | <summary>`.

## Index and log conventions

- **`index.md`** — content-oriented catalog. Each page: link + one-line summary (+ optional date / source count),
  grouped by category (Sources, Entities, Concepts, Analyses). Update on **every** ingest and filed query.
  This is what you read first when answering a query.
- **`log.md`** — append-only, chronological. Every entry starts with a consistent, greppable prefix:
  `## [YYYY-MM-DD] <op> | <title>` where `<op>` ∈ `setup | ingest | query | lint | note`.
  `grep "^## \[" wiki/log.md | tail -5` should give the last five events. Never rewrite old entries.

## Page conventions (summary — details in `references/page-formats.md`)

- Markdown with YAML frontmatter (`type`, `tags`, `created`, `updated`, `sources`) so Obsidian Dataview works.
- Obsidian-style `[[wikilinks]]`; lowercase-hyphenated filenames.
- Keep pages focused; link rather than duplicate.
- Note confidence and conflicts inline (e.g. `> [!warning] Contradiction: ...`).

## Optional tooling

- `scripts/wiki_tools.py` provides `init`, `search`, `lint`, `log-tail`, `index-check` — a naive
  but dependable toolkit. Use `search` once the index alone stops being enough.
- For serious scale, suggest a local hybrid search engine such as **qmd** (BM25 + vector + reranking, CLI + MCP).
- Handy for the user: Obsidian (browse + graph view), Obsidian Web Clipper (articles → markdown),
  Marp (slides from markdown), Dataview (queries over frontmatter).

## Communication style

- Be concise after each operation: what changed, what's notable, what's next.
- Keep the user in charge of *what to learn and ask*; you own *how it's filed*.
- Never mention internal mechanics unless useful; just do the bookkeeping well.
- If the user's wiki conventions evolve, update the schema file and say so in one line.
