import mysql.connector as ms
import sys
import time
from tabulate import tabulate
from datetime import datetime

#################################### FUNCTION - ADMIN #################################################


def admin_access():
    print()
    global aaccess
    aaccess = False
    ch="Y"
    while ch in 'Yy':
        usern = input('Enter username  : ')
        pasw = input('Enter password  : ')
        if usern == user and pasw == passwd:
            aaccess = True
        if aaccess:
            print()
            color.write("Access granted : )\n","STRING")
            print("Opening menus....")
            time.sleep(2)
            print("\n")
            break
        else:
            print()
            color.write("Incorrect username or password","COMMENT")
            print()
            ch=input("Do you wish to try again? (Y/N): ")
            print("\n")
            

#################################### FUNCTION - ADD ###################################################

            
def addrecord():
    chn='Y'
    while chn in 'Yy':
        a=input("Enter employee number: ")
        try:
            int(a)
            chn='N'
        except:
            color.write("Invalid value.. Please try again","KEYWORD")
            time.sleep(1.5)
            print("\n")
    print()
    b=input("Enter Name of the employee: ")
    print()
    while True:
        c=input('''Departments
|    1. Transport     |
|    2. Office        |
|    3. Cleaning      |
|    4. Maintenance   |
|    5. Security      |
|    6. Sales         |
|    7. Accounts      |
Choose your department: ''')
        if c == '1':
            y = 'Transport'
            break
        elif c == '2':
            y = 'Office'
            break
        elif c == '3':
            y = 'Cleaning'
            break
        elif c == '4':
            y = 'Maintenance'
            break
        elif c == '5':
            y = 'Security'
            break
        elif c == '6':
            y = 'Sales'
            break
        elif c == '7':
            y = 'Accounts'
            break
        else:
            color.write("Invalid value.. Please try again","KEYWORD")
            time.sleep(1.5)
            print("\n")
    print()
    c=y
    cho='Y'
    while cho in 'Yy':
        d=input("Enter salary: ")
        try:
            int(d)
            cho='N'
        except:
            color.write("Invalid value.. Please try again","KEYWORD")
            time.sleep(1.5)
            print("\n")
            
    print()
    while True:
        e=input("Enter Payment status (P->Paid N->Not paid): ")
        if e.upper() in 'P':
            e='Paid'
            break
        elif e.upper() in 'N':
            e='Not Paid'
            break
        else:
            e='Not available'
            color.write("Invalid value.. Please try again","KEYWORD")
            time.sleep(1.5)
            print("\n")
    print()
    f="None"
    g=input("Enter contact no: ")
    try:
        mc.execute("insert into employee values ('{}','{}','{}',{},'{}','{}','{}')".format(a,b,c,d,e,f,g))
        mydb.commit()
        print()
        color.write("Record Saved","STRING")
        time.sleep(1.5)
    except:
        print()
        print("Record not Saved")
        mydb.rollback()
    print("\n")
    

#################################### FUNCTION - DELETE ##################################################
    
    
def delrecord():
    try:
        print()
        no=int(input("Enter employee no to be removed: "))
        mc.execute("delete from employee where empid={}".format(no))
        c=mc.rowcount
        if c>0:
            co='Y'
            while co in 'Yy':
                ans=input("Are you sure you want to remove the employee?(Y/N): ")
                if ans=='y' or ans=='Y':
                    co='N'
                    mydb.commit()
                    print()
                    color.write("The employee has been removed successfully\n","STRING")
                    print()
                    time.sleep(1)
                elif ans=='n' or ans=='N':
                    co='N'
                    mydb.rollback()
                    color.write("Exiting back to menu...\n","BUILTIN")
                    print()
                    time.sleep(1)
                else:
                    color.write("Invalid choice... Please try again\n","COMMENT")
                    print()
                    time.sleep(1)
        else:
            print()
            color.write("No records found with matching employee number","KEYWORD")
            time.sleep(1)
            print("\n")
    except:
        print()
        print('An unexpected error occured :(')
        print("Record not Saved")
        mydb.rollback()
        print("\n")


