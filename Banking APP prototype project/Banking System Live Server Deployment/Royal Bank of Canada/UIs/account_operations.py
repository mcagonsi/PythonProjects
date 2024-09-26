import sys
sys.path.append("../")
sys.path.append("../DBs")
sys.path.append("../funcs")
sys.path.append('../APIs')
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import *
from dataclasses import dataclass
from funcs import biz_rules as br
import time
import account_overview as acct_ov
import login_create_account as login
from DBs import readDB as rdb
from DBs import writeDB as wdb
from objs import entity as E
from objs import abstracts as A
from objs import actors as I



# THESE IMPORTS WILL ACT LIKE THE IPs FOR SIMULATING API CALLS
# for ScotiaBank
import ScotiaAPI as SCOTIA
#for TESLA Bank
import TeslaAPI as TESLA
# FOR RBC
import RBCanada as RBC
# FOR TDBANK
import TDBankAPI as TDBANK


BANKS_API = [SCOTIA.API(),TESLA.API(),RBC.API(),TDBANK.API()]


@dataclass
class ReceiveMoney(tk.Tk):
    def __init__(self, accounts):
        tk.Tk.__init__(self)
        self.title('Receive Money')
        self.resizable(False, False)
        self.geometry('250x200')

        frame = ttk.Frame(self)
        frame.pack(expand = True, fill=tk.BOTH)
        account_label = Label(frame, text='ACCOUNT', font=('Arial', 10, 'bold'))
        account_label.grid(row=1, column=2, sticky=tk.W)

        balance_label = Label(frame, text='ACCOUNT NUMBER', font=('Arial', 10, 'bold'))
        balance_label.grid(row=1, column=4, sticky=tk.E)

        cust_accts = accounts.showAccounts()
        row = 4
        for account in cust_accts.values():
            # for account name
            account_name = ttk.Label(frame, text=account.accountType.name)
            account_name.grid(row=row, column=2, sticky=tk.W)

            acct_num = list(str(account.accountNumber))
            acct_num.insert(4, '-')
            acct_no = ''.join(acct_num)
            account_balance = ttk.Label(frame, text=acct_no)
            account_balance.grid(row=row, column=4, sticky=tk.W)
            row +=1

        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=10)


@dataclass
class SetTransactionsPin(tk.Tk):
    def __init__(self, customerID, AccountsID, OnlineBankingAcct):
        tk.Tk.__init__(self)
        self.title('Set Transaction Pin')
        self.resizable(False, False)
        self.geometry('300x220')
        frame = ttk.Frame(self)
        frame.pack(expand = True, fill=tk.BOTH)

        def savePin():
            try:
                if pin.get()== '' and cpin.get()== '':
                   self.destroy()
                   acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
                else:
                    New_pin = int(pin.get())
                    Cnew_pin = int(cpin.get())
                    if len(pin.get()) == 4:
                        if New_pin == Cnew_pin:
                            save = br.savepin(Cnew_pin)
                            if save == True:
                                time.sleep(2)
                                messagebox.showinfo('Success', 'Pin has been saved!')

                                self.destroy()
                                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
                            else:
                                messagebox.showinfo('Error', 'Something went wrong!')
                                self.destroy()
                        else:
                            not_equal = Label(frame, text='PINS must be equal', font=('Arial', 6, 'bold'),fg = 'red')
                            not_equal.grid(row=3, column=2, sticky=tk.E)
                    else:
                        messagebox.showwarning('Error', 'Pin must be 4 digits')
            except ValueError:
                messagebox.showwarning('Warning', 'PIN must be Integers')


        Note = Label(frame, text=' NOTE: Changes to PIN will only be made if\n    you fill in new pin else old pin will remain.'.center(100), font=('Arial', 9, 'bold'),fg='red')
        Note.grid(row=0, column=0,columnspan=5, sticky=tk.EW)

        pin_label = Label(frame, text='PIN:', font=('Arial', 10))
        pin_label.grid(row=1, column=2, sticky=tk.E)

        pin = tk.StringVar()
        pin_entry = ttk.Entry(frame,show='*', textvariable=pin)
        pin_entry.grid(row=1, column=3, sticky=tk.W)


        cpin_label = Label(frame, text='CONFIRM PIN:', font=('Arial', 10))
        cpin_label.grid(row=2, column=2, sticky=tk.E)

        cpin = tk.StringVar()
        cpin_entry = ttk.Entry(frame,show='*', textvariable=cpin)
        cpin_entry.grid(row=2, column=3, sticky=tk.W)

        confirm = ttk.Button(frame, text= 'CONFIRM', width=25, command=savePin)
        confirm.grid(row=3, column=3, sticky=tk.W)

        cancel = ttk.Button(frame, text='CANCEL', width=25, command=self.destroy)
        cancel.grid(row=4, column=3, sticky=tk.W)



        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=8)

