# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 22:53:07 2023

@author: Chidera
"""
import pickle
import csv

'''CONTAINS ALL THE REQUIRED FUNCTIONS FOR THE SOFTWARE IN GENERAL'''


def checkPassword(password:str)-> bool:
    '''
    

    Parameters
    ----------
    password : str
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    if len(password) > 6  :
        c = 0
        n = 0
        for i in password:
            if i.isdigit():
                n+=1
            if i.isupper():
                c += 1
        if c > 0 and n > 0:
            return True
        else:
            print('Password must contain atleast one uppercase and one numeric character!')
            return False
    else:
        print('Password must be atleast 6 Characters Long')
def checkUsername(username:str)->bool:
    '''
    

    Parameters
    ----------
    username : str
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    
    with open ('login.pswd', 'rb') as logins:
        staffs = pickle.load(logins)
        if username in staffs.keys():
            return True
        else:
            print('Invalid username! ')
            return False

def validatePassword(username:str, password:str)->bool:
    '''
    

    Parameters
    ----------
    username : str
        DESCRIPTION.
    password : str
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    
    with open('login.pswd', 'rb') as logins:
        staffs = pickle.load(logins)
        if staffs[username] == password:
            return True
        else:
           
            return False

def readStaffList()->list:
    '''
    

    Returns
    -------
    list
        DESCRIPTION.

    '''
    
    with open('staff.csv') as staff:
        stafflist = csv.reader(staff)
        staffList = list(stafflist)
        staffList.pop(0)
        return staffList
    
def writeStaffList(employees:list):
    '''
    

    Parameters
    ----------
    employees : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    with open('staff.csv', 'w', newline='') as staff:
        stafflist = csv.writer(staff)
        employees.insert(0,['Username', 'First Name', 'Last Name', 'Contact','Role'])
        stafflist.writerows(employees)

def readLogin()->dict:
    '''
    

    Returns
    -------
    dict
        DESCRIPTION.

    '''
    
    with open('login.pswd','rb') as logins:
        Logins = pickle.load(logins)
        return Logins
        
def writeLogin(logins:dict):
    '''
    

    Parameters
    ----------
    logins : dict
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    with open('login.pswd','wb') as staffLogins:
        pickle.dump(logins,staffLogins)
    
def readPins()->dict:
    '''
    

    Returns
    -------
    dict
        DESCRIPTION.

    '''
    
    with open('sales.pins','rb') as pins:
        Pins = pickle.load(pins)
        return Pins
    
def validatePins()->dict:
    '''
    

    Returns
    -------
    dict
        DESCRIPTION.

    '''
    with open('sales.pins','rb') as pins:
        Pins = pickle.load(pins)
        return Pins
        
def writePins(Pins:dict):
    '''
    

    Parameters
    ----------
    Pins : dict
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    with open('sales.pins','wb') as salesPins:
        pickle.dump(Pins,salesPins)

        
def readInventory()->list:
    '''
    

    Returns
    -------
    list
        DESCRIPTION.

    '''
    
    with open('Inventory.csv') as inventory:
        products = csv.reader(inventory)
        products = list(products)
        products.pop(0)
        return products
    
def writeInventory(products:list):
    '''
    

    Parameters
    ----------
    products : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    with open ('Inventory.csv', 'w', newline='') as inventory:
        Products = csv.writer(inventory)
        products.insert(0,['Barcode','Product Name','Price','Status'])
        Products.writerows(products)

def readReceipts()->list:
    '''
    

    Returns
    -------
    list
        DESCRIPTION.

    '''
    with open('Receipts_log.csv') as receipts:
        Receipts = csv.reader(receipts)
        receiptsLog = list(Receipts)
        receiptsLog.pop(0)
        return receiptsLog


def writeReceipts(Receipts:list):
    '''
    

    Parameters
    ----------
    Receipts : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    with open('Receipts_log.csv', 'w', newline= '') as receipts:
        receiptsLog = csv.writer(receipts)
        Receipts.insert(0,['Receipt Number','Items Barcode','Total Price','Seller', 'Transc.'])
        receiptsLog.writerows(Receipts)
            
def updateInventory(products:list,lineItems:list):
    '''
    

    Parameters
    ----------
    products : list
        DESCRIPTION.
    lineItems : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    for product in products:
        for item in lineItems:
            if product[0] == item[0]:
                product[3] = 'SOLD'
                
def readReceiptSales()->list:
    '''
    

    Returns
    -------
    list
        DESCRIPTION.

    '''
    with open('Receipts_log.csv') as receipts:
        Receipts = csv.reader(receipts)
        receiptsLog = list(Receipts)
        receiptsLog.pop(0)
        return receiptsLog
    

            
                    