#################################### FUNCTION - DISPLAY ##################################################
        

def displayall():
    try:
        mc.execute("select * from employee")
        print("\n")
        color.write(tabulate(mc,headers=['EmpNo','EmpName','Department','Salary','Status','Bonus','Contact no'],tablefmt='psql'),"SYNC")
        print("\n")
        if mc.rowcount==-1:
            color.write("No records found\n","KEYWORD")
            print("\n")
    except:
        print("Something went wrong")
        
def displayno():
    try:
        x=int(input("Enter the employee number: "))   
        mc.execute("select * from employee where empid={}".format(x))
        print("\n")
        color.write(tabulate(mc,headers=['EmpNo','EmpName','Department','Salary','Status','Bonus','Contact no'],tablefmt='psql'),"SYNC")
        print("\n")
        if mc.rowcount==-1:
            color.write("No records found with matching emploee number\n","KEYWORD")
            print("\n")
    except:
        print("Something went wrong")
        print("\n")
    
def display():
    while True:
        print("\n|   1. Display details of all employees          |")
        print("|   2. Display details of employee with emp no   |")
        print("|   0. Use any other number to exit              |")
        ch=int(input("\nEnter a choice: "))
        if ch==1:
            displayall()
        elif ch==2:
            displayno()
        else:
            color.write("Exiting....\n","BUILTIN")
            time.sleep(2)
            print("-"*48)
            print("\n")
            break

def displaydept():
    try:
        print("Departments:")
        print("      |    1. Transport     | ")
        print("      |    2. Office        | ")
        print("      |    3. Cleaning      | ")
        print("      |    4. Maintenance   | ")
        print("      |    5. Security      | ")
        print("      |    6. Sales         | ")
        print("      |    7. Accounts      | ")
        x=input("Enter a choice: ")
        if x=='1':
            y="Transport"
        elif x=='2':
            y="Office"
        elif x=='3':
            y="Cleaning"
        elif x=='4':
            y="Maintenance"
        elif x=='5':
            y="Security"
        elif x=='6':
            y="Sales"
        elif x=='7':
            y="Accounts"
        else:
            color.write("Invalid choice","COMMENT")
            time.sleep(1.5)
            print("\n")
        mc.execute("select * from employee where department='{}'".format(y))
        print("\n")
        color.write(tabulate(mc,headers=['EmpID','EmpName','Department','Salary','Status','Bonus','Contact no'],tablefmt='psql'),"SYNC")
        print("\n")
        if mc.rowcount==-1:
            color.write("No records found\n","KEYWORD")
            print("\n")

            
    except:
        print("Please try again")
        print("\n")


#################################### FUNCTION - UPDATE ##################################################
        

def updatename():
    print()
    no=int(input("Enter employee no: "))
    mc.execute("select * from employee where empid={}".format(no))
    d=mc.fetchall()
    if mc.rowcount<=0:
        color.write("No records found with matching employee number\n","COMMENT")
        print()
        time.sleep(1.2)
    else:
        for i in d:
            print("Current employee: ",i[1])
        co='Y'
        while co in 'Yy':
            ans=input("Are you sure you want to update?(Y/N): ")
            if ans=='y' or ans=='Y':
                co='N'
                x=input("Enter the new employee: ")
                mc.execute("update employee set empname='{}' where empid={}".format(x,no))
                mydb.commit()
                color.write("Record updated successfully\n","STRING")
                print()
                time.sleep(1)
            elif ans=='n' or ans=='N':
                co='N'
                color.write("Exiting back to menu...\n","BUILTIN")
                print()
                time.sleep(1)
            else:
                color.write("Invalid choice... Please try again\n","COMMENT")
                print()
                time.sleep(1)
            
