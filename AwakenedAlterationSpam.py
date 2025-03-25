import keyboard
import pyautogui
import pyperclip
import time
import re
import sys

safety_limit = 40  # Max number of roll attempts before exiting

running = False
user_regex = ""

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

def start():
    global running, user_regex
    if not running:
        running = True
        print("Program started.")

        attempts = 0
        attempt_width = len(str(safety_limit))  # Align width based on safety_limit

        while attempts < safety_limit:
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.05)
            raw_text = pyperclip.paste()

            # Extract and clean item name
            item_name = extract_item_name(raw_text)
            item_name = "".join(line.lstrip() for line in item_name.splitlines())

            # Check for regex match
            if re.search(user_regex, item_name):
                print("Match found. Exiting.")
                keyboard.unhook_all_hotkeys()
                sys.exit(0)

            # Print formatted attempt log
            print(f"Attempt {str(attempts + 1).rjust(attempt_width)}: Regex: {user_regex} Item Name: {item_name}")
            pyautogui.click()
            attempts += 1
            time.sleep(0.1)

        print(f"Reached safety limit of {safety_limit} attempts. Exiting.")
        running = False

def stop():
    global running
    if running:
        running = False
        print("Program stopped.")

# Ask user for safety limit (default to 40 if invalid)
try:
    user_input = input("Enter safety limit [40] (max attempts before auto-stop): ").strip()
    SAFETY_LIMIT = int(user_input) if user_input else 40
except ValueError:
    SAFETY_LIMIT = 40
print(f"Using safety limit: {SAFETY_LIMIT}")

# Ask user for regex
user_regex = input("Enter regex to match item name: ")

keyboard.add_hotkey('shift+=', start)
keyboard.add_hotkey('shift+-', stop)

print("Waiting for Shift+= to start, Shift+- to stop.")
print("Press Ctrl+C to exit manually if needed.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting on Ctrl+C")
