from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import mysql.connector as ms
from employees import get_employee_id

AWARD = "Employee of the month"

def get_employee(mc, empid):
    mc.execute(
        "SELECT empname, salary, bonus FROM employee WHERE empid = %s",
        (empid,)
    )
    return mc.fetchone()

def set_employee_of_month(mydb, mc):
    print("\n--- SET EMPLOYEE OF THE MONTH ---")
    empid = get_employee_id()
    employee = get_employee(mc, empid)

    if employee is None:
        print("\nEmployee not found.\n")
        return

    print(f"\nSelected employee: {employee[0]}")

    if input("Confirm selection? (Y/N): ").strip().upper() != "Y":
        print("\nCancelled.\n")
        return

    try:
        # Preserve the original project's single-award behavior.
        mc.execute(
            "UPDATE employee SET bonus = 'None' WHERE bonus = %s",
            (AWARD,)
        )
        mc.execute(
            "UPDATE employee SET bonus = %s WHERE empid = %s",
            (AWARD, empid)
        )
        mydb.commit()
        print("\nEmployee of the Month updated successfully.\n")

    except ms.Error as error:
        mydb.rollback()
        print(f"\nCould not update award: {error}\n")

def current_employee_of_month(mc):
    print("\n--- CURRENT EMPLOYEE OF THE MONTH ---")

    mc.execute(
        "SELECT empid, empname, department FROM employee "
        "WHERE bonus = %s",
        (AWARD,)
    )
    employees = mc.fetchall()

    if not employees:
        print("\nNo Employee of the Month selected.\n")
        return

    for empid, name, department in employees:
        print(f"\n{name} | ID: {empid} | Department: {department}")

    print()

def remove_employee_of_month(mydb, mc):
    print("\n--- REMOVE EMPLOYEE OF THE MONTH ---")
    empid = get_employee_id()
    employee = get_employee(mc, empid)

    if employee is None:
        print("\nEmployee not found.\n")
        return

    if employee[2] != AWARD:
        print("\nThis employee does not hold the award.\n")
        return

    if input("Remove award? (Y/N): ").strip().upper() != "Y":
        print("\nCancelled.\n")
        return

    try:
        mc.execute(
            "UPDATE employee SET bonus = 'None' WHERE empid = %s",
            (empid,)
        )
        mydb.commit()
        print("\nAward removed successfully.\n")

    except ms.Error as error:
        mydb.rollback()
        print(f"\nCould not remove award: {error}\n")

def salary_bonus(mydb, mc):
    print("\n--- SALARY BONUS ---")
    empid = get_employee_id()
    employee = get_employee(mc, empid)

    if employee is None:
        print("\nEmployee not found.\n")
        return

    name, current_salary, _ = employee
    current_salary = Decimal(str(current_salary))

    print(f"\nEmployee: {name}")
    print(f"Current salary: {current_salary:.2f}")

    while True:
        raw = input("Enter bonus percentage (0-100): ").strip()

        try:
            percentage = Decimal(raw)

            if percentage.is_finite() and 0 <= percentage <= 100:
                break
        except InvalidOperation:
            pass

        print("Enter a valid percentage between 0 and 100.")

    new_salary = (
        current_salary * (1 + percentage / 100)
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if new_salary > Decimal("9999999999.99"):
        print("\nResult exceeds the maximum supported salary.\n")
        return

    print(f"New salary: {new_salary:.2f}")

    if input("Apply salary bonus? (Y/N): ").strip().upper() != "Y":
        print("\nCancelled.\n")
        return

    try:
        mc.execute(
            "UPDATE employee SET salary = %s WHERE empid = %s",
            (new_salary, empid)
        )
        mydb.commit()
        print("\nSalary bonus applied successfully.\n")

    except ms.Error as error:
        mydb.rollback()
        print(f"\nCould not apply bonus: {error}\n")

def bonus(mydb, mc):
    while True:
        print("""
---------- BONUS MANAGEMENT ----------
1. Set Employee of the Month
2. View current Employee of the Month
3. Remove Employee of the Month
4. Apply salary bonus
0. Return to main menu
--------------------------------------
""")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            set_employee_of_month(mydb, mc)
        elif choice == "2":
            current_employee_of_month(mc)
        elif choice == "3":
            remove_employee_of_month(mydb, mc)
        elif choice == "4":
            salary_bonus(mydb, mc)
        elif choice == "0":
            break
        else:
            print("\nInvalid choice. Please try again.")
