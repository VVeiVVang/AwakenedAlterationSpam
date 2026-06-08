# Awakened Alteration Spam

## Warning: Read This Before Using

### Intention

Alteration orbs in Path of Exile are a legitimate crafting mechanic available to all players. In practice, using them is extremely difficult when rolling for low-probability mods: there is no built-in way to stop rolling automatically when a target mod appears, which means a single misclick can undo all that work. This makes the mechanic unreliable for anything that requires a high number of attempts to hit.

This script exists solely to address that gap — it stops rolling when your target mod is hit, preventing misclicks. It is intended as a developer reference and for personal crafting use. It is not intended to provide an economic advantage, automate farming, or facilitate market manipulation.

This declaration applies to the developer and to anyone using this tool.

### Legal Risk and GGG Policy

**Using this script may result in a permanent ban from Path of Exile. The developer takes no responsibility for any consequences to your account.**

Path of Exile's [Terms of Use, Clause 7(c)](https://www.pathofexile.com/legal/terms-of-use-and-privacy-policy) explicitly states:

> "Utilise any automated software or 'bots' in relation to your access or use of the Website, Materials or Services."

GGG's [forum guidance on macros](https://www.pathofexile.com/forum/view-thread/2077975) further clarifies that scripts are only acceptable if they produce a single server-side action per keypress. Timer-based loops and multi-action sequences are not permitted under that standard. This script runs an automated loop with repeated clicks, which falls outside what GGG considers acceptable.

Good intentions do not change the policy. Using this tool is your decision and your risk.

### Continued Support

This project is maintained in good faith. If it becomes clear that the tool is being widely used outside its intended purpose, or if GGG explicitly deems this category of script illegitimate, development and support will stop. The goal was never to ship something that causes harm to the game or its community — if the evidence points that way, the right call is to pull it.

### How GGG May Detect This

GGG's Privacy Policy explicitly states they collect your **running process list (PC only)** as part of anti-cheat monitoring. If this script is running while you play, it is potentially visible to their systems regardless of what it is doing.

Community reports also indicate server-side detection of abnormally frequent or regular input patterns consistent with automated loops. There is no guaranteed safe way to run automation tools alongside Path of Exile.

---

## About

A lightweight Python script that rolls an item with alteration and augmentation orbs until a user-defined regex matches anywhere in the item tooltip. When a match is found the script stops and stays ready — press `=` again to start a new session without restarting the script.

## Features

- Reads item tooltip via `Ctrl+C`
- Matches a regex against the full item text
- Automatically uses an Augmentation Orb when an affix slot is open (optional, on by default)
- Holds `Shift` automatically so you stay in orb-spam mode
- Stops on match and waits for the next session — no need to restart
- Stop mid-roll at any time with `-`
- Per-session orb cap counts every orb used (alt + aug combined)
- Type `?` at any startup prompt for inline help

## Requirements

- Python 3.x

## Installation

1. Install dependencies

```bash
pip install pyautogui pyperclip keyboard
```

2. Clone this repository

```bash
git clone https://github.com/VVeiVVang/AwakenedAlterationSpam.git
cd AwakenedAlterationSpam
```

## Usage

> **Note:** An older video demo is available [here](https://youtu.be/WtSM1Micxlc?si=9efSIHJaNv3YiaWe) but reflects an earlier version of the script. The workflow has changed — use it as a rough reference only.

1. Run the script

```bash
python AwakenedAlterationSpam.py
```

2. At startup you will be prompted for a few things. Type `?` at any prompt to see inline help for that question.

Whether to allow Augmentation Orbs (default yes):

```
Allow Augmentation Orb? [Y/n]:
```

The item base name — **only asked when Augmentation Orbs are enabled.** This is the base item with no affixes; everything before it is treated as the prefix and everything after as the suffix, which is how the script detects an open affix slot:

```
Enter item base name: Kinetic Wand
```

> For example, if the item reads `Humming Kinetic Wand of Waning`, the base is `Kinetic Wand` (`Humming` is the prefix, `of Waning` is the suffix).

A per-session orb cap — the script auto-stops after this many orbs are used in total (alt + aug combined):

```
Enter max orbs per session [40]: 100
```

A regex pattern to match against the item tooltip (same syntax as your loot filter):

```
Enter regex to match: Merciless|Dictator
```

3. In-game setup

- Right-click the Alteration Orb to enter orb-spam mode (the cursor changes)
- Hover over the item you want to roll
- Press `=` — the script takes over from here

The script will:

- Hold `Shift` automatically (you do not need to hold it yourself)
- Copy the item tooltip with `Ctrl+C`
- Match the full tooltip text against your regex — stop if found
- Use one orb per cycle: an Augmentation Orb (hold `Alt` + click) if aug is enabled and an affix slot is open, otherwise an Alteration Orb to reroll. After an aug fills a slot, the next cycle naturally rolls an Alteration Orb.
- Stop and release `Shift` when a match is found, then print `Press = to start again`

4. Controls

| Key | Action |
|-----|--------|
| `=` | Start rolling |
| `-` | Stop mid-roll |
| `Ctrl+C` | Exit the script entirely |

5. After a match is found

The script stays running. You do not need to tab back to the terminal and restart. Just set up the next item in-game and press `=` again.

## Notes

- Requires PoE to be running in windowed or borderless windowed mode.
- The regex matches against the full item tooltip text, not just the item name. This means mods, flavour text, and implicit lines are all included in the match.
- Consider using a PowerShell window set to "Always on Top" to monitor the orb log without alt-tabbing.
- Affix slot detection works by splitting the item name on the base name you provide: any text before the base is the prefix, any text after is the suffix. If both are present the item is full, so an Alteration Orb is used; otherwise an Augmentation Orb fills the open slot. This is why the base name must be accurate (it is matched case-insensitively). If the base cannot be found in the name, the script falls back to Alteration Orbs only.
- Regex is evaluated with Python's `re` module against the full tooltip, so any Python regex syntax works. The `?` help on the regex prompt covers matching multi-word mods and combining them with `|`.
