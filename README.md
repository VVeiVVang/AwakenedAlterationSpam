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

A lightweight Python script that rolls an item with alteration orbs until a user-defined regex matches anywhere in the item tooltip. When a match is found the script stops and stays ready — press `=` again to start a new session without restarting the script.

## Features

- Reads item tooltip via `Ctrl+C`
- Matches a regex against the full item text
- Holds `Shift` automatically so you stay in alt-spam mode
- Stops on match and waits for the next session — no need to restart
- Stop mid-roll at any time with `-`
- Safety limit prevents runaway rolling

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

2. At startup you will be prompted for two things:

A safety limit — the maximum number of roll attempts before the script auto-stops:

```
Enter safety limit [40] (max attempts before auto-stop): 100
```

A regex pattern to match against the item tooltip (same syntax as your loot filter):

```
Enter regex to match: Merciless|Dictator
```

3. In-game setup

- Right-click the Alteration Orb to enter alt-spam mode (the cursor changes)
- Hover over the item you want to roll
- Press `=` — the script takes over from here

The script will:

- Hold `Shift` automatically (you do not need to hold it yourself)
- Copy the item tooltip with `Ctrl+C`
- Match the full tooltip text against your regex
- Left-click to reroll if no match is found
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
- Consider using a PowerShell window set to "Always on Top" to monitor the attempt log without alt-tabbing.