CUSTOMER = rdb.getCustomerInfo(1)
@dataclass
class ProfileDetails(tk.Tk):
    def __init__(self, CUSTOMER,OnlineBankingAcct):
        tk.Tk.__init__(self)
        self.title('Profile Details')
        self.resizable(False, False)
        self.geometry('320x500')
        frame = ttk.Frame(self)
        frame.pack(expand = True, fill=tk.BOTH)

        def cancel():
            self.destroy()
            acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()


        def update():
            decrypted = br.decrypt(OnlineBankingAcct.password.encode('utf-8'))
            rpin = br.getpin()
            if phone.get() == '' or pin.get()=='' or password.get()=='':
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=5, column=4, sticky=tk.E)
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=7, column=4, sticky=tk.E)
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=8, column=4, sticky=tk.E)
            else:
                if password.get() == decrypted and pin.get() == str(rpin):
                    if phone.get() == CUSTOMER.PhoneNumber:
                        self.destroy()
                        acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
                    else:
                        if len(phone.get()) == 10:
                            update=wdb.updatePhoneNumber(phone.get(), CUSTOMER.CustomerID)

                            if update == True:
                                time.sleep(1)
                                messagebox.showinfo('Success', 'Phone number successfully updated!')
                                self.destroy()
                                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
                            else:
                                messagebox.showerror('Failed', 'Phone number not updated!\n Something went Wrong.')
                        else:
                            messagebox.showinfo('Error', 'Phone number must be 10 digits')
                else:
                    messagebox.showwarning('Invalid', 'Password or Pin incorrect!')


        note = Label(frame, text='Note: To update phone number you must \n confirm with password and pin.', font=('Arial', 10, 'bold'),fg='red')
        note.grid(row=0, column=1,columnspan=4)

        name_label = ttk.Label(frame, text='Name:', font=('Arial', 10))
        name_label.grid(row=1, column=2, sticky=tk.E)

        name = tk.Label(frame, text=CUSTOMER.FullName)
        name.grid(row=1, column=3, sticky=tk.W)

        dateOfBirth_label = ttk.Label(frame,text = 'Date of Birth:', font=('Arial', 10))
        dateOfBirth_label.grid(row=2, column=2, sticky=tk.W)

        dateofBirth = tk.Label(frame, text=CUSTOMER.DateOfBirth, font=('Arial', 10))
        dateofBirth.grid(row=2, column=3, sticky=tk.W)


        gender_label = ttk.Label(frame, text='Gender:', font=('Arial', 10))
        gender_label.grid(row=3, column=2, sticky=tk.E)

        gender = tk.Label(frame, text=CUSTOMER.Gender)
        gender.grid(row=3, column=3, sticky=tk.W)

        relationship_label = ttk.Label(frame, text='Relationship:', font=('Arial', 10))
        relationship_label.grid(row=4, column=2, sticky=tk.E)

        relationship = tk.Label(frame, text=CUSTOMER.Relationship)
        relationship.grid(row=4, column=3, sticky=tk.W)

        phone_label = ttk.Label(frame, text='Phone:', font=('Arial', 10))
        phone_label.grid(row=5, column=2, sticky=tk.E)

        phone = tk.StringVar()
        phone.set(CUSTOMER.PhoneNumber)
        phone_label = ttk.Entry(frame, textvariable=phone)
        phone_label.grid(row=5, column=3, sticky=tk.W)

        address_label = ttk.Label(frame, text='Address:', font=('Arial', 10))
        address_label.grid(row=6, column=2, sticky=tk.E)

        address_value = ttk.Label(frame, text=CUSTOMER.FullAddress)
        address_value.grid(row=6, column=3, sticky=tk.W)

        password_label = ttk.Label(frame, text='Password:', font=('Arial', 10))
        password_label.grid(row=7, column=2, sticky=tk.E)

        password = tk.StringVar()
        password_entry = ttk.Entry(frame,show='*', textvariable=password)
        password_entry.grid(row=7, column=3, sticky=tk.W)

        pin_label = ttk.Label(frame, text='PIN:', font=('Arial', 10))
        pin_label.grid(row=8, column=2, sticky=tk.E)

        pin = tk.StringVar()
        pin_entry = ttk.Entry(frame,show='*', textvariable=pin)
        pin_entry.grid(row=8, column=3, sticky=tk.W)

        update_button = ttk.Button(frame, text='Update', command=update)
        update_button.grid(row=9, column=2, sticky=tk.E)

        back_button = ttk.Button(frame, text='Back', command=cancel)
        back_button.grid(row=9, column=3, sticky=tk.W)




        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=10)


