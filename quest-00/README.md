# Quest 0: The First Gate

You are standing in front of the first gate of the Guild.
The gate opens only for adventurers who can **read a README**.

You do not have to read every word.
Look at the headings first, and find the section you need.

## Prerequisites

- Python 3.10 or later
- A terminal (Command Prompt, PowerShell, or Terminal)

To check your Python version, run:

    python --version

## Installation

There is nothing to install.

## Usage

This quest has three stages. Run them in order:

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3

Each stage asks you one question. The answer is somewhere in this repository.

To see which stages you have cleared, run:

    python quest.py --status

> **Note:** The answer to stage 3 is **not** in this file.
> Open `docs/ARCHIVE.md` and look for the heading that begins with **"Deprecated"**.
> Read carefully: old information is not always current information.

When you clear all three stages, you will get a flag.
Submit it in **Guild HQ** with the **Submit a Flag** form.

## Troubleshooting

**`python` is not found**

On macOS, try `python3` instead of `python`.

**`GateClosedError: the gate key is missing`**

The gate needs a key. Create an empty file named `gate.key` in this folder,
and run the stage again.
You do not need to write anything in the file.

**I typed a wrong answer**

That is OK. Run the same stage again.

## Maintainers

This quest is maintained by **Mira**, the keeper of the gate.
If you find a bug in this quest, please open an issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md) to learn how.

## License

This quest is released under the MIT License. See [LICENSE](../LICENSE).