def updatesal():
    print()
    no=int(input("Enter employee no: "))
    mc.execute("select * from employee where empid={}".format(no))
    d=mc.fetchall()
    if mc.rowcount<=0:
        color.write("No records found with matching employee number\n","COMMENT")
        print()
        time.sleep(1)
    else:
        for i in d:
            print("Employee name: ",i[1])
            print("Current salary: ",i[3])
        co='Y'
        while co in 'Yy':
            ans=input("Are you sure you want to update?(Y/N): ")
            if ans=='y' or ans=='Y':
                co='N'
                sal=int(input("Enter new salary: "))
                mc.execute("update employee set salary={} where empid={}".format(sal,no))
                mydb.commit()
                color.write("Record updated successfully\n","STRING")
                print()
                time.sleep(1)
            elif ans=='n' or ans=='N':
                co='N'
                color.write("Exiting back to menu...\n","BUILTIN")
                print()
                time.sleep(1)
            else:
                color.write("Invalid choice... Please try again\n","COMMENT")
                print()
                time.sleep(1)
    
def updatedep():
    print()
    no=int(input("Enter employee no: "))
    mc.execute("select * from employee where empid={}".format(no))
    d=mc.fetchall()
    if mc.rowcount<=0:
        color.write("No records found with matching employee number\n","COMMENT")
        print()
        time.sleep(1)
    else:
        for i in d:
            print("Employee name: ",i[1])
            print("Current department: ",i[2])
        co='Y'
        while co in 'Yy':
            ans=input("Are you sure you want to update?(Y/N): ")
            if ans=='y' or ans=='Y':
                co='N'
                cho='Y'
                while cho in 'Yy':
                    c=input('''\nDepartments
|    1. Transport     |
|    2. Office        |
|    3. Cleaning      |
|    4. Maintenance   |
|    5. Security      |
|    6. Sales         |
|    7. Accounts      |\n
Choose your department: ''')
                    if c == '1':
                        y = 'Transport'
                        cho='N'
                    elif c == '2':
                        y = 'Office'
                        cho='N'
                    elif c == '3':
                        y = 'Cleaning'
                        cho='N'
                    elif c == '4':
                        y = 'Maintenance'
                        cho='N'
                    elif c == '5':
                        y = 'Security'
                        cho='N'
                    elif c == '6':
                        y = 'Sales'
                        cho='N'
                    elif c == '7':
                        y = 'Accounts'
                        cho='N'
                    else:
                        color.write("Invalid choice... Please try again\n","COMMENT")
                        time.sleep(1.5)
                        print("\n")
                
                mc.execute("update employee set department='{}' where empid={}".format(y,no))
                mydb.commit()
                color.write("Record updated successfully\n","STRING")
                print()
                time.sleep(1)
            elif ans=='n' or ans=='N':
                co='N'
                color.write("Exiting back to menu...\n","BUILTIN")
                print()
                time.sleep(1)
            else:
                color.write("Invalid choice... Please try again\n","COMMENT")
                print()
                time.sleep(1)
        
def updatestat():
    print()
    no=int(input("Enter employee no: "))
    mc.execute("select * from employee where empid={}".format(no))
    d=mc.fetchall()
    if mc.rowcount<=0:
        color.write("No records found with matching employee number\n","COMMENT")
        print()
        time.sleep(1)
    else:
        for i in d:
            print("Employee name: ",i[1])
            print("Current status: ",i[4])
        co='Y'
        while co in 'Yy':
            ans=input("Are you sure you want to update?(Y/N): ")
            if ans=='y' or ans=='Y':
                co='N'
                cc='Y'
                while cc in 'Yy':
                    stat=input("Enter new payment status (P->Paid / N->Not paid) : ")
                    if stat.upper() in 'P':
                        cc='N'
                        stat='Paid'
                    elif stat.upper() in 'N':
                        cc='N'
                        stat='Not Paid'
                    else:
                        print("Invalid choice... Please try again\n")
                        time.sleep(1)
                mc.execute("update employee set status='{}' where empid={}".format(stat,no))
                mydb.commit()
                color.write("Record updated successfully\n","STRING")
                print()
                time.sleep(1)
            elif ans=='n' or ans=='N':
                co='N'
                color.write("Exiting back to menu...\n","BUILTIN")
                print()
                time.sleep(1)
            else:
                color.write("Invalid choice... Please try again\n","COMMENT")
                print()
                time.sleep(1)

