# Awakened Alteration Spam

A lightweight Python automation script for efficiently rolling items with alteration orbs in **Path of Exile**. It reads item text from the clipboard, checks if it matches a user-defined regex pattern, and clicks to reroll if it doesn't. The script stops automatically when a match is found or a safety limit is reached.

## Features

- Automatically captures item tooltip with `Ctrl+C`
- Extracts and cleans item name lines
- Matches against a regex entered by the user at startup
- Auto-clicks to roll again if no match is found
- Stops instantly on match or after safety limit
- Hotkey controlled for start/stop
- No re-encoding, overlays, or GUI required

## Requirements

- Python 3.x
- Windows (recommended)

## Installation

1. Install dependencies

```bash
pip install pyautogui pyperclip keyboard
```

2. Clone this repository

```bash
git clone https://github.com/your-username/poe-alteration-assistant.git
cd poe-alteration-assistant
```

## Usage

Video demo can be found at: https://youtu.be/WtSM1Micxlc?si=9efSIHJaNv3YiaWe

1. Run the script

```bash
python AlterationSpam.py
```

2. At startup, you'll be prompted to enter

A safety limit (maximum number of attempts before auto-stop)
Example:

```bash
Enter safety limit [40] (max attempts before auto-stop): 100
```

A regex pattern to match the item name, same as the one you typically put in the filter input
Example:

```bash
Enter regex to match item name: Merciless|Dictator
```

3. In-game

Right-click the Alteration Orb while pressing Shift. Hover over the item you want to roll

Press "=" to start rolling while continue holding Shift

Press "-" to stop the rolling preemptively

The script will:

- Copy item text with Ctrl + C
- Extract and clean the item name
- Match it against your regex
- Left-click to reroll if not matched
- Repeat until a match is found or safety limit is hit

## Notes

- The script simulates keyboard and mouse input; use responsibly.
- Works only with PoE in windowed or borderless mode.
- Consider using a visible overlay (e.g. PowerShell "Always on Top") if running alongside the game.
