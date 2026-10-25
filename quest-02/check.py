"""Checks error messages, and gives you a word when they pass.

  python check.py --part 1
  python check.py --part 2
  python check.py --part 3
  python check.py --part 4 YOUR-ID/YOUR-GAME     (or a path to your main.py)

This checker can only check the form of a message, not how good it is.
Read your messages aloud, and ask yourself: "Would this help a new player?"
"""
import argparse
import ast
import base64
import json
import os
import re
import string
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_LENGTH = 100
SHOP_PLACEHOLDERS = {"command", "item", "price", "money", "limit"}
COLD_WORDS = ["stupid", "idiot", "dumb", "illegal", "fatal", "invalid", "go away"]
ACTION_WORDS = {"try", "type", "use", "check", "choose", "pick", "enter", "say", "look", "go", "run",
                "press", "add", "open", "ask", "come", "drop", "buy", "sell", "wait", "read", "write",
                "find", "keep", "please", "make", "save", "earn", "get"}

# Which messages each part checks, and which placeholders each message must use.
PARTS = {
    1: {"unknown_command": set(), "unknown_item": set(), "no_money": set()},
    2: {"unknown_command": {"command"}, "unknown_item": {"item"}, "no_money": {"price"}},
    3: {"unknown_command": {"command"}, "unknown_item": {"item"}, "no_money": {"price"},
        "empty_command": set(), "already_have": {"item"}, "bag_full": {"limit"}},
}
WORDS = {1: "Y2FsbQ==", 2: "Y29tcGFzcw==", 3: "d2VsY29tZQ==", 4: "a2luZG5lc3M="}


def placeholders(message):
    try:
        return {name for _, name, _, _ in string.Formatter().parse(message) if name is not None}
    except ValueError:
        return None


def tone_problems(message):
    """Part 1 rules: the message is short, calm, and polite."""
    problems = []
    if not message.strip():
        return ["The message is empty. Write a message."]
    if len(message) > MAX_LENGTH:
        problems.append(f"The message is too long ({len(message)} characters). Keep it to {MAX_LENGTH} or less.")
    plain = re.sub(r"\{[^}]*\}", "", message)
    shouting = [w for w in re.findall(r"[A-Za-z]+", plain) if len(w) >= 3 and w.isupper()]
    if shouting:
        problems.append(f"Do not shout. Write '{shouting[0]}' in small letters, or remove it.")
    if "!!" in message:
        problems.append("One '!' is enough. You can also use none.")
    for word in COLD_WORDS:
        if re.search(r"\b" + word + r"\b", message.lower()):
            problems.append(f"'{word}' sounds cold or rude. Say what happened in plain words.")
    return problems


def help_problems(message, required, allowed):
    """Part 2 rules: the message says what happened and what to do next."""
    problems = []
    names = placeholders(message)
    if names is None:
        return ["A '{' or '}' is not closed. A placeholder looks like {item}."]
    if allowed is not None:
        for name in sorted(names - allowed):
            problems.append(f"Unknown placeholder {{{name}}}. You can use: "
                            + ", ".join("{" + a + "}" for a in sorted(allowed)))
    for name in sorted(required - names):
        problems.append(f"Show the player the {name}: add {{{name}}} to the message.")
    if message.rstrip()[-1:] not in (".", "!", "?"):
        problems.append("End the message with '.', '!' or '?'.")
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", message.strip()) if s.strip()]
    if len(sentences) < 2:
        problems.append("Write two short sentences: what happened, and what to do next.")
    first_words = [re.sub(r"^[^A-Za-z]+", "", s).split(" ")[0].lower() for s in sentences]
    if not any(w in ACTION_WORDS for w in first_words) and "you can" not in message.lower():
        problems.append("Tell the player what to do next. Start a sentence with a verb like 'Try', 'Type' or 'Check'.")
    return problems