@dataclass
class SendMoney(tk.Tk):

    def __init__(self,OnlineBankingAcct, CUSTOMER,accounts):
        self._RECIPIENT = None
        tk.Tk.__init__(self)
        self.title('Send Money')
        self.resizable(False, False)
        self.geometry('350x380')
        frame = ttk.Frame(self,padding='10 10 10 10')
        frame.pack(expand = True, fill=tk.BOTH)
        global BANKS_API
        banks = [bank.name for bank in BANKS_API]
        banks.insert(0,'Select Bank')

        def cancel():
            self.destroy()
            acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
        def validate():
            if bank.get() == 'Select Bank':
                messagebox.showwarning('Warning', 'Please Select Bank')
            else:
                for api in BANKS_API:
                    if api.name == bank.get():

                        if acct_number.get() == ''  or amount.get() == '':
                            required = ttk.Label(frame, text='required', font=('Arial', 7), foreground='red')
                            required.grid(row=3, column=4, sticky=tk.W)
                            required_no = ttk.Label(frame, text='required', font=('Arial', 7), foreground='red')
                            required_no.grid(row=2, column=4, sticky=tk.W)
                        else:
                            try:
                                if int(acct_number.get()) in accounts:
                                    messagebox.showerror('Error','Cannot Send Money to Your Account')
                                else:
                                    recipientBank, recipientAccount, recipient = api.get(int(acct_number.get()))
                                    time.sleep(2)
                                    if api.status == 404:
                                        messagebox.showwarning('Validation Failed','Customer not Found')
                                    elif api.status == 200:

                                        recipient_name.set(recipient.FullName)

                                        try:
                                            if isinstance(float(amount.get()), float):
                                                pass
                                        except ValueError:
                                            messagebox.showwarning('Validation Failed', 'Amount must be numeric')

                                        self._RECIPIENT = I.ExternalClient(recipientBank, recipient.FullName,recipientAccount.accountNumber,float(amount.get()))
                                    else:
                                        messagebox.showwarning('Failed', 'Something went wrong')
                            except ValueError:
                                messagebox.showwarning('Validation Failed', 'Account Number must be numeric')


        def confirm():
            if transaction_pin.get() == "":
                pin_required = ttk.Label(frame, text='required', font=('Arial', 7), foreground='red')
                pin_required.grid(row=5, column=4, sticky=tk.W)
            elif isinstance(int(transaction_pin.get()),int):
                if int(transaction_pin.get()) == br.getpin():
                    if bank.get() == 'Select Bank' or bank.get()== '':
                        messagebox.showwarning('Transaction Failed','Please Select Bank and Fill other details')
                    else:
                        for account in accounts.values():
                            if int(account.accountType.id) == 1:
                                if int(amount.get()) <= account.balance:
                                    DEBIT_TRANSACTION = E.Transaction(0,0,'DEBIT',float(amount.get()),None,RBC.API().name,account.accountType.name,account.accountNumber,self._RECIPIENT.bankName, self._RECIPIENT.FullName, self._RECIPIENT.accountNumber,'success')
                                    CREDIT_TRANSACTION = E.Transaction(0,0,'CREDIT',float(amount.get()),None,RBC.API().name,CUSTOMER.FullName,account.accountNumber,self._RECIPIENT.bankName,account.accountType.name, self._RECIPIENT.accountNumber,'success')

                                    debit = account.debitAccount(DEBIT_TRANSACTION)
                                    if debit == True:
                                        for api in BANKS_API:
                                            if api.name == bank.get():
                                                api.post(CREDIT_TRANSACTION)
                                                if api.status == 200:
                                                    time.sleep(2)
                                                    messagebox.showinfo('Successful', 'Money Sent')
                                                    self.destroy()
                                                    acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
                                                elif api.status == 400:
                                                    messagebox.showwarning('Failed', 'Money Not Sent')
                                                else:
                                                    messagebox.showwarning('Failed', 'Something went wrong')
                                else:
                                    messagebox.showwarning('Failed', 'Insufficient Funds')
                else:
                    messagebox.showerror('Invalid Pin','Wrong Transaction Pin, please try again')

            else:
                messagebox.showwarning('Failed','Pin must be numeric')




        note = Label(frame,text='Note: Money can only be sent from Chequing Account \n if Checking balance is 0, transfer from other account',font=('Arial', 7, 'bold'),fg='red')
        note.grid(row=0, column=1,columnspan=3)

        bankName_label = ttk.Label(frame, text='Bank Name:', font=('Arial', 10))
        bankName_label.grid(row=1, column=2, sticky=tk.E)



        bank = StringVar()
        bank_menu = ttk.OptionMenu(frame, bank, *banks)
        bank_menu.grid(row=1, column=3, sticky=tk.W)

        acct_number_label = ttk.Label(frame, text='Account Number:', font=('Arial', 10))
        acct_number_label.grid(row=2, column=2, sticky=tk.E)

        acct_number = tk.StringVar()
        acct_number_entry = ttk.Entry(frame, textvariable=acct_number)
        acct_number_entry.grid(row=2, column=3, sticky=tk.W)

        amount_label = ttk.Label(frame, text='Amount:', font=('Arial', 10))
        amount_label.grid(row=3, column=2, sticky=tk.E)

        amount = tk.StringVar()
        amount_entry = ttk.Entry(frame, textvariable=amount)
        amount_entry.grid(row=3, column=3, sticky=tk.W)

        validate_button = ttk.Button(frame, text='Validate', command=validate)
        validate_button.grid(row=4, column=2, sticky=tk.W)

        recipient_name = tk.StringVar()
        recipient_name_entry = ttk.Entry(frame, textvariable=recipient_name, state='readonly')
        recipient_name_entry.grid(row=4, column=3, sticky=tk.W)


        pin_label = ttk.Label(frame, text='PIN:', font=('Arial', 10))
        pin_label.grid(row=5, column=2, sticky=tk.E)

        transaction_pin = tk.StringVar()
        transaction_pin_entry = ttk.Entry(frame, textvariable=transaction_pin,show='*')
        transaction_pin_entry.grid(row=5, column=3, sticky=tk.W)

        confirm_button = ttk.Button(frame, text= 'CONFIRM', command=confirm)
        confirm_button.grid(row=6, column=2, sticky=tk.E)

        cancel_button = ttk.Button(frame, text= 'CANCEL', command=cancel)
        cancel_button.grid(row=6, column=3, sticky=tk.W)

        for child in frame.winfo_children():
            child.grid_configure(padx=12, pady=12)

