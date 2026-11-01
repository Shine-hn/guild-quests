# Quest 3: The Silent Oracle

The forge is working again. Mira takes you down a long staircase to a dark hall.
In the middle of the hall sits the **Oracle** of the Guild.

"The Oracle knows many secrets," says Mira. "But it is very strict.
It answers only when you call it in the right way. If you call it the wrong way,
it says nothing useful. Luckily, it always tells you how to call it. Just ask for help."

In this quest, you read **help messages**.
Almost every command-line tool has one. It is the first thing a developer reads.

## Usage

Talk to the Oracle:

    python oracle.py

Then answer the stages:

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3
    python quest.py --stage 4

You can run `oracle.py` as many times as you like.

## Files

| File | What it is |
| --- | --- |
| `oracle.py` | The Oracle. A command-line tool. |
| `archive.py` | Makes the archive of prophecies (stage 4). |

Do not edit `oracle.py` or `archive.py`. Read their help instead.

## How to get help

Most tools show their help when you add `--help` (or `-h`):

    python oracle.py --help

Some tools have **commands** (also called subcommands), like `git commit` or `git log`.
Each command has its own help, and it often shows more options:

    python oracle.py COMMAND --help

## How to read a usage line

The help starts with a **usage** line. It shows how to write the command:

    usage: tool.py [-h] [--color {red,blue}] [--fast | --slow] name [name ...]

| You see | It means |
| --- | --- |
| `[--fast]` | Optional. You can leave it out. |
| `name` (no brackets) | Required. You must write it. |
| `{red,blue}` | Choose one of these: `red` or `blue`. |
| `name [name ...]` | One or more. You can write many names. |
| `--fast \| --slow` | Use only one of them, not both. They are *mutually exclusive*. |
| `COMMAND ...` | A command, and then the options of that command. |

So these are all right:

    python tool.py Mira
    python tool.py --color red Mira Bram
    python tool.py --slow Mira

But this is wrong, because `--fast` and `--slow` are used together:

    python tool.py --fast --slow Mira

Under the usage line, the help explains each option.
`(default: ...)` shows the value that the tool uses when you do not choose one.

At the end, some tools add more notes. Read the help to the last line.

## The archive (stage 4)

The Oracle keeps old prophecies in a git repository called the **archive**.
Five seers wrote fifty prophecies. Each prophecy is one commit.

Make the archive:

    python archive.py --setup

Then go into the `archive` folder and look at the history:

    cd archive
    git log

Fifty commits are too many to read one by one.
`git log` has options to show only the commits you want.

`git log -h` shows a **short** list of options. Some options are not in it.
To see all of them, run `git log --help`, or read the page on the web:
https://git-scm.com/docs/git-log

Look for the options that limit the commits. You can use more than one option at the same time.

If you get lost, run `python archive.py --setup` again. It makes a new archive from the start.

## Troubleshooting

**`python` is not found**

On macOS, try `python3` instead of `python`.

**The Oracle shows `error:` and stops**

Good. That is normal. The Oracle is telling you how to call it.
Read the usage line just above the error.

**How do I set an environment variable?**

An environment variable is a setting that a program can read.
Here, `NAME` and `value` are only examples. Use the real name and value.

In bash (Codespaces, macOS, Linux, Git Bash):

    export NAME=value

In PowerShell (Windows):

    $env:NAME = "value"

The setting stays until you close the terminal. To remove it:

    unset NAME                  # bash
    Remove-Item Env:NAME        # PowerShell

In bash, you can also set it for one command only:

    NAME=value python oracle.py ...

**`git log` does not go back to the prompt**

git shows long output one page at a time.
Press `Space` for the next page, and `q` to quit.

**`git log --help` says "No manual entry"**

The help pages are not installed on your computer.
Read the same page on the web: https://git-scm.com/docs/git-log

## Maintainers

This quest is maintained by **Mira**.
If you find a bug in this quest, please open an issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md) to learn how.

## License

This quest is released under the MIT License. See [LICENSE](../LICENSE).