def updatecontact():
    print()
    no=int(input("Enter employee no: "))
    mc.execute("select * from employee where empid={}".format(no))
    d=mc.fetchall()
    if mc.rowcount<=0:
        color.write("No records found with matching employee number\n","COMMENT")
        print()
        time.sleep(1.2)
    else:
        for i in d:
            print("Employee name: ",i[1])
            print("Current contact number: ",i[6])
        co='Y'
        while co in 'Yy':
            ans=input("Are you sure you want to update?(Y/N): ")
            if ans=='y' or ans=='Y':
                co='N'
                cont=input("Enter the new contact number: ")
                mc.execute("update employee set contact='{}' where empid={}".format(cont,no))
                mydb.commit()
                color.write("Record updated successfully\n","STRING")
                print()
                time.sleep(1)
            elif ans=='n' or ans=='N':
                co='N'
                color.write("Exiting back to menu...\n","BUILTIN")
                print()
                time.sleep(1)
            else:
                color.write("Invalid choice... Please try again\n","COMMENT")
                print()
                time.sleep(1)

def updates():
    c='Y'
    while c in 'Yy':
        passw=input("Enter security password to continue: ")
        if passw=="1234":
            color.write("\nPassword correct.... opening menus\n","STRING")
            print()
            time.sleep(1.5)
            while True:
                update_op = input('''
                |     1. Update name           |
                |     2. Update salary         |   
                |     3. Update department     |
                |     4. Update status         |
                |     5. Update contact no     |
                |     0. Exit                  |
                Enter a choice : ''')
                if update_op == '1':
                    updatename()
                elif update_op == '2':
                    updatesal()
                elif update_op == '3':
                    updatedep()
                elif update_op == '4':
                    updatestat()
                elif update_op == '5':
                    updatecontact()
                else:
                    color.write("Exiting...\n","BUILTIN")
                    time.sleep(2)
                    print("-"*48)
                    print("\n")
                    break
            break
        else:
            print()
            color.write("Invalid password\n","COMMENT")
            print()
            c=input("Do you want to try again? (Y/N): ")
            if c=='N':
                color.write("Exiting...\n","BUILTIN")
                time.sleep(2)
                print("\n")


#################################### FUNCTION - COUNT ##################################################
                

def count():
    print()
    mc.execute("select * from employee")
    data=mc.fetchall()
    count=0
    if mc.rowcount<=0:
        color.write("No employees found\n","KEYWORD")
        print()
        time.sleep(1.2)
    else:
        for i in data:
            count=count+1
        color.write("Total number of employees in the company: ","SYNC")
        color.write(str(count),"SYNC")
        print("\n")
        time.sleep(1)
        
        
#################################### FUNCTION - BONUS ##################################################
        

