from objs import actors as a
from objs import entity as e
import mysql.connector as db
from datetime import datetime
import time

DATEFORMAT = '%Y-%m-%d'
con = db.connect(host='localhost', user='root', passwd='root', port=3306, database='rbcdb')
c = con.cursor()


# always use c.fetchall() to buffer the cursor to avoid internal error: unreadable result from sql


# always use c.fetchall() to buffer the cursor to avoid internal error: unreadable result from sql


def openCustomerAccount():
    print("OPENING NEW ACCOUNT")
    print()
    fname = input("FIRST NAME: ").upper()
    lname = input("LAST NAME: ").upper()
    sex = input('GENDER(M/F): ').upper()
    dob = input("DATE OF BIRTH (YYYY-MM-DD): ")
    relationship = input("RELATIONSHIP STATUS (Single/Married/Divorced/Other): ").upper()
    phone = input("PHONE: ")
    stateOfOrigin = input("STATE/REGION: ").upper()
    countryofOrigin = input("COUNTRY OF ORIGIN: ").upper()
    streetAddress = input("HOUSE/STREET ADDRESS: ").upper()
    town = input("TOWN/CITY: ").upper()
    country = input("COUNTRY: ").upper()
    postalcode = input("POSTAL CODE (XXX XXX): ").upper()

    # initializing the customer class to write to database

    C = a.Customer(fname, lname, sex, dob, relationship, phone, stateOfOrigin, countryofOrigin, streetAddress, town,
                   country, postalcode, 0)

    parameters = (
    C.FirstName, C.LastName, C.Gender, C.DateOfBirth, C.Relationship, C.PhoneNumber, C.StateOfOrigin, C.CountryOfOrigin,
    C.StreetAddress, C.City, C.Country, C.PostalCode)

    query = 'insert into `Customer` values (default,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s);'

    c.execute(query, parameters)
    con.commit()

    # Note that by default upon creation of a customer account only a chequing account is opened
    acct_type = e.AccountType(1).name
    getaccountNumber = '''Select `AccountNumber` from `Customer_Accounts_Account` where `LastName`=%s and `PhoneNumber`=%s and `AccountType_ID`=1'''
    c.execute(getaccountNumber, (C.LastName, C.PhoneNumber))
    accountNumber = c.fetchone()[0]
    time.sleep(2)
    print()
    print('ACCOUNT CREATED SUCCESSFULLY')
    print()
    time.sleep(1)
    print('FETCHING NEW ACCOUNT DETAILS...')
    print()
    time.sleep(2)

    print('FULL NAME: ', C.FirstName, C.LastName)
    print('ACCOUNT TYPE: ', acct_type)
    print('ACCOUNT NUMBER: ', accountNumber)
    print()
    print('PLEASE PROVIDE THE ACCOUNT NUMBER GENERATED HERE WHEN LOGGING INTO Y0U ONLINE BANK ACCOUNT')
    print()


def checkCustomerAccount(lname, phone):
    print("ACCOUNT DETAILS")
    print('-' * 40)
    print()

    getaccountsID = "select `Accounts_id` from `Customer_Accounts_Account` where `LastName`=%s and `PhoneNumber`=%s"

    c.execute(getaccountsID, (lname, phone))
    accountsID = c.fetchone()

    c.fetchall()
    accounts = 'select * from `Account` where `Accounts_ID`=%s order by `AccountType_ID` asc;'
    c.execute(accounts, (accountsID[0],))
    accountDetails = c.fetchall()

    for acct in accountDetails:
        acct = e.Account(acct[0], acct[1], acct[2], e.AccountType(acct[3]).name, acct[4])
        if acct.active == 1:
            print(f"{'ACCOUNT NUMBER: ':<15} {acct.accountNumber:>10}")
            print(f"{'ACCOUNT : ':<15} {acct.accountType:>11}")
            print(f"{'ACCOUNT BALANCE: ':<15} {acct.balance:>9}")
            print()
            time.sleep(2)


def closeCustomerAccount(customerID):
    print("CLOSING CUSTOMER ACCOUNT, PLEASE PROVIDE DATE OF BIRTH TO CONFIRM")
    print()
    while True:
        dob = input("Date of Birth (YYYY-MM-DD): ")

        if customerID == None:
            print('CUSTOMER ACCOUNT NOT FOUND')
            print()
            break
        else:
            # gets customer date of birth from database to verify entry
            getdob = 'select `DOB` from `Customer` where `ID` = %s'
            c.execute(getdob, (customerID[0],))
            customer_dob = c.fetchone()

            if customer_dob == None:
                print('DATE OF BIRTH NOT CORRECT')
                print()
            elif datetime.strftime(customer_dob[0], DATEFORMAT) == dob:
                closeaccount = 'delete from `Customer` where `ID` = %s'
                c.execute(closeaccount, (customerID[0],))
                con.commit()
                time.sleep(2)
                print('CUSTOMER ACCOUNT CLOSED SUCCESSFULLY')
                print()
                break
            else:
                print('DATE OF BIRTH NOT CORRECT ')
                print()


