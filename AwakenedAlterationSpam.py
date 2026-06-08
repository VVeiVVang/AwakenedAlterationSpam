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

        pyautogui.keyDown('shift')  # Hold shift at the start

        try:
            while attempts < safety_limit and running:
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.05)
                raw_text = pyperclip.paste()

                item_name = extract_item_name(raw_text)
                item_name = "".join(line.lstrip() for line in item_name.splitlines())

                if re.search(user_regex, raw_text, re.IGNORECASE):
                    print("Match found. Exiting.")
                    print("Press = to start again.")
                    break  # exits loop to release shift

                print(f"Attempt {str(attempts + 1).rjust(attempt_width)}: Regex: {user_regex} Item Name: {item_name}")
                pyautogui.click()
                attempts += 1
                time.sleep(0.05)

            if attempts >= safety_limit:
                print(f"Reached safety limit of {safety_limit} attempts. Exiting.")

        finally:
            pyautogui.keyUp('shift')  # Always release shift, even if an error occurs
            running = False

def stop():
    global running
    if running:
        running = False
        print("Program stopped.")

# Ask user for safety limit (default to 40 if invalid)
try:
    user_input = input("Enter safety limit [40] (max attempts before auto-stop): ").strip()
    safety_limit = int(user_input) if user_input else 40
except ValueError:
    safety_limit = 40
print(f"Using safety limit: {safety_limit}")

# Ask user for regex
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