def bonus():
    c='Y'
    while c in 'Yy':
        print('''\n|   1. Set employee of the month       |
|   2. Current employee of the month   |
|   3. Remove employee of the month    |
|   4. Salary bonus                    |
|   0. Exit                            |\n''')
        ch=int(input("Enter a choice: "))
        if ch==1:
            print()
            no=int(input("Enter employee no: "))
            mc.execute("select * from employee where empid={}".format(no))
            d=mc.fetchall()
            if mc.rowcount<=0:
                color.write("No records found with matching employee number\n","COMMENT")
                print()
                time.sleep(1)
            else:
                for i in d:
                    print("Employee name: ",i[1])
                x='Employee of the month'
                y='None'
                mc.execute("update employee set bonus='{}'".format(y))
                mc.execute("update employee set bonus='{}' where empid={}".format(x,no))
                color.write("Successfully updated bonus\n","STRING")
                print()
                time.sleep(1)
                mydb.commit()
                
        elif ch==2:
            print()
            x='Employee of the month'
            mc.execute("select * from employee where bonus='{}'".format(x))
            data=mc.fetchall()
            if mc.rowcount<=0:
                color.write("No employee of the month found\n","KEYWORD")
                print()
                time.sleep(1)
            else:
                for i in data:
                    print("Current employee of the month: ",i[1])
                    print("\n")
                    time.sleep(1)
        elif ch==3:
            no=input("Enter employee no: ")
            mc.execute("select * from employee where empid={}".format(no))
            d=mc.fetchall()
            found=True
            if mc.rowcount<=0:
                color.write("No records found with matching employee number\n","COMMENT")
                time.sleep(1)
            else:
                for i in d:
                    if i[5]=="Employee of the month":
                        print("Employee name: ",i[1])
                        found=True
                    else:
                        print("Employee name: ",i[1])
                        print(i[1],"is not the current Employee of the month")
                        time.sleep(1)
                        print("\n")
                        found=False
                if found==True:
                    y='None'
                    mc.execute("update employee set bonus='{}' where empid={}".format(y,no))
                    color.write("Successfully removed employee of the month\n","STRING")
                    print()
                    time.sleep(1)
                    mydb.commit()

        elif ch==4:
            print()
            no=int(input("Enter employee no to give salary bonus: "))
            mc.execute("select * from employee where empid={}".format(no))
            d=mc.fetchall()
            if mc.rowcount<=0:
                print()
                color.write("No records found with matching employee number\n","COMMENT")
                print()
                time.sleep(1)
            else:
                for i in d:
                    print("Employee name: ",i[1])
                    print("Current salary: ",i[3])
                co='Y'
                while co in 'Yy':
                    co='N'
                    s=float(input("Enter new percentage to increase: "))
                    sal=s/100
                    mc.execute("update employee set salary=salary+salary*{} where empid={}".format(sal,no))
                    mydb.commit()
                    color.write("Salary bonus added successfully\n","STRING")
                    print()
                    time.sleep(1)
            
        else:
            color.write("Exiting...\n","BUILTIN")
            time.sleep(2)
            print("-"*48)
            print("\n")
            break

#################################### FUNCTION - LOGIN ##################################################


def logindetails():
    global user
    global passwd
    c='Y'
    while c in 'Yy':
        x=input("Enter current username: ")
        y=input("Enter current password: ")
        if x==user and y==passwd:
            c='N'
            print()
            color.write("Access granted\n","STRING")
            print()
            u=input("Enter new username: ")
            p=input("Enter new password: ")
            user=u
            passwd=p
            color.write("Successfully changed\n","STRING")
            print()
        else:
            color.write("\nIncorrect username or password\n","COMMENT")
            print()
            c=input("Do you wish to try again? (Y/N): ")
            if c=='N':
                color.write("Exiting...\n","BUILTIN")
                time.sleep(2)
                print("\n")
        
            
#################################### FUNCTION - CARD ###############################################

                                
def employee_card():
    print()
    id=input('Enter employee no : ')
    print("\n")
    mc.execute("select * from employee where empid='{}'".format(id))
    data=mc.fetchall()
    now=datetime.now()
    month=now.strftime('%B')
    year=now.strftime('%Y')
    if mc.rowcount<=0:
        color.write("-"*54,"COMMENT")
        print()
        color.write("!!! No records found with matching employee number !!!\n","COMMENT")
        color.write("-"*54,"COMMENT")
        print("\n")
        time.sleep(1)
    else:
        print('-'*70)
        print('RECRUITCARE EMPLOYMENT AGNECY'.center(70))
        print('Shrajah, UAE'.center(70))
        print('email: contact@Recruitcareagency.ae   phone: 06 598 1203'.center(70))
        print()
        print('\t\t    EMPLOYEE CARD -',month,year)
        print()
        print('ID:',data[0][0])
        print()
        print('NAME:',data[0][1])
        print()
        print('DEPARTMENT:',data[0][2])
        print()
        print('SALARY:',data[0][3])
        print()
        print('SALARY STATUS:',data[0][4])
        print()
        print('CONTACT NO:',data[0][6])
        print()
        print('Generated on:',datetime.now())
        print()
        if data[0][5]=="Employee of the month":
            print("!!",data[0][1],"is the current Employee of the month !!")
            print()
        print('THANK YOU'.center(70))
        print('-'*70)
        print("\n")
        color.write("Please press enter to continue\n","KEYWORD")
        input()
        print()
        
    continu=input('''
1. Use another employee id
0. Log out / return to menu
Enter a choice : ''')
    if continu not in '1':
        color.write("Returning....\n","BUILTIN")
        print("\n")
        time.sleep(2)
    else:
        employee_card()
        
        