@dataclass
class TransferMoney(tk.Tk):
    def __init__(self,OnlineBankingAcct,accounts):
        tk.Tk.__init__(self)
        self.title('Transfer Money')
        self.resizable(False, False)
        self.geometry('350x250')
        frame = ttk.Frame(self,padding='10 10 10 10')
        frame.pack(expand = True, fill=tk.BOTH)
        ACCTS = accounts.showAccounts()
        accts = [acct.accountType.name for acct in ACCTS.values()]
        accts.insert(0, 'Select Account Type')

        def cancel():
            self.destroy()
            acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()

        def transfer():
            # this should select one option from the options and check the value
            if from_option.get() == accts[0] or to_option.get() == accts[0]:
                messagebox.showinfo('Warning','You must select an account')
            else:
                if from_option.get() == to_option.get():
                    messagebox.showinfo('Failed', 'Cannot transfer to same account')
                else:
                    from_acct = None
                    to_acct = None
                    for acct in ACCTS.values():
                        if acct.accountType.name == from_option.get():
                            from_acct = acct
                        elif acct.accountType.name == to_option.get():
                            to_acct = acct
                    try:
                        if float(amount.get()) <= float(from_acct.balance):
                            transfer = wdb.recordTransferTransaction(from_acct.accountsID,float(amount.get()),from_acct,to_acct)
                            if transfer == True:
                                time.sleep(1)
                                messagebox.showinfo('Success', 'Transfer successful')
                                self.destroy()
                                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
                            else:
                                messagebox.showinfo('Failed', 'Transfer failed')
                        else:
                            messagebox.showinfo('Failed', 'Insufficient Funds')
                    except ValueError:
                        messagebox.showinfo('Failed', 'Something went wrong \n Please Enter Only Numbers')




        amount_label = ttk.Label(frame, text='Amount:', font=('Arial', 10))
        amount_label.grid(row=1, column=2, sticky=tk.E)

        amount = StringVar()
        amount_entry = ttk.Entry(frame, textvariable=amount)
        amount_entry.grid(row=1, column=3, sticky=tk.W)

        from_label = ttk.Label(frame, text='From:', font=('Arial', 10))
        from_label.grid(row=2, column=2, sticky=tk.E)

        from_option = StringVar()
        from_option_entry = ttk.OptionMenu(frame,from_option,*accts)
        from_option_entry.grid(row=2, column=3, sticky=tk.W)

        to_label = ttk.Label(frame, text='To:', font=('Arial', 10))
        to_label.grid(row=3, column=2, sticky=tk.E)

        to_option = tk.StringVar()
        to_option_entry = ttk.OptionMenu(frame, to_option, *accts)
        to_option_entry.grid(row=3, column=3, sticky=tk.W)

        transfer_button = ttk.Button(frame, text= 'Transfer', command=transfer)
        transfer_button.grid(row=4, column=2, sticky=tk.W)

        cancel_button = ttk.Button(frame, text= 'CANCEL', command=self.destroy)
        cancel_button.grid(row=4, column=3, sticky=tk.W)

        for child in frame.winfo_children():
            child.grid_configure(padx=12, pady=12)

