# Page formats

## Frontmatter (all pages)
```yaml
---
type: source | entity | concept | analysis | overview
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [sources/some-source, sources/another]
---
```

## Source page (`wiki/sources/<slug>.md`)
```markdown
---
type: source
tags: []
created: 2026-01-01
updated: 2026-01-01
raw: raw/<filename>
author: ...
date: ...
---
# <Title>
**One-line summary:** ...

## Key points
- ...

## Notable quotes / data (short, attributed)
- ...

## Entities & concepts touched
[[entities/x]], [[concepts/y]]

## Connections to the wiki
- Supports / extends: [[...]]
- Contradicts: [[...]] — see callout there

## Open questions
- ...
```

## Entity page (`wiki/entities/<slug>.md`)
Short definition → key facts (each with `[[sources/...]]`) → relationships → timeline (if relevant) → open questions.

## Concept page (`wiki/concepts/<slug>.md`)
Definition → current synthesis → competing views → evidence by source → related concepts.

## Analysis page (`wiki/analyses/<slug>.md`)
The question → the answer/synthesis → pages and sources consulted → caveats/gaps → date answered.

## Contradiction callout
```markdown
> [!warning] Contradiction
> [[sources/a]] says X (2025-03); [[sources/b]] says Y (2026-01). Status: unresolved / b supersedes a.
```

## index.md entry
`- [[concepts/foo]] — one-line summary (3 sources, updated 2026-04-02)`

## log.md entry
```markdown
## [2026-04-02] ingest | Article Title
Created: sources/article-title, entities/new-person. Updated: concepts/foo, overview. Flagged: contradiction on concepts/foo.
```
