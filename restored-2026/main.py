from database import connect_db
from employees import addrecord, delrecord, displayall, displayno
from management import displaydept, updates
from bonuses import bonus
from cards import employee_card
from auth import setup_admin, admin_access, logindetails
from employee_auth import set_employee_pin, employee_access


def count_employees(mc):
    mc.execute("SELECT COUNT(*) FROM employee")
    total = mc.fetchone()[0]
    print(f"\nTotal number of employees: {total}\n")


def admin_menu(mydb, mc):
    while True:
        print("\n" + "=" * 50)
        print("RECRUITCARE EMPLOYEE MANAGEMENT".center(50))
        print("ADMINISTRATOR MENU".center(50))
        print("=" * 50)

        print("""
1. Add employee
2. Update employee details
3. Remove employee
4. View all employees
5. View employee by ID
6. View employees by department
7. Count employees
8. Manage bonuses
9. View employee card
10. Change administrator login
11. Set / Reset employee PIN
0. Log out
""")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            addrecord(mydb, mc)
        elif choice == "2":
            updates(mydb, mc)
        elif choice == "3":
            delrecord(mydb, mc)
        elif choice == "4":
            displayall(mc)
        elif choice == "5":
            displayno(mc)
        elif choice == "6":
            displaydept(mc)
        elif choice == "7":
            count_employees(mc)
        elif choice == "8":
            bonus(mydb, mc)
        elif choice == "9":
            employee_card(mc)
        elif choice == "10":
            logindetails()
        elif choice == "11":
            set_employee_pin(mydb, mc)
        elif choice == "0":
            print("\nAdministrator logged out.\n")
            break
        else:
            print("\nInvalid choice. Please try again.")


def employee_menu(mc, empid):
    while True:
        print("\n========== EMPLOYEE MENU ==========")
        print("1. View my employee card")
        print("0. Log out")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            employee_card(mc, empid)
        elif choice == "0":
            print("\nEmployee logged out.\n")
            break
        else:
            print("\nInvalid choice. Please try again.")


def main():
    mydb = None
    mc = None

    try:
        setup_admin()

        mydb = connect_db()

        if mydb is None:
            return

        mc = mydb.cursor()

        while True:
            print("\n" + "=" * 50)
            print("RECRUITCARE EMPLOYEE MANAGEMENT".center(50))
            print("=" * 50)

            print("""
1. Administrator Login
2. Employee Login
0. Exit Program
""")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                if admin_access():
                    admin_menu(mydb, mc)

            elif choice == "2":
                empid = employee_access(mc)

                if empid is not None:
                    employee_menu(mc, empid)

            elif choice == "0":
                print("\nThank you for using Employee Management!")
                break

            else:
                print("\nInvalid choice. Please try again.")

    except (KeyboardInterrupt, EOFError):
        print("\nApplication closed.")

    finally:
        if mc is not None:
            mc.close()

        if mydb is not None and mydb.is_connected():
            mydb.close()


if __name__ == "__main__":
    main()