def updateCustomerName(customerID):
    if customerID == None:
        print('CUSTOMER ACCOUNT NOT FOUND')
        print()

    else:
        nFName = input("New First Name: ").upper()
        nLName = input("New Last Name: ").upper()
        print()
        updateName = 'update `Customer` set `FirstName` = %s , `LastName` = %s where `ID`=%s;'
        c.execute(updateName, (nFName, nLName, customerID[0]))
        con.commit()
        time.sleep(2)
        print('CUSTOMER NAME UPDATED SUCCESSFULLY')
        print()


def updateCustomerAddress(customerID):
    if customerID == None:
        print('CUSTOMER ACCOUNT NOT FOUND')
        print()

    else:
        nHouseAddress = input("NEW HOUSE ADDRESS: ").upper()
        nCity = input("NEW CITY: ").upper()
        nCountry = input("NEW COUNTRY: ").upper()
        nPostalCode = input("NEW POSTAL CODE: ").upper()
        print()
        updateAddress = 'update `Customer` set `HouseAddress`= %s , `Town_City` = %s , `CountryOfResidence` = %s , `PostalCode` = %s where `ID`=%s;'
        c.execute(updateAddress, (nHouseAddress, nCity, nCountry, nPostalCode, customerID[0]))
        con.commit()
        time.sleep(2)
        print('CUSTOMER ADDRESS UPDATED SUCCESSFULLY')
        print()


def updateCustomerPhone(customerID):
    if customerID == None:
        print('CUSTOMER ACCOUNT NOT FOUND')
        print()

    else:
        nPhone = input('NEW PHONE: ')
        print()
        updateAddress = 'update `Customer` set `PhoneNumber` = %s where `ID`=%s;'
        c.execute(updateAddress, (nPhone, customerID[0]))
        con.commit()
        time.sleep(2)
        print('CUSTOMER PHONE UPDATED SUCCESSFULLY')
        print()


def updateAccountInformation(lname, phone):
    c.fetchall()
    # gets the customerID from database
    getcustomerID = 'select `ID` from `Customer_Accounts_Account` where `LastName`=%s and `PhoneNumber`=%s'
    c.execute(getcustomerID, (lname, phone))
    customerID = c.fetchone()
    print()
    print('Menu Options: ')
    print('1. Update Customer Name')
    print('2. Update Customer Address')
    print('3. Update Customer Phone Number')
    print('4. Back')
    print()
    while True:
        try:
            print()
            cmd = int(input("Update Account Option: "))
            print()
            if cmd == 1:
                updateCustomerName(customerID)
            elif cmd == 2:
                updateCustomerAddress(customerID)
            elif cmd == 3:
                updateCustomerPhone(customerID)
            elif cmd == 4:
                break
            else:
                print()
                print('INVALID OPTION')
                print()
        except ValueError:
            print('INVALID INPUT')


def depositIntoAccount(accountsID):
    print('DEPOSIT TRANSACTION')
    try:
        print()
        depositAccountNumber = int(input("DEPOSIT ACCOUNT NUMBER: "))
        print()

        print('FETCHING ACCOUNT NAME...')
        print()
        time.sleep(3)

        depositAccountNumber = int(depositAccountNumber)
        getcustomerID = 'select `ID` from `Customer_Accounts_Account` where `AccountNumber`=%s'
        c.execute(getcustomerID, (depositAccountNumber,))
        customerID = c.fetchone()

        if customerID == None:
            print('CUSTOMER ACCOUNT NOT FOUND')
            print()
        else:

            c.fetchall()
            # verifies account owner by returning the customer name
            getFullName = 'select `FirstName`, `LastName` from `Customer` where `ID`=%s'
            c.execute(getFullName, (customerID[0],))
            fullName = list(c.fetchall())
            fullName = ' '.join(fullName[0])
            print('ACCOUNT OWNER: ', fullName)
            print()
            while True:
                try:
                    depositAmount = float(input("DEPOSIT AMOUNT: "))
                    clientName = input("CLIENT NAME: ").upper()

                    if depositAmount > 0:
                        getCurrentbalance = 'select `Balance` from `Account` where `AccountNumber`=%s'
                        c.execute(getCurrentbalance, (depositAccountNumber,))
                        currentBalance = c.fetchone()
                        newBalance = depositAmount + float(currentBalance[0])
                        deposit = 'update `Account` set `Balance` = %s where `AccountNumber`=%s'
                        c.execute(deposit, (newBalance, depositAccountNumber))
                        con.commit()
                        print()
                        print('PROCESSING...')
                        time.sleep(3)
                        recordTransaction = "insert into `Transaction` (`ID`, `type`, `Amount`, `FromName`, `ToAccountNumber`, `accountID`) values (default,'DEPOSIT',%s,%s,%s,%s)"
                        c.execute(recordTransaction, (depositAmount, clientName, depositAccountNumber,accountsID))
                        con.commit()
                        print()
                        print('DEPOSIT TRANSACTION DONE SUCCESSFULLY')
                        print()
                        break
                except ValueError:
                    print('INVALID INPUT')
                    print()
    except ValueError:
        print('INVALID INPUT')
        print()


