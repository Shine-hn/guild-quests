# Guild Quests

Weekly reading quests for the guild. Each week a new quest folder
(`quest-00/`, `quest-01/`, ...) appears in this repository.

This is also an **open source project**. If you find a typo, a broken link,
or a confusing sentence, you can fix it and send a pull request.
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Getting started

You work on **your own copy** of this repository, called a *fork*.

1. Click **Fork** at the top right of this page, then **Create fork**.
2. Clone **your fork** (replace `YOUR-ID` with your GitHub ID):

       git clone https://github.com/YOUR-ID/guild-quests.git
       cd guild-quests

## Before each class: get the new quest

New quests are added to the original repository (we call it *upstream*).
Bring them into your fork:

1. Open your fork on GitHub and click **Sync fork**, then **Update branch**.
2. In your terminal:

       git pull

> **Note:** If `git pull` fails because you changed a file, run `git stash`
> and try again.

## Playing a quest

1. Move into the quest folder and read its `README.md`.
2. Run `quest.py` and answer every stage. At the end, you get a flag:

       FLAG{xxxxxxxxxx}

3. Submit the flag in **Guild HQ** with the **Submit a Flag** form:
   https://github.com/kwaka1208/guild-hq/issues/new/choose

Your flag is made from your GitHub ID, so it works only for you.

## Contributing

- Found a problem? [Open an issue](https://github.com/kwaka1208/guild-quests/issues/new/choose).
- Want to fix it yourself? Read [CONTRIBUTING.md](CONTRIBUTING.md).
- Looking for something to work on? See issues labeled
  [`good first issue`](https://github.com/kwaka1208/guild-quests/labels/good%20first%20issue).

Every merged pull request earns points on the leaderboard.

## License

[MIT](LICENSE)
