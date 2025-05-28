# tools/password_checker.py
import re

def main():
    pwd = input("Enter password to check: ")
    strength = 0
    criteria = [
        (r"[a-z]", "Lowercase"),
        (r"[A-Z]", "Uppercase"),
        (r"[0-9]", "Digits"),
        (r"[^a-zA-Z0-9]", "Symbols"),
        (r".{8,}", "Length ≥ 8"),
    ]

    print("\nCriteria Met:")
    for pattern, desc in criteria:
        if re.search(pattern, pwd):
            strength += 1
            print(f"✔ {desc}")
        else:
            print(f"✘ {desc}")

    verdicts = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    print("\nPassword Strength:", verdicts[strength])