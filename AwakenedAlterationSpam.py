import keyboard
import pyautogui
import pyperclip
import time
import re

CLICK_DELAY = 0.1   # seconds between orb uses — rate limit so we don't hammer the server
SHORT_DELAY = 0.0  # seconds to wait after a click before copying, so the item can refresh
ALT_SWAP_DELAY = 0.2  # the aug path spends ~0.2s holding/releasing Alt (pyautogui PAUSE);
                      # match it on the alt path so both orbs feel equally paced

orb_cap = 40
running = False
user_regex = ""
allow_aug = True
item_base = ""

def extract_item_name(text):
    lines = text.splitlines()
    capture = False
    extracted = []

    for line in lines:
        if line.startswith("Rarity:"):
            capture = True
            continue
        if line.strip() == "--------" and capture:
            break
        if capture:
            extracted.append(line)

    return "\n".join(extracted)

def has_both_affixes(item_name, base):
    # A magic item name reads: [prefix ]BASE[ of suffix]. Split on the base
    # name: anything before it is the prefix, anything after it is the suffix.
    idx = item_name.lower().find(base.lower())
    if idx == -1:
        return True  # base not found in the name — fall back to Alt only
    prefix = item_name[:idx].strip()
    suffix = item_name[idx + len(base):].strip()
    return bool(prefix) and bool(suffix)

def ask(prompt, help_text):
    # Re-prompt until the user gives a real answer; '?' shows help and asks again.
    while True:
        answer = input(prompt).strip()
        if answer == "?":
            print(help_text)
            continue
        return answer


def start():
    global running, user_regex, allow_aug, orb_cap, item_base
    if not running:
        running = True
        print("Program started.")

        alts_used = 0
        augs_used = 0
        width = len(str(orb_cap))

        pyautogui.keyDown('shift')

        try:
            # Read the item currently under the cursor
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(SHORT_DELAY)
            raw_text = pyperclip.paste()
            item_name = extract_item_name(raw_text)
            item_name = "".join(line.lstrip() for line in item_name.splitlines())

            # The hovered item might already match before we spend any orb
            if re.search(user_regex, raw_text, re.IGNORECASE):
                print(f"Match found. Alt Orbs used: {alts_used}, Aug Orbs used: {augs_used}. Press = to start again.")
            else:
                while running and (alts_used + augs_used) < orb_cap:
                    # Decide which orb to use, then use it (one orb per loop)
                    if allow_aug and not has_both_affixes(item_name, item_base):
                        pyautogui.keyDown('alt')  # hold Alt to swap to an Augmentation Orb
                        pyautogui.click()
                        pyautogui.keyUp('alt')
                        augs_used += 1
                    else:
                        pyautogui.click()
                        alts_used += 1
                        time.sleep(ALT_SWAP_DELAY)  # mirror the aug path's Alt key timing

                    # Wait for the item to refresh, then copy and read it
                    time.sleep(SHORT_DELAY)
                    pyautogui.hotkey('ctrl', 'c')
                    time.sleep(SHORT_DELAY)
                    raw_text = pyperclip.paste()
                    item_name = extract_item_name(raw_text)
                    item_name = "".join(line.lstrip() for line in item_name.splitlines())
                    print(
                        f"Alt Orbs used: {str(alts_used).rjust(width)} | "
                        f"Aug Orbs used: {str(augs_used).rjust(width)} | "
                        f"{user_regex} | {item_name}"
                    )

                    # Stop the instant we hit the mod, before any further waiting
                    if re.search(user_regex, raw_text, re.IGNORECASE):
                        print(f"Match found. Alt Orbs used: {alts_used}, Aug Orbs used: {augs_used}. Press = to start again.")
                        break

                    # Rate-limit before the next orb
                    time.sleep(CLICK_DELAY)
                else:
                    # Loop ended without a match (hit the cap or was stopped)
                    if (alts_used + augs_used) >= orb_cap:
                        print(f"Reached session orb cap of {orb_cap}. Alt Orbs used: {alts_used}, Aug Orbs used: {augs_used}. Press = to start again.")

        finally:
            pyautogui.keyUp('shift')
            running = False

def stop():
    global running
    if running:
        running = False
        print("Program stopped.")

print("\nType ? at any prompt for help.\n")

# Allow augmentation orb
aug_input = ask(
    "Allow Augmentation Orb? [Y/n]: ",
    "Augmentation Orbs add a second mod to a magic item that has an open affix slot.\n"
    "With this on, the script uses an Aug Orb whenever a slot is open, then an\n"
    "Alteration Orb to reroll. Turn it off to use Alteration Orbs only.",
).lower()
allow_aug = aug_input != 'n'
print(f"Augmentation Orb: {'enabled' if allow_aug else 'disabled'}")

# Item base name — needed to detect open affix slots when aug is enabled.
# Everything before the base is the prefix, everything after is the suffix.
if allow_aug:
    item_base = ask(
        "Enter item base name: ",
        "The base item name with no affixes. Everything before it is the prefix and\n"
        "everything after it is the suffix, which is how the script detects open slots.\n"
        'Example: for "Humming Kinetic Wand of Waning", the base is "Kinetic Wand".',
    )
    print(f"Item base: {item_base}")

# Session orb cap
try:
    user_input = ask(
        "Enter max orbs per session [40]: ",
        "The maximum number of orbs (Alt + Aug combined) the script will use in one\n"
        "session before stopping automatically. A safety limit. Press Enter for 40.",
    )
    orb_cap = int(user_input) if user_input else 40
except ValueError:
    orb_cap = 40
print(f"Orb cap: {orb_cap}")

# Regex
user_regex = ask(
    "Enter regex to match: ",
    "Matched against the full item tooltip with Python's re module, so any Python\n"
    "regex works (| ( ) [ ] . * + ^ $ etc.). Mod text is literal, so spaces work\n"
    "as-is. Three common cases:\n"
    "\n"
    "1. A single mod with spaces - just type it as it appears:\n"
    "     Chaos Damage over Time\n"
    '   matches "+17% to Chaos Damage over Time Multiplier".\n'
    "\n"
    "2. OR (match any one) - separate phrases with | :\n"
    "     Lightning Damage|Cold Damage\n"
    "\n"
    "3. Spaces combine freely with both - each phrase can be multiple words:\n"
    "     Chaos Damage over Time|Lightning Damage\n"
    "   matches either whole phrase.",
)

keyboard.add_hotkey('=', start)
keyboard.add_hotkey('-', stop)

print("Waiting for = to start, - to stop.")
print("Press Ctrl+C to exit manually if needed.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting on Ctrl+C")
