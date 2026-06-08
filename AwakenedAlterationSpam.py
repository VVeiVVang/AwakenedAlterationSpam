import keyboard
import pyautogui
import pyperclip
import time
import re

orb_cap = 40
running = False
user_regex = ""
allow_aug = True

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

def has_both_affixes(item_name):
    has_prefix = bool(re.search(r"'s\b", item_name))
    has_suffix = bool(re.search(r"\bof\s", item_name))
    return has_prefix and has_suffix

def start():
    global running, user_regex, allow_aug, orb_cap
    if not running:
        running = True
        print("Program started.")

        orbs_used = 0
        width = len(str(orb_cap))

        pyautogui.keyDown('shift')

        try:
            while orbs_used < orb_cap and running:
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.05)
                raw_text = pyperclip.paste()

                item_name = extract_item_name(raw_text)
                item_name = "".join(line.lstrip() for line in item_name.splitlines())

                if re.search(user_regex, raw_text, re.IGNORECASE):
                    print(f"Match found after {orbs_used} orbs. Press = to start again.")
                    break

                if allow_aug and not has_both_affixes(item_name):
                    pyautogui.keyDown('alt')
                    pyautogui.click()
                    pyautogui.keyUp('alt')
                    orbs_used += 1

                print(f"Orbs used {str(orbs_used + 1).rjust(width)}: {user_regex} | {item_name}")
                pyautogui.click()
                orbs_used += 1
                time.sleep(0.05)

            if orbs_used >= orb_cap:
                print(f"Reached session orb cap of {orb_cap}. Press = to start again.")

        finally:
            pyautogui.keyUp('shift')
            running = False

def stop():
    global running
    if running:
        running = False
        print("Program stopped.")

# Allow augmentation orb
aug_input = input("Allow Augmentation Orb? [Y/n]: ").strip().lower()
allow_aug = aug_input != 'n'
print(f"Augmentation Orb: {'enabled' if allow_aug else 'disabled'}")

# Session orb cap
try:
    user_input = input("Enter max orbs per session [40]: ").strip()
    orb_cap = int(user_input) if user_input else 40
except ValueError:
    orb_cap = 40
print(f"Orb cap: {orb_cap}")

# Regex
user_regex = input("Enter regex to match: ")

keyboard.add_hotkey('=', start)
keyboard.add_hotkey('-', stop)

print("Waiting for = to start, - to stop.")
print("Press Ctrl+C to exit manually if needed.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting on Ctrl+C")
