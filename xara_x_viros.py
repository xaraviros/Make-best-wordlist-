#!/usr/bin/env python3
# xara X viros - Smart Wordlist Generator
# Educational / Defensive Use Only

import sys
import time

SYMBOLS = ["", "@", "_", ".", "!", "#", "$"]

def banner():
    print("\033[1;36m" + "-" * 42)
    print("   xara X viros | wordlist generator")
    print("-" * 42 + "\033[0m")

def variants(word):
    if not word:
        return set()
    return {
        word,
        word.lower(),
        word.upper(),
        word.capitalize()
    }

def ask_list(msg):
    data = input(msg).strip()
    return data.split() if data else []

def ask_yn(msg):
    return input(msg + " (y/n): ").lower().startswith("y")

def main():
    banner()

    try:
        count = int(input("How many usernames? (1–10): "))
        if not 1 <= count <= 10:
            raise ValueError
    except ValueError:
        print("Invalid number")
        sys.exit(1)

    base_words = set()

    for i in range(1, count + 1):
        print(f"\nUser #{i}")
        username = input("  Username: ").strip()
        base_words |= variants(username)

        if ask_yn("  Add phone number"):
            phone = input("    Phone (no code): ").strip()
            code = input("    Code (0750 optional): ").strip()
            if phone:
                base_words.add(phone)
                if code:
                    base_words.add(code + phone)

        if ask_yn("  Add years / dates"):
            base_words |= set(ask_list("    Years (1999 2001): "))
            base_words |= set(ask_list("    Dates (0101 1508): "))

        if ask_yn("  Add city names"):
            for c in ask_list("    Cities: "):
                base_words |= variants(c)

        if ask_yn("  Add family / nicknames"):
            groups = [
                ask_list("    Father: "),
                ask_list("    Mother: "),
                ask_list("    Children: "),
                ask_list("    Nicknames: "),
            ]
            for group in groups:
                for w in group:
                    base_words |= variants(w)

    print("\nGenerating wordlist...")
    time.sleep(1)

    passwords = set()
    base_words = list(base_words)

    for w1 in base_words:
        for w2 in [""] + base_words:
            for s in SYMBOLS:
                pwd = f"{w1}{s}{w2}"
                if len(pwd) >= 6:
                    passwords.add(pwd)

    with open("wordlist.txt", "w", encoding="utf-8") as f:
        for p in sorted(passwords):
            f.write(p + "\n")

    print("\nDone ✔")
    print(f"Unique passwords : {len(passwords)}")
    print("Saved as         : wordlist.txt")

if __name__ == "__main__":
    main()
