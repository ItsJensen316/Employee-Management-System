from datetime import datetime
from employees import get_employee_id


def display_card(mc, empid):
    mc.execute(
        """
        SELECT empid, empname, department, salary,
               status, bonus, contact
        FROM employee
        WHERE empid = %s
        """,
        (empid,)
    )

    employee = mc.fetchone()

    if employee is None:
        print("\nNo employee found with that ID.\n")
        return

    empid, name, dept, salary, status, award, contact = employee
    now = datetime.now()

    print("\n" + "-" * 62)
    print("RECRUITCARE EMPLOYMENT AGENCY".center(62))
    print("EMPLOYEE CARD".center(62))
    print(now.strftime("%B %Y").center(62))
    print("-" * 62)

    print(f"Employee ID    : {empid}")
    print(f"Name           : {name}")
    print(f"Department     : {dept}")
    print(f"Salary         : {salary:.2f}")
    print(f"Payment Status : {status}")
    print(f"Contact Number : {contact or 'Not provided'}")

    if award == "Employee of the month":
        print("\n*** EMPLOYEE OF THE MONTH ***")

    print("-" * 62)
    print(f"Generated on: {now:%d-%m-%Y %H:%M:%S}")
    print("THANK YOU".center(62))
    print("-" * 62 + "\n")


def employee_card(mc, empid=None):
    # Employee mode: use the ID already verified at login.
    if empid is not None:
        display_card(mc, empid)
        return

    # Administrator mode: allow viewing different employees.
    while True:
        print("\n--- EMPLOYEE CARD ---")
        selected_id = get_employee_id()
        display_card(mc, selected_id)

        print("1. View another employee card")
        print("0. Return to administrator menu")

        choice = input("Enter your choice: ").strip()

        if choice != "1":
            break
