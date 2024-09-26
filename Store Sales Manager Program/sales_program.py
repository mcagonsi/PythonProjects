# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 10:56:09 2023

@author: Chidera
"""

import software_functions as sf

def title():
    print()
    print('********SALES   PROGRAM********')
    print()
    print()
def menu ():
    print('Options: '+
          '\n1. Enter sale' +
          '\n2. Returns'+
          '\n3. Exit' ) 
    
def sales(): 
    ''' handles sales transaction by reading barcode for each item, presenting the final cost,
        authenticating with a workers pin, changing the status of the item in inventory and 
        writing to receipts log file'''
    print('ENTER A SALE')
    try:
        products = sf.readInventory()
        barcodes = [str(product[0]) for product in products]
        
           
        lineItems = []
        while True:
            
            print()
            barcode = input("Product Barcode ('x' to cancel) :  ")
            print()
            if barcode.lower() == 'x':
                break
            elif not barcode.isdigit():
                print()
                print('Invalid Entry')
                print()
            else:
                if barcode in barcodes:
                    i = barcodes.index(barcode)
                    if products[i][3] == 'AVL':
                        lineItems.append(products[i])
                        print('Item has be added.')
                        print()
                    else:
                        print('ITEM SOLD')
                        print()
                else:
                    print()
                    print('Product is not in inventory')
                    print()
                    
                print()
                prompt = input('Add more items? (y/n):  ').lower() 
                print()
                if prompt == 'n' and len(lineItems)==0:
                    break
                elif prompt == 'n':
                    print()
                    print(f'{len(lineItems)} ITEM(S) TO BUY')
                    print('='*60)
                    print()
                    print('PRODUCT  NAME\t\t\t\t\t\t\tPRICE')
                    print()
                    for i,item in enumerate(lineItems, start=1):
                        s=37
                        print('{}. {}{}{}'.format(i,item[1],' '*(s-len(item[1])), item[2]))
                    print('='*60)
                    totalCost = sum([float(item[2]) for item in lineItems])
                    totalHST = sum([float(item[2]) for item in lineItems]) * 0.15
                    finalCost = sum([float(item[2]) for item in lineItems]) *1.15
                    print('TOTAL COST:\t\t\t\t${:,.2f}'.format(totalCost))
                    print('TAXES:\t\t\t\t\t${:,.2f}'.format(totalHST))
                    print('FINAL COST:\t\t\t\t${:,.2f}'.format(finalCost))
                    
                    while True:
                        Pins = sf.validatePins()
                        print()
                        salespin = input("PIN: ")
                        
                        if salespin in Pins.keys():
                            seller = Pins[salespin]
                            try:
                                Receipts = sf.readReceipts()
                                lineItemsBarcodes = ' '.join([str(item[0]) for item in lineItems])
                                if len(Receipts) == 0:
                                    receiptNumber = 100000
                                    
                                    Receipt = [str(receiptNumber),lineItemsBarcodes,round(finalCost,2),seller,'SALE']
                                else:
                                    receiptNumber = int(Receipts[-1][0]) + 1
                                    Receipt = [str(receiptNumber),lineItemsBarcodes,round(finalCost,2),seller,'SALE']
                                Receipts.append(Receipt)
                                print('Transaction Completed Successfully')
                                print()
                                sf.writeReceipts(Receipts)
                                sf.updateInventory(products, lineItems)
                                sf.writeInventory(products)
                                break
                            
                            except FileNotFoundError:
                                sampleReceipts = []
                                sf.writeReceipts(sampleReceipts)
                                print('Receipts Log File Created')
                                continue
                        else:
                            print('Invalid Pin!')
                    break
                elif prompt.lower() == 'y':
                    continue
                else:
                    print('Invalid response')
                        
        
        
    except FileNotFoundError:
        print('Nothing in Inventory. Add products!')
        
    
        
    
def returns():
    '''Handles returns transactions by taking invoice number input, validating in the system,
        presenting the refund ammount and authenticating the transaction with a workers pin,
        as well as writing the receipts log file'''
    print('********RETURNS********')
    print()
    Receipts = sf.readReceipts()
    products = sf.readInventory()
    receiptNumbers = [receipt[0] for receipt in Receipts]
    while True:
        print()
        enterReceipt = input("Receipt Number ('x to cancel'):  ")
        if enterReceipt.lower() == 'x':
            break
        elif enterReceipt.isdigit():
            print()
            if enterReceipt in receiptNumbers:
                i = receiptNumbers.index(enterReceipt)
                returnReceipt = Receipts[i]
                moneyRefund = returnReceipt[2]
                returnItems= returnReceipt[1].split()
                for product in products:
                    for item in returnItems:
                        if item == str(product[0]):
                            product[3] = 'AVL'
                print()
                print(f'{len(returnItems)} ITEM(S)  FOR   RETURN')
                print('='*40)
                print('')
                n=1
                for product in products:
                    for item in returnItems:
                        if item in product:
                            print('{}. {}'.format(n,product[1]))
                            n+=1
                print('')
                print('='*40)
                print('REFUND AMOUNT: ${:,.2f}'.format(float(moneyRefund)))
                print()
                while True:
                    print()
                    Pins = sf.validatePins()
                    
                    salespin = input('PIN: ')
                    
                    if salespin in Pins.keys():
                        seller = Pins[salespin]
                        try:
                            Receipts = sf.readReceipts()
                            if len(Receipts) == 0:
                                receiptNumber = 100000
                                
                                Receipt = [str(receiptNumber),' '.join(returnItems),round(float(moneyRefund),2),seller,'RETURN']
                            else:
                                receiptNumber = int(Receipts[-1][0]) + 1
                                Receipt = [str(receiptNumber),' '.join(returnItems),round(float(moneyRefund),2),seller,'RETURN']
                            Receipts.append(Receipt)
                            print('Transaction Completed Successfully')
                            print()
                            print('='*40)
                            sf.writeReceipts(Receipts)
                            sf.writeInventory(products)
                            break
                        except FileNotFoundError:
                            sampleReceipts = []
                            sf.writeReceipts(sampleReceipts)
                            print('Receipts Log File Created')
                            continue
            else:
                print()
                print('RECEIPT NOT FOUND')
                print()
        else:
            print('\nINVALID ENTRY\n')
         
        
    
def main():
    title()
    while True:
        menu()
        print()
        try:
            option = int(input('Option:  '))
            print()
            if option == 1:
                sales()
            elif option == 2:
                returns()
            elif option == 3:
                break
            else:
                print()
                print('Invalid Option')
                print()
        except ValueError:
            print()
            print('Numeric Input Expected')
            print()
        except Exception:
            print()
            print('Unexpected Error Occured')
            print()
if __name__ == '__main__':
    main()