"""
Author: Pavith Bambaravanage
URL: https://github.com/Pavith19
"""

import mysql.connector as M
import random
import re
from prettytable import PrettyTable

# Database connection
mydb = M.connect(host="localhost", user="root", password="", database="banking_system")
mycur = mydb.cursor()
a = 0

def validate_name(name):
    """Validate name contains only letters and spaces"""
    return name.replace(' ', '').isalpha() and len(name) >= 2

def validate_email(email):
    """Validate email format"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_age(age):
    """Validate age is 18 or above"""
    try:
        age = int(age)
        return age >= 18
    except ValueError:
        return False

def validate_phone(phone):
    """Validate phone number is 10 digits"""
    try:
        phone_str = str(phone)
        return len(phone_str) == 10 and phone_str.isdigit()
    except ValueError:
        return False

def Display_Table1():
    global a
    mycur.execute("SELECT * FROM PERSONALDETAILS")
    k = mycur.fetchall()
    mytable = PrettyTable(["ACC NO.", "NAME", "AGE", "RESIDENTIAL ADDRESS", "E-MAIL ADDRESS", "PHONE NUMBER"])
    for i in k:
        if i[0] == a:
            mytable.add_row([i[0], i[1], i[2], i[3], i[4], i[5]])
            return mytable
    return "Account not found"

def Display_Table2():
    global a
    mycur.execute("SELECT * FROM CUSTOMERACCOUNT")
    k = mycur.fetchall()
    mytable = PrettyTable(["ACCOUNT NUMBER", "NAME", "CURRENT ACCOUNT", "SAVINGS ACCOUNT", "FIXED DEPOSITS"])
    for i in k:
        if i[0] == a:
            mytable.add_row([i[0], i[1], i[2], i[3], i[4]])
            return mytable
    return "Account not found"

def Display_Table3():
    global a
    mycur.execute("SELECT * FROM LOANDETAILS")
    r = mycur.fetchall()
    mytable = PrettyTable(["ACCOUNT NUMBER", "NAME", "PERSONAL LOAN", "HOME LOAN", "AUTO LOAN", "MORTGAGE"])
    for i in r:
        if i[0] == a:
            mytable.add_row([i[0], i[1], i[2], i[3], i[4], i[5]])
            return mytable
    return "Account not found"

def accnocheck():
    global a
    t = (a,)
    mycur.execute("SELECT * FROM ACCNOS")
    k = mycur.fetchall()
    c = 0
    while t not in k:
        print("INVALID INPUT")
        c += 1
        if c < 2:
            try:
                a = int(input("Enter a valid account number: "))
                t = (a,)
            except ValueError:
                print("Please enter a valid numeric account number.")
                continue
        else:
            print("Press 1 to try again or 2 to return to the home screen")
            try:
                ch = int(input("Enter a choice: "))
                if ch == 1:
                    a = int(input("Enter a valid account number: "))
                    t = (a,)
                else:
                    choosemode()
                    return
            except ValueError:
                print("Invalid input. Please enter a number.")

def Create():
    global a
    while True:
        print("\n<Enter the following details>")
        
        # Name validation
        while True:
            n = input("\n> Name: ").strip()
            if validate_name(n):
                break
            print("Invalid name. Use only letters and spaces, minimum 2 characters.")
        
        # Age validation
        while True:
            age = input("\n> Age: ")
            if validate_age(age):
                age = int(age)
                break
            print("Invalid age. Must be 18 or older.")
        
        # Residential address (basic non-empty check)
        while True:
            r = input("\n> Residential Address: ").strip()
            if r:
                break
            print("Address cannot be empty.")
        
        # Email validation
        while True:
            e = input("\n> E-mail Address: ").strip()
            if validate_email(e):
                break
            print("Invalid email format.")
        
        # Phone number validation
        while True:
            try:
                p = input("\n> Phone Number: ")
                if validate_phone(p):
                    p = int(p)
                    break
                print("Invalid phone number. Must be 10 digits.")
            except ValueError:
                print("Please enter a valid phone number.")
        
        # Generate unique account number
        a = random.randint(50, 1000)
        mycur.execute("SELECT * FROM ACCNOS")
        k = mycur.fetchall()
        while True:
            t = (a,)
            if not any(i[0] == a for i in k):
                mycur.execute("INSERT INTO ACCNOS VALUES(%s)", t)
                break
            else:
                a = random.randint(50, 1000)
        
        # Insert personal details
        d = "INSERT INTO PERSONALDETAILS VALUES(%s,%s,%s,%s,%s,%s)"
        mycur.execute(d, (a, n, age, r, e, p))
        print("Your account has been created successfully!")
        print("Your account details are as follows:")
        print(Display_Table1())
        
        # Initial deposit
        while True:
            try:
                am = int(input("\n> Enter the amount you would like to deposit: "))
                if am < 10000:
                    print("The minimum deposit required is Rs.10000")
                    continue
                break
            except ValueError:
                print("Please enter a valid numeric amount.")
        
        # Insert account details
        v = "INSERT INTO CUSTOMERACCOUNT (ACCNO, NAME, CURRENTACCOUNT) VALUES(%s, %s, %s)"
        mycur.execute(v, (a, n, am))
        print("Deposition successful!!!")
        
        # Initialize loan details
        w = "INSERT INTO LOANDETAILS (ACCNO, NAME) VALUES(%s, %s)"
        mycur.execute(w, (a, n))
        mydb.commit()
        break

def Modify():
    print("""
    ================================
           *** MODIFY MENU ***
    ================================
    WHICH OF THE FOLLOWING WOULD YOU LIKE TO MODIFY?
    1. Modify Name
    2. Modify Age
    3. Modify Residential Address
    4. Modify E-mail Address
    5. Modify Phone Number
    6. Return to Main Menu
    ================================
    """)
    
    choice = int(input(">> Enter a choice from the MODIFY Menu: "))
    global a
    while True:
        if choice == 1:
            a = int(input("\n> Enter account number:"))
            accnocheck()
            while True:
                n = input("\n> New Name:").strip()
                if validate_name(n):
                    mycur.execute("UPDATE PERSONALDETAILS SET NAME=%s WHERE ACCNO=%s", (n, a))
                    break
                print("Invalid name. Use only letters and spaces, minimum 2 characters.")
            print("Updated account details are as follows:")
            print(Display_Table1())
            break
        elif choice == 2:
            a = int(input("\n> Enter account number:"))
            accnocheck()
            while True:
                ag = input("\n> New Age:")
                if validate_age(ag):
                    ag = int(ag)
                    mycur.execute("UPDATE PERSONALDETAILS SET AGE=%s WHERE ACCNO=%s", (ag, a))
                    break
                print("Invalid age. Must be 18 or older.")
            print("Updated account details are as follows:")
            print(Display_Table1())
            break
        elif choice == 3:
            a = int(input("\n> Enter account number:"))
            accnocheck()
            while True:
                r = input("\n> New Residential Address:").strip()
                if r:
                    mycur.execute("UPDATE PERSONALDETAILS SET RESIDENTIALADDRESS=%s WHERE ACCNO=%s", (r, a))
                    break
                print("Address cannot be empty.")
            print("Updated account details are as follows:")
            print(Display_Table1())
            break
        elif choice == 4:
            a = int(input("\n> Enter account number:"))
            accnocheck()
            while True:
                e = input("\n> New E-mail Address:").strip()
                if validate_email(e):
                    mycur.execute("UPDATE PERSONALDETAILS SET EADD=%s WHERE ACCNO=%s", (e, a))
                    break
                print("Invalid email format.")
            print("Updated account details are as follows:")
            print(Display_Table1())
            break
        elif choice == 5:
            a = int(input("\n> Enter account number:"))
            accnocheck()
            while True:
                try:
                    p = input("\n> New Phone Number:")
                    if validate_phone(p):
                        p = int(p)
                        mycur.execute("UPDATE PERSONALDETAILS SET PHNO=%s WHERE ACCNO=%s", (p, a))
                        break
                    print("Invalid phone number. Must be 10 digits.")
                except ValueError:
                    print("Please enter a valid phone number.")
            print("Updated account details are as follows:")
            print(Display_Table1())
            break
        elif choice == 6:
            print("Exiting")
            break
        else:
            print("INVALID INPUT: ENTER A CHOICE ONLY BETWEEN 1 TO 6")
            choice = int(input("Enter a choice from the MODIFY Menu:"))
    mydb.commit()

def Withdraw():
    global a
    a = int(input("\n> Enter account number:"))
    accnocheck()
    while True:
        try:
            s = int(input("\n> Enter amount you would like to withdraw:"))
            if s <= 0:
                print("Please enter a positive amount.")
                continue
            break
        except ValueError:
            print("Please enter a valid numeric amount.")
    
    mycur.execute("SELECT CURRENTACCOUNT FROM CUSTOMERACCOUNT WHERE ACCNO=%s", (a,))
    k = mycur.fetchone()
    if k:
        d = k[0]
        amt = d - s
        if s > d:
            print("\nCurrent balance is", d, "\nThe value entered is more than current balance!")
            print("\n> Would you like to try again? Press 1 to try again or 2 to return to the main menu;")
            while True:
                try:
                    ch = int(input("Enter your choice:"))
                    if ch == 1:
                        Withdraw()
                        break
                    elif ch == 2:
                        choosemode()
                        break
                    else:
                        print("Invalid choice:")
                except ValueError:
                    print("Please enter a valid number.")
        elif amt < 10000:
            print("\nWithdrawal leads to insufficient minimum balance")
            print("\nWould you like to try again? Press 1 to try again or 2 to return to the main menu;")
            while True:
                try:
                    ch = int(input("Enter your choice:"))
                    if ch == 1:
                        Withdraw()
                        break
                    elif ch == 2:
                        choosemode()
                        break
                    else:
                        print("Invalid choice:")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            m = "UPDATE CUSTOMERACCOUNT SET CURRENTACCOUNT=%s WHERE ACCNO=%s"
            mycur.execute(m, (amt, a))
            mydb.commit()
            print(Display_Table2())
            print("Rs.", s, "has been withdrawn from your account with account number:", a, "\nAmount remaining in your account is Rs.", amt)
    else:
        print("Account not found")

def Deposit():
    global a
    a = int(input("Enter your account number:"))
    accnocheck()
    print(''' ***DEPOSIT MENU***
    DEPOSIT AMOUNT IN:
    1. Current Account
    2. Savings Account
    3. Fixed Deposit
    4. Exit''')
    while True:
        try:
            ch = int(input("Enter a choice from the DEPOSIT Menu: "))
            if ch == 1:
                Currentacc()
                break
            elif ch == 2:
                Savingsacc()
                break
            elif ch == 3:
                Fixeddeposit()
                break
            elif ch == 4:
                print("RETURNING TO THE ADMIN MENU")
                choosemode()
                break
            else:
                print("Invalid Input")
        except ValueError:
            print("Please enter a valid numeric choice.")

def Currentacc():
    global a
    a = int(input("Enter your account number:"))
    accnocheck()
    while True:
        try:
            am = int(input("Enter amount to deposit: "))
            if am <= 0:
                print("Please enter a positive amount.")
                continue
            break
        except ValueError:
            print("Please enter a valid numeric amount.")
    
    mycur.execute("SELECT CURRENTACCOUNT FROM CUSTOMERACCOUNT WHERE ACCNO=%s", (a,))
    d = mycur.fetchone()[0]
    amt = d + am
    m = "UPDATE CUSTOMERACCOUNT SET CURRENTACCOUNT=%s WHERE ACCNO=%s"
    mycur.execute(m, (amt, a))
    mydb.commit()
    print("Amount successfully deposited")
    print(Display_Table2())

def Savingsacc():
    global a
    a = int(input("Enter your account number:"))
    accnocheck()
    while True:
        try:
            am = int(input("Enter amount to deposit: "))
            if am <= 0:
                print("Please enter a positive amount.")
                continue
            break
        except ValueError:
            print("Please enter a valid numeric amount.")
    
    mycur.execute("SELECT SAVINGSACCOUNT FROM CUSTOMERACCOUNT WHERE ACCNO=%s", (a,))
    d = mycur.fetchone()[0]
    amt = d + am
    m = "UPDATE CUSTOMERACCOUNT SET SAVINGSACCOUNT=%s WHERE ACCNO=%s"
    mycur.execute(m, (amt, a))
    mydb.commit()
    print("Amount successfully deposited")
    print(Display_Table2())

def Fixeddeposit():
    global a
    a = int(input("Enter your account number:"))
    accnocheck()
    while True:
        try:
            am = int(input("Enter amount to deposit: "))
            if am <= 0:
                print("Please enter a positive amount.")
                continue
            break
        except ValueError:
            print("Please enter a valid numeric amount.")
    
    mycur.execute("SELECT FIXEDDEPOSITS FROM CUSTOMERACCOUNT WHERE ACCNO=%s", (a,))
    d = mycur.fetchone()[0]
    amt = d + am
    m = "UPDATE CUSTOMERACCOUNT SET FIXEDDEPOSITS=%s WHERE ACCNO=%s"
    mycur.execute(m, (amt, a))
    mydb.commit()
    print("Amount successfully deposited")
    print(Display_Table2())

def Viewall():
    mycur.execute("SELECT * FROM PERSONALDETAILS")
    personal_details = mycur.fetchall()
    mytable1 = PrettyTable(["ACC NO.", "NAME", "AGE", "RESIDENTIAL ADDRESS", "E-MAIL ADDRESS", "PHONE NUMBER"])
    for row in personal_details:
        mytable1.add_row(row)
    print(mytable1)
    
    mycur.execute("SELECT * FROM CUSTOMERACCOUNT")
    customer_accounts = mycur.fetchall()
    mytable2 = PrettyTable(["ACCOUNT NUMBER", "NAME", "CURRENT ACCOUNT", "SAVINGS ACCOUNT", "FIXED DEPOSITS"])
    for row in customer_accounts:
        mytable2.add_row(row)
    print(mytable2)
    
    mycur.execute("SELECT * FROM LOANDETAILS")
    loan_details = mycur.fetchall()
    mytable3 = PrettyTable(["ACCOUNT NUMBER", "NAME", "PERSONAL LOAN", "HOME LOAN", "AUTO LOAN", "MORTGAGE"])
    for row in loan_details:
        mytable3.add_row(row)
    print(mytable3)

def choosemode():
    while True:
        print("""
        ================================
             *** BANKING MENU ***
        ================================
        1. Create Account
        2. Modify Account
        3. Withdraw
        4. Deposit
        5. View All
        6. Exit
        ================================
        """)
        try:
            choice = int(input(">> Enter a choice from the MENU: "))
            if choice == 1:
                Create()
            elif choice == 2:
                Modify()
            elif choice == 3:
                Withdraw()
            elif choice == 4:
                Deposit()
            elif choice == 5:
                Viewall()
            elif choice == 6:
                print("Exiting the Banking System")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Please enter a valid numeric choice.")
        
        # Ask if user wants to continue or exit after each operation
        while True:
            try:
                cont = input("Do you want to perform another operation? (yes/no): ").lower()
                if cont in ['yes', 'y']:
                    break
                elif cont in ['no', 'n']:
                    print("Exiting the Banking System")
                    return
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            except Exception:
                print("Invalid input. Please try again.")

def main():
    try:
        # Additional error handling for database connection
        print("Connecting to Banking System...")
        choosemode()
    except M.Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure database connection is closed
        if mydb.is_connected():
            mycur.close()
            mydb.close()
            print("\nDatabase connection closed.")

# Main execution
if __name__ == "__main__":
    main()
