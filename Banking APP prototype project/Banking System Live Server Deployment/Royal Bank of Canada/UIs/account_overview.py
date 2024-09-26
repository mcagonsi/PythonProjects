import sys
sys.path.append("../")
sys.path.append("../DBs")
sys.path.append("../funcs")
from funcs import biz_rules
import login_create_account
import time
from tkinter import ttk,messagebox
import tkinter as tk
from tkinter import *
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
from DBs import readDB as rdb
from dataclasses import dataclass
import account_operations as AO
from objs import actors as A
from objs import entity as E
import mysql.connector as db
con = db.connect(host='10.0.0.55', user='dera', passwd='', port=3306, database='rbcdb')
c = con.cursor()

@dataclass
class AccountOverviewMenu(tk.Tk):

    def __init__(self,OnlineBankingAccount):
        tk.Tk.__init__(self)
        self.title('RBC Account Overview')
        self.geometry('640x300')
        customerID = OnlineBankingAccount.customerID
        AccountsID = OnlineBankingAccount.accountsID
        CUSTOMER = rdb.getCustomerInfo(customerID)
        accounts = E.Accounts(AccountsID, customerID)


        #ACCOUNT OPERATION FUNCTIONS

        def sendMoney():
            self.destroy()
            AO.SendMoney(OnlineBankingAccount,CUSTOMER, accounts.showAccounts()).mainloop()

        def receiveMoney():
            receiveMoney = AO.ReceiveMoney(accounts)
            receiveMoney.mainloop()

        def transferMoney():
            self.destroy()
            AO.TransferMoney(OnlineBankingAccount, accounts).mainloop()

        def setTransactionPin():
            self.destroy()
            AO.SetTransactionsPin(customerID, AccountsID,OnlineBankingAccount).mainloop()


        def viewTransactionHistory():
            AO.TransactionHistory(AccountsID).mainloop()
            pass




        def createAccount():
            self.destroy()
            AO.CreateAccount(OnlineBankingAccount).mainloop()

        def closeAccount():
            # closes Online account
            self.destroy()
            AO.CloseAccount(CUSTOMER,OnlineBankingAccount).mainloop()

        def profileDetails():
            #shows the customer profile information
            self.destroy()
            AO.ProfileDetails(CUSTOMER, OnlineBankingAccount).mainloop()

        def changeLoginDetails():
            #used to update the online account login details
            self.destroy()
            AO.ChangeLoginDetails(OnlineBankingAccount).mainloop()


        def logout():
            self.destroy()
            time.sleep(2)
            login = login_create_account.Login()
            login.mainloop()
            con.close()
        def refresh():
            self.destroy()
            con.close()
            account_overview = AccountOverviewMenu(OnlineBankingAccount)
            account_overview.mainloop()

        accounts_overview = ttk.Frame(self,padding='15 15 15 15')
        accounts_overview.pack(fill=tk.BOTH, expand=True, side = LEFT)

        account_operations = ttk.Frame(self,padding='15 15 15 15')
        account_operations.pack(fill=tk.BOTH, expand=True, side = LEFT)

        # COMPONENTS IN THE ACCOUNTS OVERVIEW FRAME
        # for the owner name
        owner_name_label = ttk.Label(accounts_overview, text='OWNER NAME')
        owner_name_label.grid(row =1, column = 1, sticky = tk.E)


        owner_name_value = ttk.Label(accounts_overview, text=CUSTOMER.FullName)
        owner_name_value.grid(row =1, column = 2, columnspan =2, sticky = tk.W)

        # transc_history_button = ttk.Button(accounts_overview, text='View Transaction\n         History', width=15,command=setTransactionPin)
        # transc_history_button.grid(row=1, column=5, sticky=tk.E)

        #for the accountsID
        accountsID_label = ttk.Label(accounts_overview, text='ACCOUNTS ID')
        accountsID_label.grid(row =2, column = 1, sticky = tk.E)

        # accounts_id = getAccountsID()



        accountsID_value = ttk.Label(accounts_overview, text=AccountsID)
        accountsID_value.grid(row =2, column = 2, columnspan =2, sticky = tk.W)

        # for refreshing account
        refresh_button = ttk.Button(accounts_overview, text='Refresh', width=10, command=refresh)
        refresh_button.grid(row=3, column=1, sticky=tk.W)

        # for showing accounts
        account_label = ttk.Label(accounts_overview, text='ACCOUNT')
        account_label.grid(row =3, column = 2, sticky = tk.W)

        balance_label = ttk.Label(accounts_overview, text='BALANCE')
        balance_label.grid(row =3, column = 3,columnspan=2,sticky=tk.W)

        # loads active accounts for display on the account overview frame
        cust_accts = accounts.showAccounts()

        total = accounts.getTotalBalance()
        row = 4
        for account in cust_accts.values():

            account_name = ttk.Button(accounts_overview, text=account.accountType.name, command =viewTransactionHistory)
            account_name.grid(row=row, column=2, sticky=tk.W)

            account_balance = ttk.Label(accounts_overview,text = account.getBalance())
            account_balance.grid(row =row, column = 4, sticky = tk.W)
            row += 1


        total_balance_label = ttk.Label(accounts_overview, text='TOTAL BALANCE')
        total_balance_label.grid(row =row+2, column = 1, sticky = tk.W)

        # totalBalance = getAccountsTotalBalance() this will get the total balance using the Accounts class method
        total_balance = ttk.Label(accounts_overview, text=locale.currency(total,grouping=True),background='green',foreground='white',font=('Arial',12,'bold'))
        total_balance.grid(row =row+2, column = 4, sticky = tk.W)



        # COMPONENTS IN THE ACCOUNT OPERATIONS FRAME

        # For send Money
        send_money_button = ttk.Button(account_operations, text='Send Money', width=15, command=sendMoney)
        send_money_button.grid(row =0, column = 1, sticky = tk.E)

        # For Receive Money
        receive_money_button = ttk.Button(account_operations, text='Receive Money', width=15, command=receiveMoney)
        receive_money_button.grid(row=0, column=2, sticky=tk.W)

        # For Transfer Money
        transfer_money_button= ttk.Button(account_operations, text='Transfer Money', width=15, command=transferMoney)
        transfer_money_button.grid(row=1, column=1, sticky=tk.E)

        # For Set Transaction Pin
        set_pin_button = ttk.Button(account_operations, text='Set Transaction\n         Pin', width=15, command=setTransactionPin)
        set_pin_button.grid(row=1, column=2, sticky=tk.W)

        # For Create Account
        create_account_button= ttk.Button(account_operations, text='Create Account', width=15, command=createAccount)
        create_account_button.grid(row=2, column=1, sticky=tk.E)

        # For Delete Account
        close_account_button= ttk.Button(account_operations, text='Close Account', width=15, command=closeAccount)
        close_account_button.grid(row=2, column=2, sticky=tk.W)

        # For Close Account
        profile_details_button = ttk.Button(account_operations, text='Profile Details', width=15, command=profileDetails)
        profile_details_button.grid(row=3, column=1, sticky=tk.E)

        # For Deactivate Account
        change_login_details_button = ttk.Button(account_operations, text='Change Login \n      Details', width=15, command=changeLoginDetails)
        change_login_details_button.grid(row=3, column=2, sticky=tk.W)

        # For Log out
        logout_button = ttk.Button(account_operations, text='Logout', width=15, command=logout)
        logout_button.grid(row=4, column=1, sticky=tk.E)

        # For Exit
        exit_button = ttk.Button(account_operations, text='Exit', width=15, command=exit)
        exit_button.grid(row=4, column=2, sticky=tk.W)

        for child in account_operations.winfo_children():
            child.grid_configure(padx=10, pady=10)
        for child in accounts_overview.winfo_children():
            child.grid_configure(padx=8, pady=8)





