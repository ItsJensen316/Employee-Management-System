import hashlib
import hmac
import secrets
from getpass import getpass

import mysql.connector as ms

from employees import get_employee_id


ITERATIONS = 600_000


def hash_pin(pin, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        bytes.fromhex(salt),
        ITERATIONS
    ).hex()


def set_employee_pin(mydb, mc):
    print("\n--- SET / RESET EMPLOYEE PIN ---")

    empid = get_employee_id()

    mc.execute(
        "SELECT empname FROM employee WHERE empid = %s",
        (empid,)
    )

    employee = mc.fetchone()

    if employee is None:
        print("\nEmployee not found.\n")
        return

    print(f"\nEmployee: {employee[0]}")

    while True:
        pin = getpass("Enter new 6-digit PIN: ")
        confirm = getpass("Confirm PIN: ")

        if len(pin) != 6 or not pin.isdigit() or not pin.isascii():
            print("PIN must contain exactly 6 ASCII digits.")
        elif pin != confirm:
            print("PINs do not match.")
        else:
            break

    if input("Save this employee PIN? (Y/N): ").strip().upper() != "Y":
        print("\nCancelled.\n")
        return

    salt = secrets.token_hex(16)
    pin_hash = hash_pin(pin, salt)

    try:
        mc.execute(
            """
            INSERT INTO employee_login (empid, pin_salt, pin_hash)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                pin_salt = %s,
                pin_hash = %s
            """,
            (empid, salt, pin_hash, salt, pin_hash)
        )

        mydb.commit()
        print("\nEmployee PIN saved successfully.\n")

    except ms.Error as error:
        mydb.rollback()
        print(f"\nCould not save employee PIN: {error}\n")


def verify_employee(mc, empid, pin):
    mc.execute(
        """
        SELECT pin_salt, pin_hash
        FROM employee_login
        WHERE empid = %s
        """,
        (empid,)
    )

    record = mc.fetchone()

    if record is None:
        return False

    salt, expected_hash = record
    actual_hash = hash_pin(pin, salt)

    return hmac.compare_digest(actual_hash, expected_hash)


def employee_access(mc):
    print("\n========== EMPLOYEE LOGIN ==========")

    for attempt in range(3):
        empid_text = input("Employee ID: ").strip()
        pin = getpass("Employee PIN: ")

        if empid_text.isdigit() and 0 < int(empid_text) <= 2147483647:
            empid = int(empid_text)

            if verify_employee(mc, empid, pin):
                print("\nEmployee login successful!\n")
                return empid

        remaining = 2 - attempt
        print(f"\nInvalid login. Attempts remaining: {remaining}\n")

    print("Too many failed attempts.")
    return None