@dataclass
class ChangeLoginDetails(tk.Tk):
    def __init__(self,OnlineBankingAcct):
        tk.Tk.__init__(self)
        self.title('Change Login Details')
        self.resizable(False, False)
        self.geometry('400x250')
        frame = ttk.Frame(self,padding='10 10 10 10')
        frame.pack(expand = True, fill=tk.BOTH)

        def cancel():
            self.destroy()
            acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
        def confirm():
            if current_password.get() == '' or new_password.get() == '' or confirm_new_password.get() == '':
                c=2
                for i in range(3):
                    email_required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                    email_required.grid(row=c, column=4, sticky=tk.E)
                    c+=1
            else:
                if current_password.get() == br.decrypt(OnlineBankingAcct.password.encode('utf-8')):

                    check_pswd = br.checkpassword(new_password.get())
                    if check_pswd == True:
                        if new_password.get() == confirm_new_password.get():
                            change =wdb.changePassword(confirm_new_password.get(),OnlineBankingAcct.ID)
                            if change == True:
                                time.sleep(1)
                                messagebox.showinfo(title='Success', message='Password changed successfully')
                                self.destroy()
                                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
                            else:
                                messagebox.showinfo(title='Error', message='Something went wrong')
                        else:
                            messagebox.showwarning(title='Warning', message='Passwords do not match')
                    else:
                        messagebox.showinfo(title='Warning', message='Password must contain at least \n8 characters\n 1 upper case and 1 number')
                else:
                    messagebox.showerror('Error', 'Incorrect Password')


        email_label = ttk.Label(frame, text='Email:', font=('Arial', 10))
        email_label.grid(row=1, column=2, sticky=tk.E)

        email_value = ttk.Label(frame, text=OnlineBankingAcct.email.upper(), font=('Arial', 8))
        email_value.grid(row=1, column=3,columnspan= 2, sticky=tk.W)

        current_password_label = ttk.Label(frame, text='Current Password:', font=('Arial', 10))
        current_password_label.grid(row=2, column=2, sticky=tk.E)

        current_password = tk.StringVar()
        current_password_entry = ttk.Entry(frame,show='*', textvariable=current_password)
        current_password_entry.grid(row=2, column=3, sticky=tk.W)

        new_password_label = ttk.Label(frame, text='New Password:', font=('Arial', 10))
        new_password_label.grid(row=3, column=2, sticky=tk.E)

        new_password = tk.StringVar()
        new_password_entry = ttk.Entry(frame,show='*', textvariable=new_password)
        new_password_entry.grid(row=3, column=3, sticky=tk.W)

        confirm_new_password_label = ttk.Label(frame, text='Confirm New Password:', font=('Arial', 10))
        confirm_new_password_label.grid(row=4, column=2, sticky=tk.E)

        confirm_new_password = tk.StringVar()
        confirm_new_password_entry = ttk.Entry(frame, show='*', textvariable=confirm_new_password)
        confirm_new_password_entry.grid(row=4, column=3, sticky=tk.W)

        confirm_button = ttk.Button(frame, text= 'CONFIRM', command=confirm)
        confirm_button.grid(row=5, column=2, sticky=tk.E)

        cancel_button = ttk.Button(frame, text= 'CANCEL', command=cancel)
        cancel_button.grid(row=5, column=3, sticky=tk.W)

        for child in frame.winfo_children():
            child.grid_configure(padx=12, pady=12)


