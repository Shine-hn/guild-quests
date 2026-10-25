"""The ledger of the forge: a small git repository with a merge conflict.

  python ledger.py --setup   make the ledger (or make it again from the start)
  python ledger.py           check the ledger
"""
import argparse
import base64
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "ledger"
RECIPE = "blade.txt"
FOLD = "Fold the iron seven times."
MITHRIL = "Add a drop of mithril."
WORD = "aGFybW9ueQ=="


def git(*args, check=True, smith="Mira"):
    """Run git in the ledger. The setup commits are made by the smiths, not by you."""
    cmd = ["git", "-C", str(LEDGER), "-c", f"user.name={smith}", "-c", f"user.email={smith.lower()}@guild.invalid",
           "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr}")
    return result


def write(lines):
    (LEDGER / RECIPE).write_text("\n".join(lines) + "\n", encoding="utf-8")


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def setup():
    if LEDGER.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(LEDGER, onexc=remove_readonly)
        else:
            shutil.rmtree(LEDGER, onerror=remove_readonly)
    LEDGER.mkdir()
    git("init", "-q")
    git("symbolic-ref", "HEAD", "refs/heads/main")
    git("config", "merge.conflictStyle", "merge")
    write(["Blade recipe", "Step 1: Heat the iron.", "Step 2: (not written yet)", "Step 3: Cool it in water."])
    git("add", RECIPE)
    git("commit", "-q", "-m", "Add the blade recipe")
    git("checkout", "-q", "-b", "bram")
    write(["Blade recipe", "Step 1: Heat the iron.", f"Step 2: {MITHRIL}", "Step 3: Cool it in water."])
    git("commit", "-q", "-am", "Add the mithril step", smith="Bram")
    git("checkout", "-q", "main")
    write(["Blade recipe", "Step 1: Heat the iron.", f"Step 2: {FOLD}", "Step 3: Cool it in water."])
    git("commit", "-q", "-am", "Add the folding step")
    git("merge", "bram", check=False)
    print("The ledger is ready in the 'ledger' folder.")
    print("Two smiths wrote different steps, and git could not merge them.")
    print()
    print("Next:")
    print("    cd ledger")
    print("    git status")


def check():
    if not (LEDGER / ".git").exists():
        print("There is no ledger yet. Run: python ledger.py --setup")
        return 1
    if (LEDGER / ".git" / "MERGE_HEAD").exists():
        print("The merge is not finished yet. Go into the ledger and read the output of `git status`.")
        return 1
    text = (LEDGER / RECIPE).read_text(encoding="utf-8")
    if any(mark in text for mark in ("<<<<<<<", "=======", ">>>>>>>")):
        print(f"{RECIPE} still has conflict markers (<<<<<<<, =======, >>>>>>>). Remove them.")
        return 1
    if FOLD not in text or MITHRIL not in text:
        print(f"Both smiths are right. Keep both of their steps in {RECIPE}.")
        return 1
    if git("rev-list", "--merges", "--count", "HEAD", check=False).stdout.strip() in ("", "0"):
        print("There is no merge commit in the ledger. Run `python ledger.py --setup` and try again.")
        return 1
    if git("status", "--porcelain", check=False).stdout.strip():
        print("Some changes are not committed yet. Read the output of `git status`.")
        return 1
    print("The ledger is clean. The two smiths shake hands.")
    print(f"The secret word is: {base64.b64decode(WORD).decode()}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="The ledger of the forge.")
    parser.add_argument("--setup", action="store_true", help="make the ledger again from the start")
    args = parser.parse_args()
    if shutil.which("git") is None:
        print("git is not found. Install git, or use Codespaces.")
        return 1
    if args.setup:
        setup()
        return 0
    return check()


if __name__ == "__main__":
    sys.exit(main())
