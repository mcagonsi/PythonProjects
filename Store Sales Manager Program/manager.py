# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 23:46:37 2023

@author: Chidera
"""
import software_functions as sf
import locale as lc
country = lc.getlocale()
lc.setlocale(lc.LC_ALL, country)
def title():
    print()
    print()
    print('***********STORE  SALES  MANAGER  PROGRAM***********')
    print()
    print('******MANAGER  TOOLS******')
    print()
def menu():
    print('MENU   OPTIONS: '+
          '\n1. Add sales employee'+
          '\n2. Edit employee info' +
          '\n3. Remove sales employee'+
          '\n4. view current staff list'+
          '\n5. View total sales by staff'+
          '\n6. View total returns by staff'+
          '\n7. Exit')
    print()
    print()

def addEmployee():
    try:
        # reads logins file,staff list file, and pins file
        logins = sf.readLogin()
        employees = sf.readStaffList()
        Pins = sf.readPins()
    except FileNotFoundError:
        # creates an empty file if file is not found
        logins = {}
        employees = []
        pins = {}
        sf.writePins(pins)
        sf.writeLogin(logins)
        sf.writeStaffList(employees)
    
    #takes all the required inputs, puts them in their respective object form 
    print('Onboarding process for your sales employees')
    print()
    while True:
        username = input('Staff Username:  ').upper()
        if username in logins.keys():
            print('Username already exists!')
        else:
            break
    
    firstName = input('First Name: ').title()
    lastName = input('Last Name: ').title()
    contact = input('Phone Number:  ')
    role = input('Role (worker/supervisor) :  ')
    while True:
        salesPin = input('Sales pin:  ')
        if len(salesPin) == 4 and salesPin.isdigit():
            Pins[salesPin] = username
            break
        else:
            print('Sales pin must be 4 digits!')
        
    while True:
        password = input('Password: ')
        check = sf.checkPassword(password)
        if check == True:
            logins[username] = password
            break
        else:
           
            continue
    # this writes the info to the respective files
    staffInfo = [username, firstName, lastName, contact, role]
    employees.append(staffInfo)
    sf.writeLogin(logins)
    sf.writeStaffList(employees)
    sf.writePins(Pins)
    
    print()
    print('Employee has been added to the Sales Force!')

def editEmployee():
    try:
        # reads the staff list file
        employees = sf.readStaffList()
        if len(employees) == 0:
            print('Staff list is empty. Add an employee')
            print()
        else:
            while True:
                username = input('Employee Username:  ').upper()
                usernames = []
                
                # validates the username if present
                for employee in employees:
                    usernames.append(employee[0])
                if username in usernames:
                    i = usernames.index(username)
                    print(f'{username} has been selected')
                    break
                else:
                    print('Username does not exist!')
            print()
            print('Manage employee info: ' +
                  '\n1. Change First Name.' +
                  '\n2. Change Last Name.' +
                  '\n3. Change contact.' +
                  '\n4. Change role' +
                  '\n5. Exit')
            print()
            while True:
                option = int(input('Info to change:  '))
                if option == 1:
                    employees[i][1] = input('Enter New First Name: ').title()
                    print('Name changed successfully.')
                    
                elif option == 2:
                    employees[i][2] = input('Enter New Last Name:  ').title()
                    print('Name has been changed successfully')
                    
                elif option == 3:
                    employees[i][3] = input('Enter New Contact:  ')
                    print('Contact info has been change successfully')
                    
                elif option == 4:
                    employees[i][4]= input('Update Role (worker/supervisor):  ')
                    print('Role updated')
                    
                elif option == 5:
                    break
                else:
                    print('Invalid option!')
                sf.writeStaffList(employees)
            
    except FileNotFoundError:
        print('There are no employees on the list. Add an employee first.')
    except Exception:
        print('An Unexpected Error Occurred!')
    
def removeEmployee(): #this function handles removing of employee details, including pins and passwords
    try:
        logins = sf.readLogin()
        employees = sf.readStaffList()
        Pins = sf.readPins()
        if len(employees)== 0:
            print('Staff list is empty. Add an employee')
        else:
            while True:
                username = input('Employee Username:  ').upper()
                usernames = []
                for employee in employees:
                    usernames.append(employee[0])
                if username in usernames:
                    i = usernames.index(username)
                    
                    break
                else:
                    print('Username does not exist!')
            employees.pop(i)
            del logins[username]
            for user in list(Pins.items()):
                if username in user:
                    del Pins[user[0]]
            
            print(f'{username} has been removed from the Sales Force successfully.')
            
            sf.writeLogin(logins)
            sf.writeStaffList(employees)
            sf.writePins(Pins)
            
    except FileNotFoundError:
        print('There are no employees on the list. Add an employee first.')
    except Exception:
        print('An Unexpected Error Occurred!')
        
def viewStaffList(): #checks the number of current staff and presents it as a list with names and roles
    try:
        employees = sf.readStaffList()
        if len(employees) == 0:
            print('Staff list is empty. Add an employee')
        else:
            print(f"  {'Name':20} {'Role':>10}")
            print('='*43)
            for i, employee in enumerate(employees, start = 1):
                s=5
                print('{}. {:10} {:10} {:>10}'.format(i,employee[1],employee[2],employee[4]))
            
            print()
            print()
            print('Total number of staff: {}'.format(len(employees)))
            print('='*43)
        
    except FileNotFoundError:
        print('There are no employees on the list. Add an employee first.')
    except Exception:
        print('An Unexpected Error Occurred!')
    
    
def viewStaffSales(): #presents info on the total sales made by each worker
    Receipts = sf.readReceiptSales()
    staff = list(set([Receipt[-2] for Receipt in Receipts]))
    
    print(f"{'EMPLOYEE':15} {'SALE':>10}")
    print('='*40)
    print()
    for user in staff:
        userSales = []
        for Receipt in Receipts:
        
            if user in Receipt and Receipt[-1]=='SALE':
                
                userSales.append(float(Receipt[2]))
        totalSales = sum(userSales) - sum(userSales) * 0.15

        print('{:15} {:>10}'.format(user,lc.currency(totalSales)))
    print()
    print('='*40)
    print()

def viewStaffReturns(): #presents info on the total returns made by each worker
    Receipts = sf.readReceiptSales()
    staff = list(set([Receipt[-2] for Receipt in Receipts]))
    
    print(f"{'EMPLOYEE':15} {'RETURNS':>10}")
    print('='*40)
    print()
    for user in staff:
        userReturns = []
        for Receipt in Receipts:
        
            if user in Receipt and Receipt[-1]=='RETURN':
                
                userReturns.append(float(Receipt[2]))
        totalReturns = sum(userReturns) - sum(userReturns) * 0.15

        print('{:15} {:>10}'.format(user,lc.currency(totalReturns)))
    print()
    print('='*40)
    print()
                
    
def main():
    title()
    while True:
        print()
        menu()
        print()
        try:
            option = int(input('Option:  '))
            print()
            if option == 1:
                addEmployee()
                
            elif option == 2:
                editEmployee()
            elif option == 3:
                removeEmployee()
            elif option == 4:
                viewStaffList()
            elif option == 5 :
                viewStaffSales()
            elif option == 6:
                viewStaffReturns()
            elif option == 7:
                break
            else:
                print
                print('Invalid option!')
                print()
        except ValueError:
            print()
            print('Numeric Value expected')
            print()
    
if __name__ == '__main__' :
    main()

