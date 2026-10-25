import hashlib
import hmac
import json
import secrets
from getpass import getpass
from pathlib import Path

AUTH_FILE = Path(__file__).resolve().parent / ".admin_auth.json"
ITERATIONS = 600_000


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        ITERATIONS
    ).hex()


def save_credentials(username, password):
    salt = secrets.token_hex(16)

    data = {
        "username": username,
        "salt": salt,
        "password_hash": hash_password(password, salt)
    }

    AUTH_FILE.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )


def load_credentials():
    with AUTH_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_new_credentials():
    while True:
        username = input("Enter administrator username: ").strip()

        if username and len(username) <= 50:
            break

        print("Username must contain 1-50 characters.")

    while True:
        password = getpass("Enter administrator password: ")
        confirm = getpass("Confirm password: ")

        if len(password) < 12:
            print("Password must be at least 12 characters.")
        elif password != confirm:
            print("Passwords do not match.")
        else:
            break

    return username, password


def setup_admin():
    if AUTH_FILE.exists():
        return

    print("\n--- FIRST-TIME ADMINISTRATOR SETUP ---")
    print("Create your administrator login credentials.\n")

    username, password = get_new_credentials()
    save_credentials(username, password)

    print("\nAdministrator account created successfully!\n")


def verify_credentials(username, password):
    data = load_credentials()

    expected = data["password_hash"]
    actual = hash_password(password, data["salt"])

    password_correct = hmac.compare_digest(actual, expected)
    username_correct = hmac.compare_digest(
        username.encode("utf-8"),
        data["username"].encode("utf-8")
    )

    return username_correct and password_correct


def admin_access():
    print("\n========== ADMIN LOGIN ==========")

    for attempt in range(3):
        username = input("Username: ").strip()
        password = getpass("Password: ")

        if verify_credentials(username, password):
            print("\nAccess granted! Welcome, Administrator.\n")
            return True

        remaining = 2 - attempt
        print(f"\nIncorrect credentials. Attempts remaining: {remaining}\n")

    print("Too many failed login attempts.")
    return False


def logindetails():
    print("\n--- CHANGE ADMINISTRATOR LOGIN ---")

    data = load_credentials()

    current_password = getpass("Enter current password: ")

    if not verify_credentials(data["username"], current_password):
        print("\nIncorrect password. Changes cancelled.\n")
        return

    username, password = get_new_credentials()
    save_credentials(username, password)

    print("\nAdministrator credentials updated successfully!\n")
