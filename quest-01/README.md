# Quest 1: The Broken Forge

You passed the first gate. Mira takes you to the forge of the Guild.

"Our smith left on a trip, and the forge is broken," says Mira.
"Every time I start it, it shows a long message and stops.
Can you read the message and fix the forge?"

In this quest, you read **error messages**.
An error message is not a wall. It is a map that tells you where to look.

## Usage

Start the forge:

    python forge.py

Then answer the stages:

    python quest.py --stage 1
    python quest.py --stage 2
    python quest.py --stage 3
    python quest.py --stage 4
    python quest.py --stage 5

You can run `forge.py` as many times as you like.

## Files

| File | What it is |
| --- | --- |
| `forge.py` | Starts the forge. |
| `smithy.py` | Does the real work: takes materials, readies the anvil, and lights the fire. |
| `recipes.json` | What each item needs. |
| `storehouse.json` | The materials the Guild has now. |
| `anvil.json` | Information about the anvil. |
| `ledger.py` | Makes and checks the ledger (stage 5). |

You may edit `storehouse.json` and `anvil.json`, and create new files in this folder.
Do not edit `forge.py` or `smithy.py`. The forge is not broken in the code.

## How to read a traceback

When Python stops with an error, it prints a **traceback**:

    Traceback (most recent call last):
      File "start.py", line 3, in <module>
        main()
      File "start.py", line 2, in main
        open_door()
    NameError: name 'open_door' is not defined

- "most recent call last" means the newest step is at the **bottom**.
- The **last line** shows the name of the error and a short message.
- The lines above it show the path the program took to get there.
- Some lines may point to Python's own files (for example, `json/decoder.py`).
  Your problem is usually not there. Look for the files in this folder.

So, read a traceback **from the bottom up**.

Sometimes one error causes another error.
Then Python prints two tracebacks, and puts a sentence between them.
Read that sentence carefully: it tells you which error came first.

## The ledger (stage 5)

The forge keeps its recipes in a small git repository called the **ledger**.
Two smiths, Mira and Bram, added a step to the same recipe at the same time.
Both of their steps are right, so the recipe needs **both** of them.

Make the ledger:

    python ledger.py --setup

Then go into the `ledger` folder and use git to finish the merge.
git tells you what to do. Read its messages carefully.

When you think you are done, go back to this folder and check the ledger:

    python ledger.py

If you get lost, run `python ledger.py --setup` again. It makes a new ledger from the start.

## Troubleshooting

**`python` is not found**

On macOS, try `python3` instead of `python`.

**I fixed something, but the forge still stops**

Good. That is normal. Read the new error message. It may be a different error.

**`git commit` opens a strange screen**

git opened a text editor for the commit message. If you see `~` at the start of
many lines, you are in Vim. Type `:wq` and press Enter to save and close it.
Next time, you can give the message on the command line:

    git commit -m "Merge the mithril step"

## Maintainers

This quest is maintained by **Mira**.
If you find a bug in this quest, please open an issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md) to learn how.

## License

This quest is released under the MIT License. See [LICENSE](../LICENSE).