def check_messages(messages, rules, allowed, full):
    failed = 0
    for key, required in rules.items():
        message = messages.get(key)
        if not isinstance(message, str):
            print(f"[{key}] is missing. Do not delete or rename the keys.")
            failed += 1
            continue
        problems = tone_problems(message)
        if full and not problems:
            problems = help_problems(message, required, allowed)
        if problems:
            failed += 1
            print(f"[{key}] {message!r}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[{key}] OK")
    return failed


def load_shop_messages():
    try:
        return json.loads((HERE / "messages.json").read_text(encoding="utf-8"))
    except ValueError as err:
        sys.exit(f"messages.json is broken: {err}\nRead the line and column, like you did in Quest 1.")


def fetch_game(target):
    """Read main.py from a local path, or from a public GitHub repository (OWNER/REPO)."""
    path = Path(target)
    if path.is_dir():
        path = path / "main.py"
    if path.is_file():
        return path.read_text(encoding="utf-8")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", target):
        sys.exit(f"'{target}' is not a file. Give a path to main.py, or YOUR-ID/YOUR-GAME.")
    url = f"https://github.com/{target}.git"
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    result = subprocess.run(["git", "ls-remote", url, "HEAD"], capture_output=True, text=True,
                            env=env, stdin=subprocess.DEVNULL, timeout=30)
    if result.returncode != 0 or not result.stdout:
        sys.exit(f"Cannot find the repository {url}\nCheck the name. Is the repository public?")
    sha = result.stdout.split()[0]
    try:
        with urllib.request.urlopen(f"https://raw.githubusercontent.com/{target}/{sha}/main.py", timeout=20) as r:
            return r.read().decode("utf-8")
    except OSError as err:
        sys.exit(f"Cannot read main.py from {target}: {err}\n"
                 "Is main.py at the top of the repository? Did you push it?")


def game_messages(source):
    """Find ERRORS = {"key": "message", ...} in the game, and check that the game uses it."""
    try:
        tree = ast.parse(source)
    except SyntaxError as err:
        sys.exit(f"main.py has a syntax error on line {err.lineno}: {err.msg}")
    found = None
    used = False
    for node in ast.walk(tree):
        target = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else getattr(node, "target", None)
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(target, ast.Name) and target.id == "ERRORS":
            try:
                found = ast.literal_eval(node.value)
            except ValueError:
                sys.exit("ERRORS must be a plain dictionary of strings, like {\"no_exit\": \"...\"}.")
        if isinstance(node, ast.Name) and node.id == "ERRORS" and isinstance(node.ctx, ast.Load):
            used = True
    if not isinstance(found, dict):
        sys.exit("Cannot find ERRORS = {...} in main.py. See 'Part 4' in README.md.")
    if not used:
        sys.exit("ERRORS is written, but the game does not use it yet. Print the messages from ERRORS.")
    return found


def main():
    parser = argparse.ArgumentParser(description="Check error messages.",
                                     epilog="Example: python check.py --part 4 your-id/your-game")
    parser.add_argument("--part", type=int, choices=[1, 2, 3, 4], required=True, help="which part to check")
    parser.add_argument("game", nargs="?", help="part 4 only: YOUR-ID/YOUR-GAME, or a path to main.py")
    args = parser.parse_args()

    if args.part < 4:
        failed = check_messages(load_shop_messages(), PARTS[args.part], SHOP_PLACEHOLDERS, args.part >= 2)
    else:
        if not args.game:
            parser.error("part 4 needs your game: python check.py --part 4 YOUR-ID/YOUR-GAME")
        messages = game_messages(fetch_game(args.game))
        failed = check_messages(messages, {key: set() for key in messages}, None, True)
        if len(messages) < 3:
            print(f"ERRORS has {len(messages)} message(s). Write at least 3.")
            failed += 1
        if not any(placeholders(m) for m in messages.values() if isinstance(m, str)):
            print("Use a placeholder in at least one message, like {direction} or {command}.")
            failed += 1

    print()
    if failed:
        print("Not yet. Fix the problems above, and run the checker again.")
        return 1
    print(f"Part {args.part} passed!")
    print(f"The word for stage {args.part} is: {base64.b64decode(WORDS[args.part]).decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