@dataclass
class TransactionHistory(tk.Tk):
    def __init__(self,AccountsID):
        tk.Tk.__init__(self)
        self.title('Accounts Transaction History')
        self.geometry('950x500')
        container = ttk.Frame(self,padding='10 10 10 10',width=900,height=600)
        container.pack(fill='both',expand=True)
        frame = A.ScrollableFrame(container)
        frame.pack(expand = True, fill=tk.BOTH)

        Accts_Trns_History = E.TransactionHistory(AccountsID).history.values()

        TransID_label = ttk.Label(frame.scroll, text='ID', font=('Arial', 10, 'bold'))
        TransID_label.grid(row=1, column=0)

        type_label = ttk.Label(frame.scroll, text='Type', font=('Arial', 10,'bold'))
        type_label.grid(row=1, column=1)

        from_label = ttk.Label(frame.scroll, text='From', font=('Arial', 10,'bold'))
        from_label.grid(row=1, column=2)

        amount_label = ttk.Label(frame.scroll, text='Amount', font=('Arial', 10,'bold'))
        amount_label.grid(row=1, column=3)

        to_label = ttk.Label(frame.scroll, text='To', font=('Arial', 10,'bold'))
        to_label.grid(row=1, column=4)

        to_bank = ttk.Label(frame.scroll, text='To Bank', font=('Arial', 10,'bold'))
        to_bank.grid(row=1, column=5)

        to_accountNo_label = ttk.Label(frame.scroll, text='To Account', font=('Arial', 10,'bold'))
        to_accountNo_label.grid(row=1, column=6)

        date_label = ttk.Label(frame.scroll, text='Date', font=('Arial', 10,'bold'))
        date_label.grid(row=1, column=7)

        status_label = ttk.Label(frame.scroll, text='Status', font=('Arial', 10,'bold'))
        status_label.grid(row=1, column=8)



        row = 2
        if len(Accts_Trns_History) == 0:
            no_transactions_label = ttk.Label(frame.scroll, text='No Transactions', font=('Arial', 10))
            no_transactions_label.grid(row=row, column=0,sticky=tk.NSEW)
        else:
            for trans in Accts_Trns_History:
                trnscid = ttk.Label(frame.scroll, text=trans.transactionID, font=('Arial', 10))
                trnscid.grid(row=row, column=0,padx=5,pady=5)

                trnsctype = ttk.Label(frame.scroll, text=trans.type, font=('Arial', 10))
                trnsctype.grid(row=row, column=1,padx=5,pady=5)

                trnscFrom = ttk.Label(frame.scroll, text=trans.From, font=('Arial', 10))
                trnscFrom.grid(row=row, column=2,padx=5,pady=5)

                trnscAmt = ttk.Label(frame.scroll, text=trans.amount, font=('Arial', 10))
                trnscAmt.grid(row=row, column=3,padx=5,pady=5)

                trnscTo = ttk.Label(frame.scroll, text=trans.to, font=('Arial', 10))
                trnscTo.grid(row=row, column=4,padx=5,pady=5)

                trnscToBank = ttk.Label(frame.scroll, text=trans.toBankName, font=('Arial', 10))
                trnscToBank.grid(row=row, column=5,padx=5,pady=5)

                toAccountNo = ttk.Label(frame.scroll, text=trans.toAccountNumber, font=('Arial', 10))
                toAccountNo.grid(row=row, column=6,padx=5,pady=5)

                trnscDate = ttk.Label(frame.scroll, text=trans.date, font=('Arial', 10))
                trnscDate.grid(row=row, column=7,padx=5,pady=5)

                trnscStatus = ttk.Label(frame.scroll, text=trans.status, font=('Arial', 10))
                trnscStatus.grid(row=row, column=8,padx=5,pady=5)

                row +=1




        for child in frame.winfo_children():
            child.grid_configure(padx=20, pady=20)

