# Bring Your Own Chess Engine to PyChess!

**Powerful native analysis and community-run BOT opponents**

Ever wished you could analyze your favorite chess variant with the full power of your computer—or challenge an engine built specifically for that variant? Now you can do both on PyChess.

We're introducing **external analysis engines**, which let you connect a native chess engine running on your own computer to the familiar PyChess analysis board. And we're taking the opportunity to highlight another feature that has been available for a while but never received its own announcement: **community-run BOT accounts**, powered by engines hosted by PyChess users.

These features serve different purposes, but share one idea: **bring your own engine**.

## Faster analysis, more choice

PyChess's built-in Fairy-Stockfish engine runs directly in your browser through WebAssembly (WASM). It's wonderfully convenient: there's nothing to install, and you can start analyzing with a click.

But WebAssembly isn't always the fastest way to use your hardware, and Fairy-Stockfish isn't the only engine worth exploring. With the new [PyChess External Engine](https://github.com/pychess/pychess-external-engine) companion application, you can run a native UCI engine on your own computer and see its analysis directly in PyChess.

A native build may search substantially faster than the browser build, depending on the engine, CPU, position and settings. More importantly, it also opens the door to specialized engines for particular variants:

- **[Fairy-Stockfish](https://github.com/fairy-stockfish/Fairy-Stockfish)** — native analysis for its many supported chess variants.
- **[Alice-Stockfish](https://github.com/Belzedar94/Alice-Stockfish)** by Belzedar94 — a dedicated engine for the unusual two-board world of Alice Chess.
- **[MBCA-10x10](https://github.com/romstad/mbca-10x10)** by Tord Romstad — an engine for Grand Chess.
- **[wakwak](https://github.com/Silverrzz/wakwak)** by Silverrzz — an engine for Duck Chess.

Native Fairy-Stockfish and Alice-Stockfish have been tested with the external-analysis integration. Other specialized engines are exciting candidates, but their compatibility depends on the engine's protocol and supported rules; the list above is not a promise that every engine will work out of the box.

### How much faster?

<!-- SCREENSHOT 1: PyChess analysis panel header, browser Fairy-Stockfish WASM, showing engine name, depth, and NPS. -->

<!-- SCREENSHOT 2: Same position and comparable engine/settings, native Fairy-Stockfish, showing engine name, depth, and NPS. -->

*Above: Compare the browser and native analysis headers using real measurements from the same position.*

The **NPS** figure means *nodes per second*, the number of search-tree nodes the engine investigates each second. It's a useful speed comparison for **the same engine** under similar conditions, but higher NPS doesn't necessarily make one *different* engine stronger than another. We'll let the actual screenshots speak for themselves.

## Try a native engine in a few minutes

You'll need [uv](https://docs.astral.sh/uv/getting-started/installation/), a native UCI engine executable, and a PyChess account.

1. Open **[Account → External engines](https://www.pychess.org/account/engines)** and create an engine token. Save it in a local text file.
2. Download or build the engine you want to run.
3. Start the external-engine companion app from a terminal.
4. Open a PyChess analysis board, select your registered engine in the analysis settings, and allow local access if the browser requests it.

For example, to analyze Alice Chess with Alice-Stockfish and its compatible NNUE network:

```bash
uvx pychess-external-engine \
  --engine /path/to/alice-stockfish \
  --setoption EvalFile /path/to/Alice_v1.nnue \
  --token-file /path/to/your-token
```

Or, with native Fairy-Stockfish:

```bash
uvx pychess-external-engine \
  --engine /path/to/fairy-stockfish \
  --token-file /path/to/your-token
```

Replace the paths with those on your computer, and keep the companion app running during analysis. The engine and any required NNUE network are supplied separately. You can switch back to the built-in browser engine at any time.

The companion app has been verified on Linux x86-64 with Chromium, Edge and Firefox. Other platforms and Safari have not yet been fully verified; see the [installation guide](https://github.com/pychess/pychess-external-engine/blob/main/docs/installation.md) and [compatibility notes](https://github.com/pychess/pychess-external-engine/blob/main/docs/compatibility.md) for details.

<!-- SCREENSHOT 3 (OPTIONAL): PyChess analysis panel with Alice-Stockfish selected, showing a real Alice Chess position. -->

## Let other players challenge your engine

What if you want your engine to **play games against people**, rather than just analyze positions for you? That's what [PyChess BOT](https://github.com/gbtami/pychess-bot) is for.

PyChess already supports dedicated BOT accounts operated by members of the community. For a real example, visit **[Alice-Stockfish on PyChess](https://www.pychess.org/@/Alice-Stockfish)**. This isn't an experimental concept: our existing BOT integration has already been used to play games on the site. We simply never gave this feature the announcement it deserved.

A BOT is different from an external analysis engine. **External analysis** sends engine output to *your own analysis board*. A **BOT** connects a dedicated automated account to PyChess, so other users can challenge that account to games. Your engine and the BOT bridge run on a computer you control, and the BOT can accept games while they remain online.

### Set up your own PyChess BOT

First, create a **separate, game-free PyChess account** for your BOT. Accounts with previously played games cannot be converted into BOT accounts. Create a BOT API token with the required permissions; this is **not** the same token as the one used for external analysis.

Install the [PyChess BOT bridge](https://github.com/gbtami/pychess-bot) with `uv`:

```bash
git clone https://github.com/gbtami/pychess-bot.git
cd pychess-bot
uv sync
cp config.yml.default config.yml
```

Edit the **copied** `config.yml`, including the following fields, while retaining its other defaults:

```yaml
token: "YOUR_PYCHESS_BOT_TOKEN"
url: "https://www.pychess.org/"
engine:
  dir: "./engines/"
  name: "YOUR_ENGINE_EXECUTABLE"
  protocol: "uci"
```

Place a suitable native engine executable in the configured directory and set the engine-specific options and accepted variants as described in the [BOT quick-start guide](https://github.com/gbtami/pychess-bot/blob/pychess-bot/docs/pychess-quickstart.md). For an eligible new account, perform the one-time BOT upgrade:

```bash
uv run python lichess-bot.py -u
```

Then start your BOT:

```bash
uv run python lichess-bot.py
```

Yes, the script is still named `lichess-bot.py`! Our [pychess-bot](https://github.com/gbtami/pychess-bot) is a fork of the excellent open-source [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot) project, adapted for PyChess. We deliberately retain some upstream filenames and internal structures to make incorporating upstream improvements easier. **Make sure `url` points to PyChess, not Lichess.**

<!-- SCREENSHOT 4: Real PyChess Alice-Stockfish BOT profile with the BOT badge and challenge action. -->

*Above: A dedicated PyChess BOT account that players can challenge.*

## Your computer, your engine, your choice

These two tools make PyChess more flexible for both players and engine developers. Use a powerful native engine for in-depth analysis, experiment with a specialized engine for an unusual variant, or run a BOT so the community can test its strength over the board.

For external analysis, engine search runs locally between your browser and the companion app; you don't need to expose a public engine server. BOT hosting is separate and connects your automated account to PyChess to play games. As always, engine assistance is **not permitted in ongoing games played by human accounts**.

For full instructions, see [PyChess External Engine](https://github.com/pychess/pychess-external-engine) and [PyChess BOT](https://github.com/gbtami/pychess-bot). Thanks to the developers of Fairy-Stockfish, the specialized variant engines, lichess-bot, and everyone contributing to open-source chess software.

**Happy analyzing—and happy playing against new BOT opponents!**
