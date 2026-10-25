import mysql.connector as ms
from decimal import Decimal, InvalidOperation
from tabulate import tabulate

from employees import DEPARTMENTS, HEADERS, get_employee_id


def choose_department():
    print("\nDepartments:")

    for index, department in enumerate(DEPARTMENTS, start=1):
        print(f"{index}. {department}")

    while True:
        choice = input("Choose department (1-7): ").strip()

        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(DEPARTMENTS):
                return DEPARTMENTS[number - 1]

        print("Invalid department. Please try again.")


def displaydept(mc):
    print("\n--- EMPLOYEES BY DEPARTMENT ---")
    department = choose_department()

    mc.execute(
        "SELECT * FROM employee WHERE department = %s ORDER BY empid",
        (department,)
    )

    data = mc.fetchall()

    if not data:
        print(f"\nNo employees found in {department}.\n")
        return

    print(f"\nDepartment: {department}")
    print(tabulate(data, headers=HEADERS, tablefmt="psql"))
    print()


def update_employee(mydb, mc, field, value):
    empid = get_employee_id()

    mc.execute(
        "SELECT empname, " + field +
        " FROM employee WHERE empid = %s",
        (empid,)
    )

    employee = mc.fetchone()

    if employee is None:
        print("\nEmployee not found.\n")
        return

    print(f"\nEmployee: {employee[0]}")
    print(f"Current value: {employee[1]}")

    new_value = value()

    confirm = input("Confirm update? (Y/N): ").strip().upper()

    if confirm != "Y":
        print("\nUpdate cancelled.\n")
        return

    try:
        # Field names come only from the fixed menu below.
        mc.execute(
            f"UPDATE employee SET {field} = %s WHERE empid = %s",
            (new_value, empid)
        )
        mydb.commit()
        print("\nRecord updated successfully!\n")

    except ms.Error as error:
        mydb.rollback()
        print(f"\nUpdate failed: {error}\n")


def input_name():
    while True:
        name = input("Enter new employee name: ").strip()
        if name and len(name) <= 100:
            return name
        print("Enter a valid name (maximum 100 characters).")


def input_salary():
    while True:
        value = input("Enter new salary: ").strip()

        try:
            salary = Decimal(value)

            if (
                salary.is_finite()
                and Decimal("0") <= salary <= Decimal("9999999999.99")
                and salary == salary.quantize(Decimal("0.01"))
            ):
                return salary

        except InvalidOperation:
            pass

        print("Enter a valid salary with up to 2 decimal places.")


def input_status():
    while True:
        status = input(
            "Payment status (P=Paid, N=Not Paid): "
        ).strip().upper()

        if status == "P":
            return "Paid"
        if status == "N":
            return "Not Paid"

        print("Invalid payment status.")


def input_contact():
    while True:
        contact = input("Enter new contact number: ").strip()
        if len(contact) <= 20:
            return contact
        print("Contact number must be at most 20 characters.")


def updates(mydb, mc):
    fields = {
        "1": ("empname", input_name),
        "2": ("salary", input_salary),
        "3": ("department", choose_department),
        "4": ("status", input_status),
        "5": ("contact", input_contact)
    }

    while True:
        print("""
---------- UPDATE EMPLOYEE ----------
1. Update name
2. Update salary
3. Update department
4. Update payment status
5. Update contact number
0. Return to main menu
-------------------------------------
""")

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            break

        if choice not in fields:
            print("\nInvalid choice. Please try again.")
            continue

        field, value_function = fields[choice]
        update_employee(mydb, mc, field, value_function)
