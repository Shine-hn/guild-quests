"""Checks for pull requests: title style, protected files, and relative links in Markdown."""
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path

TYPES = ["feat", "fix", "docs", "style", "refactor", "test", "chore"]
TITLE_RE = re.compile(r"^(?P<type>[a-z]+)(\([\w\-]+\))?!?: (?P<subject>.+)$")
PROTECTED = ["quest-*/quest.py", "quest-*/stages.json", ".github/*", "LICENSE"]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")


def check_title(title):
    problems = []
    m = TITLE_RE.match(title.strip())
    if not m:
        return ["The title must look like `type: subject` (example: `docs: fix a typo in quest-00`)."]
    if m.group("type") not in TYPES:
        problems.append(f"Unknown type `{m.group('type')}`. Use one of: {', '.join(TYPES)}.")
    first = m.group("subject").split()[0]
    if re.match(r"^[a-z]+ed$", first.lower()):
        problems.append(f"`{first}` looks like past tense. Use the base form (for example `fix`, not `fixed`).")
    return problems


def changed_files(base, head):
    out = subprocess.run(["git", "diff", "--name-only", f"{base}...{head}"],
                         text=True, capture_output=True, check=True).stdout
    return [f for f in out.splitlines() if f]


def check_protected(files):
    bad = [f for f in files if any(fnmatch.fnmatch(f, p) for p in PROTECTED)]
    if not bad:
        return []
    return ["These files are managed by the maintainer. Please do not change them "
            "(open an issue instead): " + ", ".join(f"`{f}`" for f in bad)]


def check_links(files):
    problems = []
    for name in files:
        path = Path(name)
        if path.suffix.lower() != ".md" or not path.is_file():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue  # web links and anchors are not checked
                file_part = target.split("#", 1)[0]
                if file_part and not (path.parent / file_part).exists():
                    problems.append(f"Broken link in `{name}` line {lineno}: `{target}` does not exist.")
    return problems


def main():
    title = os.environ.get("PR_TITLE", "")
    files = changed_files(os.environ["BASE_SHA"], os.environ["HEAD_SHA"])
    results = [
        ("Title", check_title(title)),
        ("Protected files", check_protected(files)),
        ("Links", check_links(files)),
    ]
    lines = ["| Check | Result |", "|---|---|"]
    failed = False
    for name, problems in results:
        if problems:
            failed = True
            for p in problems:
                print(f"❌ {name}: {p}")
                lines.append(f"| {name} | ❌ {p} |")
        else:
            print(f"✅ {name}: OK")
            lines.append(f"| {name} | ✅ OK |")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## Pull request check\n\n" + "\n".join(lines) + "\n")
    if failed:
        print("\nFix the problems above and push to the same branch. The check will run again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