@dataclass
class CreateAccount(tk.Tk):
    def __init__(self,OnlineBankingAcct):
        tk.Tk.__init__(self)
        self.title('Create Account')
        self.resizable(False, False)
        self.geometry('350x300')
        frame = ttk.Frame(self,padding='10 10 10 10')
        frame.pack(expand = True, fill=tk.BOTH)

        def createSavings():

            savingscreated=wdb.createSavingsAccount(OnlineBankingAcct.accountsID)
            if savingscreated == True:
                time.sleep(2)
                messagebox.showinfo('Success', 'Account Created')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            elif savingscreated == False:
                messagebox.showinfo('Failed', 'Account Exists')
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            else:
                messagebox.showinfo('Error', 'Account Not Created')
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()

        def createInvestment():
            investment_created = wdb.createInvestmentAccount(OnlineBankingAcct.accountsID)
            if investment_created == True:
                time.sleep(2)
                messagebox.showinfo('Success', 'Account Created')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            elif investment_created == False:
                messagebox.showinfo('Failed', 'Account Exists')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            else:
                messagebox.showinfo('Error', 'Account Not Created')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()


        intro_label = ttk.Label(frame, text='Want to start saving or investing with us?', font=('Arial', 12))
        intro_label.grid(row=1, column=1)

        choice_question = ttk.Label(frame, text='Select Account to Create: ', font=('Arial', 10,'bold'), foreground='red')
        choice_question.grid(row=2, column=1)

        savings_button = ttk.Button(frame, text='OPEN SAVINGS ACCOUNT', command=createSavings)
        savings_button.grid(row=3, column=1)

        investment_button = ttk.Button(frame, text= 'OPEN INVESTMENT ACCOUNT', command=createInvestment)
        investment_button.grid(row=4, column=1)

        back = ttk.Button(frame, text='BACK', command=self.destroy)
        back.grid(row=5, column=1)


        for child in frame.winfo_children():
            child.grid_configure(padx=12, pady=12)

@dataclass
class CloseAccount(tk.Tk):
    def __init__(self,CUSTOMER,OnlineBankingAcct):
        tk.Tk.__init__(self)
        self.title('Close Account')
        self.resizable(False, False)
        self.geometry('200x300')
        frame = ttk.Frame(self,padding='10 10 10 10')
        frame.pack(expand = True, fill=tk.BOTH)

        def closeSavings():
            savings_closed = wdb.closeSavingsAccount(OnlineBankingAcct.accountsID)
            if savings_closed == True:
                time.sleep(2)
                messagebox.showinfo('Success', 'Account Closed')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            elif savings_closed == False:
                messagebox.showinfo('Failed', 'Balance Not 0 \n Please transfer money out before closing.')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            else:
                messagebox.showerror('Error', 'Account does not exist or \n something went wrong')
                messagebox.showinfo('Error','Note that an account will not be deleted \n if a transaction has been done with that account \n for security reasons \n Please contact us.')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()


        def closeInvestment():
            investment_closed = wdb.closeInvestmentAccount(OnlineBankingAcct.accountsID)
            if investment_closed == True:
                time.sleep(2)
                messagebox.showinfo('Success', 'Account Closed')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            elif investment_closed == False:
                messagebox.showinfo('Failed', 'Balance Not 0 \n Please transfer money out before closing.')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()
            else:
                messagebox.showerror('Error', 'Account does not exist or \n something went wrong')
                messagebox.showinfo('Error', 'Note that an account will not be deleted \n if a transaction has been done with that account \n for security reasons \n Please contact us.')
                self.destroy()
                acct_ov.AccountOverviewMenu(OnlineBankingAcct).mainloop()

        def closeOnlineAcct():
            self.destroy()
            CloseOnlineAccount(CUSTOMER,OnlineBankingAcct).mainloop()


        note_label = ttk.Label(frame, text='Select Account to Close: ', font=('Arial', 10,'bold'))
        note_label.grid(row=1, column=0)

        close_savings_button = ttk.Button(frame,text='Close Savings', command=closeSavings)
        close_savings_button.grid(row=2, column=0)

        close_investment_button = ttk.Button(frame, text='Close Investment Account', command=closeInvestment)
        close_investment_button.grid(row=3, column=0)

        close_online_account = ttk.Button(frame, text='Close Online Account', command=closeOnlineAcct)
        close_online_account.grid(row=4, column=0)

        cancel_button = ttk.Button(frame, text='Cancel', command=self.destroy)
        cancel_button.grid(row=5, column=0)

        for child in frame.winfo_children():
            child.grid_configure(padx=12, pady=12)

