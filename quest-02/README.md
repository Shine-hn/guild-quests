# Quest 2: The Kind Error

Mira runs a small shop in the Guild. Players love the shop, but they hate its messages.

"When a player makes a mistake, my shop shouts at them," says Mira.
"Last week, a new adventurer cried and left. Can you rewrite the messages?"

In the last quest, you **read** error messages.
In this quest, you **write** them.

## Usage

Play the shop and see the messages:

    python shop.py

Edit the messages in `messages.json`, and check them:

    python check.py --part 1

When a part passes, the checker gives you a word. Answer the stage with it:

    python quest.py --stage 1

There are four parts. Do them in order.

## Files

| File | What it is |
| --- | --- |
| `shop.py` | Mira's shop. A tiny game. |
| `messages.json` | The messages that the shop shows. **You edit this file.** |
| `check.py` | Checks your messages and gives you a word. |

Do not edit `shop.py` or `check.py`.

## What makes a kind error message?

A kind error message:

1. **is calm.** It does not shout (`ERROR!!!`), and it does not blame the player.
2. **says what happened.** "There is no item called 'sword'."
3. **says what to do next.** "Type 'list' to see what we sell."
4. **is short.** The player wants to play, not to read.

Compare:

| Not kind | Kind |
| --- | --- |
| `INVALID INPUT!!!` | `I don't know the word 'jmup'. Try 'jump'.` |
| `Error: no key.` | `The door is locked. Find a key first.` |

## Placeholders

A message can show what the player typed. Write the name in `{ }`:

    "I don't know the command '{command}'. Type 'list' to see what you can do."

When the player types `dance`, the shop shows:

    I don't know the command 'dance'. Type 'list' to see what you can do.

In `messages.json`, you can use these placeholders:

| Placeholder | What it shows |
| --- | --- |
| `{command}` | What the player typed. |
| `{item}` | The item the player wanted to buy. |
| `{price}` | The price of the item. |
| `{money}` | How much gold the player has. |
| `{limit}` | How many items the bag can hold. |

## Part 1: Stop the shouting

The first three messages in `messages.json` are rude.
Rewrite them so they are calm and polite.

    python check.py --part 1

## Part 2: Help the player

Now make the same three messages helpful.
Each message needs **two short sentences**: what happened, and what to do next.
The checker also asks you to show the player some information with placeholders.

    python check.py --part 2

## Part 3: Write new messages

The last three messages are empty. Write them from the start.
Play the shop to see when each message appears:

| Key | When it appears |
| --- | --- |
| `empty_command` | The player presses Enter without typing anything. |
| `already_have` | The player tries to buy an item that is already in the bag. |
| `bag_full` | The bag is full, and the player tries to buy one more item. |

    python check.py --part 3

## Part 4: Your team's game

Now use what you learned in your team's game.

1. In your game's `main.py`, put the error messages in one dictionary called `ERRORS`.
   Write **at least three** messages, and use a placeholder in at least one of them.
2. Use the messages from `ERRORS` in the game. For example:

       ERRORS = {
           "no_exit": "You cannot go {direction} from here. Look at the room description for the exits.",
           ...
       }

       print(ERRORS["no_exit"].format(direction=direction))

3. Commit and push your change to your team's repository on GitHub.
4. Check your game. Use your team's repository name:

       python check.py --part 4 YOUR-ID/YOUR-GAME

   You can also give a path to your `main.py` on your computer.

Your team works on the same `main.py`. Talk with your team before you edit it,
or you may get a merge conflict. (You know how to fix one now!)

## Troubleshooting

**`messages.json is broken`**

You broke the JSON. Read the line and column in the message. Check for a missing `,` or `"`.

**`KeyError` when I play the shop**

A placeholder name is wrong. Run the checker. It tells you which names you can use.

**`Cannot find the repository`**

Check the name. It is the part after `https://github.com/`, like `mira/dragon-game`.
Your repository must be public.

## Maintainers

This quest is maintained by **Mira**.
If you find a bug in this quest, please open an issue.
See [CONTRIBUTING.md](../CONTRIBUTING.md) to learn how.

## License

This quest is released under the MIT License. See [LICENSE](../LICENSE).
