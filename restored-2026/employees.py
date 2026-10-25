import mysql.connector as ms
from decimal import Decimal, InvalidOperation
from tabulate import tabulate

DEPARTMENTS = [
    "Transport",
    "Office",
    "Cleaning",
    "Maintenance",
    "Security",
    "Sales",
    "Accounts"
]

HEADERS = [
    "EmpNo", "EmpName", "Department",
    "Salary", "Status", "Bonus", "Contact No"
]


def get_employee_id():
    while True:
        value = input("Enter employee number: ").strip()

        if value.isdigit() and 0 < int(value) <= 2147483647:
            return int(value)

        print("Invalid employee number. Enter a positive integer.")


def displayall(mc):
    mc.execute("SELECT * FROM employee ORDER BY empid")
    data = mc.fetchall()

    if not data:
        print("\nNo employees found.\n")
        return

    print("\n" + tabulate(data, headers=HEADERS, tablefmt="psql"))
    print()


def displayno(mc):
    empid = get_employee_id()

    mc.execute(
        "SELECT * FROM employee WHERE empid = %s",
        (empid,)
    )
    data = mc.fetchall()

    if not data:
        print("\nNo employee found with that ID.\n")
        return

    print("\n" + tabulate(data, headers=HEADERS, tablefmt="psql"))
    print()


def addrecord(mydb, mc):
    print("\n--- ADD NEW EMPLOYEE ---")

    empid = get_employee_id()

    mc.execute(
        "SELECT empid FROM employee WHERE empid = %s",
        (empid,)
    )

    if mc.fetchone():
        print("\nAn employee with this ID already exists.\n")
        return

    while True:
        name = input("Enter employee name: ").strip()
        if name and len(name) <= 100:
            break
        print("Enter a valid name (maximum 100 characters).")

    print("\nDepartments:")
    for index, department in enumerate(DEPARTMENTS, start=1):
        print(f"{index}. {department}")

    while True:
        choice = input("Choose department (1-7): ").strip()

        if choice in [str(i) for i in range(1, 8)]:
            department = DEPARTMENTS[int(choice) - 1]
            break

        print("Invalid department. Please try again.")

    while True:
        salary_input = input("Enter salary: ").strip()

        try:
            salary = Decimal(salary_input)
            if salary.is_finite() and 0 <= salary <= Decimal("9999999999.99"):
                if salary == salary.quantize(Decimal("0.01")):
                    break
        except InvalidOperation:
            pass

        print("Enter a valid non-negative salary with up to 2 decimal places.")

    while True:
        payment = input("Payment status (P=Paid, N=Not Paid): ").upper().strip()

        if payment in ("P", "N"):
            status = "Paid" if payment == "P" else "Not Paid"
            break

        print("Invalid choice. Enter P or N.")

    while True:
        contact = input("Enter contact number: ").strip()
        if len(contact) <= 20:
            break
        print("Contact number must be at most 20 characters.")

    try:
        mc.execute(
            """
            INSERT INTO employee
            (empid, empname, department, salary, status, bonus, contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (empid, name, department, salary, status, "None", contact)
        )

        mydb.commit()
        print("\nEmployee successfully added!\n")

    except ms.Error as error:
        mydb.rollback()
        print(f"\nCould not save employee: {error}\n")


def delrecord(mydb, mc):
    print("\n--- REMOVE EMPLOYEE ---")

    empid = get_employee_id()

    mc.execute(
        "SELECT empname FROM employee WHERE empid = %s",
        (empid,)
    )

    employee = mc.fetchone()

    if employee is None:
        print("\nEmployee not found.\n")
        return

    print(f"\nEmployee: {employee[0]} (ID: {empid})")

    confirm = input("Are you sure you want to remove this employee? (Y/N): ")

    if confirm.strip().upper() != "Y":
        print("\nDeletion cancelled.\n")
        return

    try:
        mc.execute(
            "DELETE FROM employee WHERE empid = %s",
            (empid,)
        )
        mydb.commit()

        print("\nEmployee successfully removed!\n")

    except ms.Error as error:
        mydb.rollback()
        print(f"\nCould not remove employee: {error}\n")