##################################### MAIN PROGRAM #####################################
        

mydb=ms.connect(host="localhost",user="root",passwd='1234',database='EmpManagement')

if not mydb.is_connected():
    print("Connection failed")
    
mc=mydb.cursor()

try:
    color=sys.stdout.shell
except AttributeError:
    raise RuntimeError("Use Python IDLE to continue")

user="admin"
passwd="admin"

cho='Y'
while cho in 'Yy':
    print(' _________________________________________________ '.center(90))
    print('|                                                 |'.center(90))
    print('|    WELCOME TO RECRUITCARE EMPLOYEMENT AGENCY    |'.center(90))
    print('|_________________________________________________|'.center(90))
    print("\n")
    while True:
        print("|========LOGIN========|")
        print('''|                     |
|     1. Admin        |
|     2. Employee     |
|_____________________|

3. Exit program''')
        print("")
        ch = input('Enter your choice     : ')
        if ch == '1':
            admin_access()
            if aaccess == True:
                i='Y'
                while i in 'Yy':
                    op = input(''' ________________________________________
|                                        |
|     1. Add employee                    |
|     2. Update employee details         |
|     3. Remove employee                 |
|     4. View employee details           |
|     5. Sort employee by department     |
|     6. Count the no of employees       |
|     7. Manage Bonuses                  |
|     8. View employee card              |
|     9. Change login details            |
|     0. Log out                         |
|________________________________________|

Enter a choice : ''')
                    if op == '1':
                        addrecord()
                    elif op == '2':
                        updates()
                    elif op == '3':
                        delrecord()
                    elif op == '4':
                        display()
                    elif op == '5':
                        displaydept()
                    elif op == '6':
                        count()
                    elif op == '7':
                        bonus()
                    elif op == '8':
                        employee_card()
                    elif op == '9':
                        logindetails()
                    else:
                        color.write("Logging out....\n","BUILTIN")
                        time.sleep(2)
                        print("\n")
                        break
                    cn='Y'
                    while cn in 'Yy':
                        continu=input('Do you wish to continue as admin? (Y/N) : ')
                        if continu in 'Yy':
                            cn='N'
                            print("\n")
                        elif continu in 'Nn':
                            cn='N'
                            i='N'
                            color.write("Logging out....\n","BUILTIN")
                            time.sleep(2)
                            print("\n")
                            break
                        elif continu not in 'Yy' and continu not in 'Nn':
                            color.write("Invalid choice\n","COMMENT")
                            color.write("Please try again...\n","KEYWORD")
                            print()
                            time.sleep(1)
                
            elif aaccess == False:
                color.write("Exiting....\n","BUILTIN")
                time.sleep(2)
                print("\n")
            
        elif ch == '2':
            employee_card()

        elif ch == '3':
            color.write("Exiting....\n","BUILTIN")
            time.sleep(2)
            print("-"*48)
            print("\n")
            cho='N'
            break

        else:
            color.write("Invalid choice.... Please try again\n","COMMENT")
            print()
            time.sleep(1.5)
                    
                        





