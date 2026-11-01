"""The archive of the oracle: a small git repository with 50 prophecies.

  python archive.py --setup   make the archive (or make it again from the start)
  python archive.py           check that the archive is ready
"""
import argparse
import base64
import os
import random
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "archive"
SEERS = ["Mira", "Bram", "Tove", "Odo", "Sela"]
TOPICS = ["moon", "dawn", "river", "storm", "dragon", "harvest", "tower", "star", "winter", "crow"]
# One word for each prophecy. The first one belongs to Bram's prophecy about the moon.
WORDS = [
    "c3VuZGlhbA==", "cGViYmxl", "ZmVhdGhlcg==", "a2V0dGxl", "cmliYm9u", "dGhpbWJsZQ==",
    "YWNvcm4=", "YnV0dG9u", "YnVja2V0", "bGFkZGVy", "bWFyYmxl", "bmVlZGxl",
    "cGlsbG93", "c2FkZGxl", "dGVhcG90", "d2FsbnV0", "YW5jaG9y", "YmFza2V0",
    "Y29id2Vi", "Z29ibGV0", "aGVsbWV0", "bGl6YXJk", "bWl0dGVu", "b3lzdGVy",
    "cGFycm90", "cXVpbGw=", "cmFiYml0", "c3Bvb24=", "dHVybmlw", "dmlvbGlu",
    "d2hpc3RsZQ==", "YXByb24=", "YmFycmVs", "Y2FjdHVz", "ZG9scGhpbg==", "ZW5naW5l",
    "ZmFsY29u", "Z2FybGlj", "aGFtbW9jaw==", "aWdsb28=", "amlnc2F3", "a2l0dGVu",
    "bGVtb24=", "bWFnbmV0", "bm9vZGxl", "b3JjaGlk", "cGVwcGVy", "cm9ja2V0",
    "dHVsaXA=", "d2Fnb24=",
]


def git(*args, check=True, seer="Mira", date=None):
    """Run git in the archive. The prophecies are written by the seers, not by you."""
    cmd = ["git", "-C", str(ARCHIVE), "-c", f"user.name={seer}", "-c", f"user.email={seer.lower()}@guild.invalid",
           "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args]
    env = dict(os.environ)
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr}")
    return result


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def prophecies():
    """Every seer writes about every topic once, in a fixed random order."""
    pairs = [(seer, topic) for seer in SEERS for topic in TOPICS]
    pairs.remove(("Bram", "moon"))
    random.Random(3).shuffle(pairs)
    words = [base64.b64decode(w).decode() for w in WORDS]
    chosen = dict(zip(pairs, words[1:]))
    chosen[("Bram", "moon")] = words[0]
    order = pairs[:]
    order.insert(31, ("Bram", "moon"))
    return [(seer, topic, chosen[(seer, topic)]) for seer, topic in order]


def setup():
    if ARCHIVE.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(ARCHIVE, onexc=remove_readonly)
        else:
            shutil.rmtree(ARCHIVE, onerror=remove_readonly)
    ARCHIVE.mkdir()
    git("init", "-q")
    git("symbolic-ref", "HEAD", "refs/heads/main")
    for number, (seer, topic, word) in enumerate(prophecies()):
        path = ARCHIVE / f"{topic}.txt"
        with path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(f"A prophecy by {seer}.\n")
        date = f"2026-01-{1 + number // 10:02d}T{9 + number % 10:02d}:00:00+00:00"
        git("add", path.name)
        git("commit", "-q", "-m", f"Write a prophecy about the {topic}",
            "-m", f"The word of this prophecy is: {word}", seer=seer, date=date)
    print(f"The archive is ready in the 'archive' folder. It has {len(WORDS)} prophecies.")
    print()
    print("Next:")
    print("    cd archive")
    print("    git log")


def check():
    if not (ARCHIVE / ".git").exists():
        print("There is no archive yet. Run: python archive.py --setup")
        return 1
    count = git("rev-list", "--count", "HEAD", check=False).stdout.strip()
    if count != str(len(WORDS)):
        print("The archive looks different. Run `python archive.py --setup` to make it again.")
        return 1
    print(f"The archive is ready. It has {count} prophecies.")
    print("Go into the 'archive' folder, and search it with `git log`.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="The archive of the oracle.")
    parser.add_argument("--setup", action="store_true", help="make the archive again from the start")
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