@dataclass
class CloseOnlineAccount(tk.Tk):
    def __init__(self,CUSTOMER,OnlineBankingAcct):
        tk.Tk.__init__(self)
        self.title('Close Online Account')
        self.resizable(False, False)
        self.geometry('320x300')
        frame = ttk.Frame(self,padding='10 10 10 10')
        frame.pack(expand = True, fill=tk.BOTH)

        def deleteAcct():
            if LName.get() =='' or pin.get() == '' or password.get() == '' or DateOfBirth.get()=='':
                row = 1
                for i in range(4):
                    required = Label(frame, text='required', font=('arial', '6', 'bold'), fg='red')
                    required.grid(row=row, column=4, sticky=tk.E)
                    row += 1
            else:
                if LName.get().upper() == CUSTOMER.LastName and DateOfBirth.get() == CUSTOMER.DateOfBirth and password.get() == br.decrypt(OnlineBankingAcct.password.encode('utf-8')) and pin.get() == str(br.getpin()):
                    confirm = messagebox.askyesno('Confirm', 'Delete Online Banking Account?')
                    if confirm == True:
                        closed = wdb.closeOnlineBankingAccount(OnlineBankingAcct.ID)
                        if closed == True:
                            messagebox.showinfo('Success', 'Account Closed \n Please restart app to create new account')
                            self.destroy()
                            time.sleep(2)
                            login.Login().mainloop()
                        else:
                            messagebox.showerror('Error', 'Account does not exist or \n something went wrong')
                    else:
                        messagebox.showinfo('Cancelled', 'Account Not Closed')
                        self.destroy()
                else:
                    messagebox.showinfo('Failed', 'Last Name, Date of Birth, Password or Pin Not Correct')





        LName_label = ttk.Label(frame, text='Last Name:', font=('Arial', 10))
        LName_label.grid(row=1, column=0,sticky=tk.E)

        LName = tk.StringVar()
        LName_entry = ttk.Entry(frame, textvariable=LName)
        LName_entry.grid(row=1, column=1,sticky=tk.W)

        DateOfBirth_label = ttk.Label(frame, text='Date of Birth:', font=('Arial', 10))
        DateOfBirth_label.grid(row=2, column=0,sticky=tk.E)

        DateOfBirth = tk.StringVar()
        DateOfBirth_entry = ttk.Entry(frame, textvariable=DateOfBirth)
        DateOfBirth_entry.grid(row=2, column=1,sticky=tk.W)

        password_label = ttk.Label(frame, text='Password:', font=('Arial', 10))
        password_label.grid(row=3, column=0,sticky=tk.E)

        password = tk.StringVar()
        password_entry = ttk.Entry(frame,show='*', textvariable=password)
        password_entry.grid(row=3, column=1,sticky=tk.W)

        pin_label = ttk.Label(frame, text='PIN:', font=('Arial', 10))
        pin_label.grid(row=4, column=0,sticky=tk.E)

        pin = tk.StringVar()
        pin_entry = ttk.Entry(frame, show='*', textvariable=pin)
        pin_entry.grid(row=4, column=1,sticky=tk.W)

        delete_button = ttk.Button(frame, text='Delete', command=deleteAcct)
        delete_button.grid(row=5, column=0)

        cancel_button = ttk.Button(frame, text='Cancel', command=self.destroy)
        cancel_button.grid(row=5, column=1)

        for child in frame.winfo_children():
            child.grid_configure(padx=12, pady=12)

# profile = ProfileDetails(CUSTOMER).mainloop()
# ChangeLoginDetails(None).mainloop()
# TransactionHistory(25887740).mainloop()
# CreateAccount(2558).mainloop()
# CloseOnlineAccount('','3').mainloop()

# CloseOnlineAccount('s','s ').mainloop()