def withdrawFromAccount(accountsID):
    print('WITHDRAWAL TRANSACTION')
    try:
        print()
        withdrawalAccountNumber = int(input("ACCOUNT NUMBER: "))
        print()

        withdrawalAccountNumber = int(withdrawalAccountNumber)
        getcustomerID = 'select `ID` from `Customer_Accounts_Account` where `AccountNumber`=%s'
        c.execute(getcustomerID, (withdrawalAccountNumber,))
        customerID = c.fetchone()
        if customerID == None:
            print()
            print('CUSTOMER ACCOUNT NOT FOUND')
            print()
        else:

            c.fetchall()
            # verifies account owner by returning the customer name
            getFullName = 'select `FirstName`, `LastName` from `Customer` where `ID`=%s'
            c.execute(getFullName, (customerID[0],))
            fullName = list(c.fetchall())
            fullName = ' '.join(fullName[0])

            print()
            print('VERIFY ACCOUNT OWNER BEFORE WITHDRAWAL...')
            time.sleep(3)
            print('ACCOUNT OWNER: ', fullName)
            print()
            while True:
                print()
                withdrawalAmount = float(input("WITHDRAWAL AMOUNT: "))
                print()

                if withdrawalAmount > 0:
                    getCurrentbalance = 'select `Balance` from `Account` where `AccountNumber`=%s'
                    c.execute(getCurrentbalance, (withdrawalAccountNumber,))
                    currentBalance = c.fetchone()
                    if float(currentBalance[0]) > 0 and float(currentBalance[0]) > withdrawalAmount:
                        newBalance = float(currentBalance[0]) - withdrawalAmount
                        deposit = 'update `Account` set `Balance` = %s where `AccountNumber`=%s'
                        c.execute(deposit, (newBalance, withdrawalAccountNumber))
                        con.commit()
                        print()
                        print('PROCESSING...')
                        time.sleep(3)
                        recordTransaction = "insert into `Transaction` (`ID`, `type`, `Amount`, `ToName`, `FromAccountNumber`,`accountID`) values (default,'WITHDRAWAL',%s,%s,%s,%s)"
                        c.execute(recordTransaction, (withdrawalAmount, fullName, withdrawalAccountNumber,accountsID))
                        con.commit()
                        print()
                        print('WITHDRAWAL COMPLETED')
                        break
                    else:
                        print('INSUFFICIENT FUNDS')
                else:
                    print('INVALID INPUT')

    except ValueError:
        print('INVALID INPUT')

    # should be able to update name(fname and lname), address(house address, town,country, postal code) and phone


def manageCustomerAccount():
    print()
    print('MANAGE CUSTOMER ACCOUNT')
    manageOptions()
    while True:
        print('ENTER CUSTOMER LAST NAME AND PHONE NUMBER TO PROCEED')
        lname = input("LAST NAME: ").upper()
        phone = input("PHONE: ")

        getaccountsID = "select `Accounts_id` from `Customer_Accounts_Account` where `LastName`=%s and `PhoneNumber`=%s"

        c.execute(getaccountsID, (lname, phone))
        accountsID = c.fetchall()

        if accountsID == None:
            print('CUSTOMER ACCOUNT NOT FOUND')
            print()
        else:
            break

    print()
    while True:
        try:
            print()
            choice = int(input('Manage Account Option: '))
            print()
            if choice == 1:

                checkCustomerAccount(lname, phone)

            elif choice == 2:
                depositIntoAccount(accountsID[0][0])
            elif choice == 3:
                withdrawFromAccount(accountsID[0][0])
            elif choice == 4:
                updateAccountInformation(lname, phone)
            elif choice == 5:
                break
            else:
                print('INVALID OPTION')
                print()
        except ValueError:
            print('INVALID INPUT')
            print()


def title():
    print("GENERIC BANKING TELLER/ADMIN SOFTWARE")
    print('*' * 40)
    print('Note: This a simulated banking application')
    print('Ensure You have an account created first and note down the account number')
    print('*' * 40)
    print()


def manageOptions():
    print()
    print('Please Note that making changes to a customer account is a sensitive operation')
    print('1. Check Active Accounts')
    print('2. Deposit Into Account')
    print('3. Withdraw from Account')
    print('4. Update Customer Personal Details')
    print('5. Back')
    print()


def menu():
    print('MENU OPTIONS:')
    print('1. Open A New Account ')
    print('2. Manage Customer Account')
    print('3. Exit')


def main():
    title()
    menu()
    while True:
        try:
            print()
            cmd = int(input('Select an option: '))
            print()
            if cmd == 1:
                openCustomerAccount()
            elif cmd == 2:
                manageCustomerAccount()
            elif cmd == 3:
                con.close()
                break
            else:
                print('INVALID OPTION')
                print()
        except ValueError:
            print()
            print('INVALID INPUT')


if __name__ == '__main__':
    main()
