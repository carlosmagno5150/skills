#!/usr/bin/env python3
"""milk-brain wiki helper: init, search, lint, log-tail, index-check.

Usage:
  wiki_tools.py init <dir> [--domain TEXT] [--schema-name CLAUDE.md]
  wiki_tools.py search <wiki-dir> <terms...>
  wiki_tools.py lint <wiki-dir>
  wiki_tools.py log-tail <wiki-dir> [-n 5]
"""
import argparse, datetime, re, sys
from pathlib import Path

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
SKILL_DIR = Path(__file__).resolve().parent.parent


def today():
    return datetime.date.today().isoformat()


def pages(wiki: Path):
    return [p for p in wiki.rglob("*.md")]


def key(p: Path, wiki: Path):
    return p.relative_to(wiki).with_suffix("").as_posix().lower()


def resolve(link: str, keys: set, stems: dict):
    l = link.strip().lower().removesuffix(".md")
    if l in keys:
        return l
    return stems.get(l.split("/")[-1])


def cmd_init(a):
    root = Path(a.dir)
    wiki = root / "wiki"
    for d in ["raw/assets", "wiki/sources", "wiki/entities", "wiki/concepts", "wiki/analyses"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    t = today()
    (wiki / "index.md").write_text(
        f"---\ntype: index\nupdated: {t}\n---\n# Index\n\n## Sources\n\n## Entities\n\n## Concepts\n\n## Analyses\n")
    (wiki / "log.md").write_text(f"# Log\n\n## [{t}] setup | Wiki created\nDomain: {a.domain}\n")
    (wiki / "overview.md").write_text(
        f"---\ntype: overview\ncreated: {t}\nupdated: {t}\n---\n# Overview\n\n_No sources ingested yet._\n")
    tpl = (SKILL_DIR / "assets" / "schema-template.md").read_text().replace("{{DOMAIN}}", a.domain)
    sp = root / a.schema_name
    if not sp.exists():
        sp.write_text(tpl)
    print(f"Initialized wiki at {root} (schema: {sp.name})")


def cmd_search(a):
    wiki = Path(a.wiki)
    terms = [t.lower() for t in a.terms]
    scored = []
    for p in pages(wiki):
        txt = p.read_text(errors="ignore").lower()
        score = sum(txt.count(t) for t in terms) + 5 * sum(t in p.stem.lower() for t in terms)
        if score:
            scored.append((score, p))
    for score, p in sorted(scored, reverse=True)[:15]:
        first = next((l.strip() for l in p.read_text(errors="ignore").splitlines()
                      if l.strip() and not l.startswith(("---", "type:", "tags:", "created:", "updated:"))), "")
        print(f"{score:4d}  {p.relative_to(wiki)}  — {first[:90]}")
    if not scored:
        print("No matches.")


def cmd_lint(a):
    wiki = Path(a.wiki)
    ps = pages(wiki)
    keys = {key(p, wiki) for p in ps}
    stems = {}
    for k in keys:
        stems.setdefault(k.split("/")[-1], k)
    inbound = {k: 0 for k in keys}
    problems = []
    idx = wiki / "index.md"
    idx_links = set()
    for p in ps:
        txt = p.read_text(errors="ignore")
        k = key(p, wiki)
        if not txt.startswith("---") and k not in ("log", "index"):
            problems.append(f"missing frontmatter: {k}")
        for l in LINK.findall(txt):
            r = resolve(l, keys, stems)
            if r is None:
                problems.append(f"broken link in {k}: [[{l}]]")
            else:
                if r != k:
                    inbound[r] += 1
                if p == idx:
                    idx_links.add(r)
    for k, n in sorted(inbound.items()):
        if k in ("index", "log", "overview"):
            continue
        if n == 0:
            problems.append(f"orphan (no inbound links): {k}")
        elif k not in idx_links and idx.exists():
            problems.append(f"not listed in index: {k}")
    print("\n".join(problems) if problems else "Lint clean: no mechanical problems found.")
    print(f"\n{len(ps)} pages checked. Now do the judgment checks: contradictions, stale claims, missing concept pages, gaps.")


def cmd_log_tail(a):
    log = Path(a.wiki) / "log.md"
    heads = [l for l in log.read_text().splitlines() if l.startswith("## [")]
    print("\n".join(heads[-a.n:]))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("dir"); s.add_argument("--domain", default="General")
    s.add_argument("--schema-name", default="CLAUDE.md"); s.set_defaults(f=cmd_init)
    s = sub.add_parser("search"); s.add_argument("wiki"); s.add_argument("terms", nargs="+"); s.set_defaults(f=cmd_search)
    s = sub.add_parser("lint"); s.add_argument("wiki"); s.set_defaults(f=cmd_lint)
    s = sub.add_parser("log-tail"); s.add_argument("wiki"); s.add_argument("-n", type=int, default=5); s.set_defaults(f=cmd_log_tail)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
