Your `milk-brain` skill is packaged in `milk-brain.zip`. I tested the helper script's `init`, `lint`, `search` and `log-tail` commands, but I did not run the skill itself end to end in a conversation.

It turns the LLM Wiki idea into a workflow Claude follows. Claude builds and maintains a persistent markdown wiki that has three layers: immutable `raw/` sources, an LLM-owned `wiki/`, and a schema file. It covers four operations:

- **Setup:** scaffolds the folders, `index.md`, `log.md`, `overview.md` and a schema tailored to the domain.
- **Ingest:** saves the source, discusses takeaways, writes a source page, and updates entity and concept pages with cross-links. It keeps contradictions visible, updates the index and appends to the log.
- **Query:** reads the index first, answers with `[[citations]]`, and offers to file good answers back as analysis pages.
- **Lint:** the script checks broken links, orphan pages, pages missing from the index and missing frontmatter. Claude then does the judgment checks, such as contradictions, stale claims and missing concept pages.

The zip contains:

- `SKILL.md`: the workflow, with a trigger description covering phrases like "update my wiki", "ingest this" and "what does my wiki say about…"
- `scripts/wiki_tools.py`: the helper script (`init`, `search`, `lint`, `log-tail`)
- `references/page-formats.md`: templates for each page type, the contradiction callout, and index and log entries
- `references/domain-patterns.md`: setup tips for personal, research, book, team and competitive-analysis wikis
- `assets/schema-template.md`: the starter schema that `init` copies into each new wiki

To install it, upload the zip in Settings → Capabilities → Skills, or unzip it into your skills folder.

## Instructions 

Imagine you have a big pile of books, articles, and notes. Normally, if you ask a question, someone has to dig through the whole pile every time to find the answer. That's slow, and nobody remembers what they found last time.

`milk-brain` gives you a **helper who keeps a tidy notebook for you**. Every time you give the helper something new to read, they write what they learned in the notebook, connect it to things they already wrote, and keep it neat. The notebook gets smarter every time.

**How to use it**

1. **Install it.** Upload the `milk-brain.zip` file in Claude's settings under Skills.

2. **Start your notebook.** Just tell Claude what you want to learn about:
   *"Use milk-brain to start a wiki about dinosaurs."*
   Claude makes the folders and a few starter pages.

3. **Give it something to read.** Paste an article or upload a file and say:
   *"Add this to my wiki."*
   Claude reads it, tells you the most interesting parts, and writes it into the notebook. If something disagrees with what it learned before, it points that out instead of hiding it.

4. **Ask questions.** Later you can say:
   *"What does my wiki say about T-Rex?"*
   Claude looks in the notebook, answers, and tells you which pages it used. If the answer is really good, it can save it as a new page.

5. **Do a clean-up check.** Now and then say:
   *"Check my wiki for problems."*
   Claude looks for broken links, lonely pages that nothing connects to, and facts that don't match.

**The one rule to remember:** the original things you gave Claude (the `raw` folder) never get changed. Claude only writes in the notebook (the `wiki` folder).

Keep adding things you read and keep asking questions. The more you use it, the better your notebook gets.