#!/usr/bin/env python3
"""Regenerate Functional/spec/*.md from the combined spec, Functional/DhruvaOne-Functional-Spec.md.

The combined file is the master copy. Run this after every change to it and commit both:
    python3 tools/split_spec.py          # rewrite the split files
    python3 tools/split_spec.py --check  # exit 1 if any split file is out of date (for CI)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMBINED = ROOT / "Functional/DhruvaOne-Functional-Spec.md"
OUT = ROOT / "Functional/spec"

# (file, first heading, next heading or None for the end of the document)
PARTS = [
    ("01-02-introduction-and-platform-overview.md", "# 1. ", "# 3. "),
    ("03-identity-management.md", "# 3. ", "# 4. "),
    ("04-tenant-administration-and-feature-control.md", "# 4. ", "# 5. "),
    ("05-ai-dhruva.md", "# 5. ", "# 6. "),
    ("06-app-desktop.md", "# 6. ", "# 7. "),
    ("07-app-mobile.md", "# 7. ", "# 8. "),
    ("08-whatsapp.md", "# 8. ", "# 9. "),
    ("09-cross-cutting-platform.md", "# 9. ", "# 10. "),
    ("10-release-phasing-and-decisions.md", "# 10. ", "# 11. "),
    ("11-website.md", "# 11. ", "# Appendix A"),
    ("appendices.md", "# Appendix A", None),
]


def heading_at(text, prefix):
    i = text.find("\n" + prefix)
    if i < 0:
        sys.exit(f"heading not found: {prefix!r}")
    return i + 1


def render(text):
    files = {}
    for name, start, end in PARTS:
        a = heading_at(text, start)
        b = heading_at(text, end) if end else len(text)
        body = text[a:b].rstrip()
        while body.endswith("---"):
            body = body[:-3].rstrip()
        if name.startswith("01-02"):
            # Keep the document header (title, metadata table) but not the full contents list.
            header = text[: text.index("- [1. ")]
            body = header + "(see the combined document)\n\n---\n\n" + body
        files[name] = body + "\n"
    return files


def main():
    files = render(COMBINED.read_text())
    stale = [n for n, body in files.items() if not (OUT / n).exists() or (OUT / n).read_text() != body]
    if "--check" in sys.argv:
        if stale:
            sys.exit("out of date: " + ", ".join(stale) + " (run python3 tools/split_spec.py)")
        print("split files: up to date")
        return
    for n in stale:
        (OUT / n).write_text(files[n])
    print(f"split files: {len(stale)} rewritten" + (": " + ", ".join(stale) if stale else ""))


if __name__ == "__main__":
    main()
