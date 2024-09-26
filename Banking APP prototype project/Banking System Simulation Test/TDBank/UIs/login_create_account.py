import sys

sys.path.append("../")
sys.path.append("../DBs")
sys.path.append("../funcs")
sys.path.append("../encryp/psd.encryp.locked")
from funcs import biz_rules as br
import time
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import *
from DBs import readDB as rdb
from DBs import writeDB as wdb
from dataclasses import dataclass
import account_overview

from objs import actors as A
from objs import entity as E
import mysql.connector as db



CUSTOMER_ID = None
ACCOUNTS_ID = None


@dataclass
class Login(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Login')
        self.geometry('500x300')
        frame = ttk.Frame(self, padding='10 10 10 10')
        frame.pack(fill=tk.BOTH, expand=True)

        def login():
            if email.get() == '' or password.get() == '':
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=3, column=5, sticky=tk.E)
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=4, column=5, sticky=tk.E)
            else:
                if br.checkemail(email.get()) is False:
                    required = Label(frame, text='invalid email', font=('arial', '5', 'bold'), fg='red')
                    required.grid(row=3, column=5, sticky=tk.E)

                else:
                    onlineaccount = rdb.searchOnlineAccount(email.get())


                    if onlineaccount is not None:
                        try:

                            db_pswd = br.decrypt(onlineaccount.password.encode('utf-8'))
                            if (db_pswd == password.get()):
                                self.destroy()
                                time.sleep(2)
                                Accountoverview = account_overview.AccountOverviewMenu(onlineaccount)
                                Accountoverview.mainloop()
                            else:
                                messagebox.showinfo('Error', 'Email or Password Incorrect')
                        except Exception:
                            messagebox.showinfo('Error', 'Something went wrong \n Restart application')
                    else:
                        messagebox.showinfo('Error', 'Account Does Not Exist')

        def create_account():
            self.destroy()
            validate = ValidateAccount()
            validate.mainloop()

        # LOGO LABEL
        logo = Label(frame, text='TD BANK', width=35, font=('Arial', 14), )
        logo.grid(row=0, column=1, columnspan=5, sticky='ew')

        # EMAIL LABEL
        email_label = ttk.Label(frame, text='Email: ')
        email_label.grid(row=3, column=1, sticky=tk.E)

        # EMAIL INPUT ENTRY FIELD
        email = tk.StringVar()
        email_entry = ttk.Entry(frame, textvariable=email, width=40)
        email_entry.grid(row=3, column=2, columnspan=2, sticky=tk.W)

        # PASSWORD LABEL
        password_label = ttk.Label(frame, text='Password: ')
        password_label.grid(row=4, column=1, sticky=tk.E)

        # PASSWORD INPUT ENTRY FIELD
        password = tk.StringVar()
        password_entry = ttk.Entry(frame,show='*', textvariable=password, width=40)
        password_entry.grid(row=4, column=2, columnspan=2, sticky=tk.W)

        # CREATE ACCOUNT LINK
        create_account_button = ttk.Button(frame, text='Create Account', command=create_account, width=5)
        create_account_button.grid(row=5, column=2, columnspan=2, sticky=tk.NSEW)

        # LOGIN BUTTON
        login_button = ttk.Button(frame, text='Login', command=login, width=10)
        login_button.grid(row=6, column=2, sticky=tk.W)

        # EXIT BUTTON
        exit_button = ttk.Button(frame, text='Exit', command=exit, width=10)
        exit_button.grid(row=6, column=3, sticky=tk.E)

        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=10)


@dataclass
class CreateAccount(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Create Online Banking Account')
        self.geometry('500x300')
        frame = ttk.Frame(self, padding='10 10 10 10')
        frame.pack(fill=tk.BOTH, expand=True)

        def create_account():
            global CUSTOMER_ID
            Email = email.get().title()
            Password = password.get()
            CPassword = cpassword.get()
            if Email == '' or CPassword == '' or Password == '':
                email_required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                email_required.grid(row=2, column=4, sticky=tk.E)
                pswd_required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                pswd_required.grid(row=3, column=4, sticky=tk.E)
                cpswd_required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                cpswd_required.grid(row=4, column=4, sticky=tk.E)

                # email_required.destroy()
                # pswd_required.destroy()
                # cpswd_required.destroy()

            else:
                if br.checkemail(Email) == False:
                    required = Label(frame, text='Invalid email', font=('arial', '6', 'bold'), fg='red')
                    required.grid(row=2, column=4, sticky=tk.E)
                else:
                    if br.checkpassword(Password) is False:
                        required = Label(frame,
                                         text='Password must \n - contain atleast one upper\n and one number\n - be more than 8 characters ',
                                         font=('arial', '7', 'bold'), fg='red')
                        required.grid(row=6, column=2, columnspan=2, sticky=tk.W)
                    else:
                        if Password != CPassword:
                            required = Label(frame, text='Passwords must be the same', font=('arial', '6', 'bold'),
                                             fg='red')
                            required.grid(row=4, column=4, sticky=tk.E)
                        else:
                            encrypted_password = br.encrypt(Password)

                            onlinebankingaccount = E.OnlineBankingAccount(0, Email,  encrypted_password.decode('utf-8'), CUSTOMER_ID, ACCOUNTS_ID)
                            create = onlinebankingaccount.createOnlineBankingAccount() #wdb.createOnlineBankingAcct(onlinebankingaccount)
                            if create is True:
                                time.sleep(2)
                                messagebox.showinfo('Success', 'Online Banking Account Created')

                                self.destroy()
                                login = Login()
                                login.mainloop()
                            else:
                                messagebox.showwarning(title='Error', message='Something went wrong')

        # FOR EMAIL FIELD
        email_label = ttk.Label(frame, text='Email: ')
        email_label.grid(row=2, column=1, sticky=tk.E)

        email = tk.StringVar()
        email_entry = ttk.Entry(frame, textvariable=email, width=35)
        email_entry.grid(row=2, column=2, columnspan=2, sticky=tk.W)

        # FOR PASSWORD FIELD
        password_label = ttk.Label(frame, text='Password: ')
        password_label.grid(row=3, column=1, sticky=tk.E)

        password = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password,show='*' ,width=35)
        password_entry.grid(row=3, column=2, columnspan=2, sticky=tk.W)

        cpassword = ttk.Label(frame, text='Confirm Password: ')
        cpassword.grid(row=4, column=1, sticky=tk.E)

        cpassword = tk.StringVar()
        cpassword_entry = ttk.Entry(frame, textvariable=cpassword,show='*', width=35)
        cpassword_entry.grid(row=4, column=2, columnspan=2, sticky=tk.W)

        # CREATING THE ACCOUNT
        create_account_button = ttk.Button(frame, text='Create Account', command=create_account)
        create_account_button.grid(row=5, column=2)

        exit_button = ttk.Button(frame, text='Cancel', command=exit)
        exit_button.grid(row=5, column=3)

        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=10)


@dataclass
class ValidateAccount(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Validate Account')
        self.geometry('520x300')
        frame = ttk.Frame(self, padding='10 10 10 10')
        frame.pack(fill=tk.BOTH, expand=True)

        def validate_account():
            if chequing_acct_number.get() == '' or last_name.get() == '' or date_of_birth.get() == '':
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=2, column=3, sticky=tk.W)
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=3, column=3, sticky=tk.W)
                required = Label(frame, text='required', font=('arial', '7', 'bold'), fg='red')
                required.grid(row=4, column=3, sticky=tk.W)
            else:

                validate = rdb.validateFinancialAccountandCheckOnlineAcct(chequing_acct_number.get(),
                                                                          last_name.get().upper(), date_of_birth.get())
                if validate is not None:
                    custID, FName, accountsID = validate

                    OnlineID = rdb.checkOnlineAccountExists(custID)
                    if custID != None and FName != None:
                        if FName != None and OnlineID == False:
                            owner.set(f'{FName} {last_name.get().upper()}')
                            global CUSTOMER_ID
                            global ACCOUNTS_ID
                            CUSTOMER_ID = custID
                            ACCOUNTS_ID = accountsID
                        else:
                            exists_login = messagebox.askyesno('Online Already Account Exists',
                                                               'Can not create a new account. \n Login ?')
                            if exists_login == True:

                                self.destroy()
                                login = Login()
                                login.mainloop()
                            else:
                                self.destroy()
                    else:
                        messagebox.showwarning('Warning', 'Account Not Found')
                else:
                    retry = messagebox.askretrycancel('Invalid Inputs',
                                                      'Something wrong with your entries or \n Account not found')
                    if retry == True:
                        pass
                    else:
                        self.destroy()

        def continueToCreateAccount():
            if owner.get() == None or owner.get() != '':
                self.destroy()
                createAccount = CreateAccount()
                createAccount.mainloop()
            else:
                messagebox.showerror('Error', 'Must Validate Account')

        chequing_acct_number_label = ttk.Label(frame, text='Chequing \nAccount Number: ')
        chequing_acct_number_label.grid(row=2, column=1, sticky=tk.E)

        last_name_label = ttk.Label(frame, text='Lastname: ')
        last_name_label.grid(row=3, column=1, sticky=tk.E)

        date_of_birth_label = ttk.Label(frame, text='Date of Birth (YYYY-MM-DD) : ')
        date_of_birth_label.grid(row=4, column=1, sticky=tk.E)

        chequing_acct_number = tk.StringVar()
        chequing_acct_number_entry = ttk.Entry(frame, textvariable=chequing_acct_number, width=30)
        chequing_acct_number_entry.grid(row=2, column=2, columnspan=2, sticky=tk.W)

        last_name = tk.StringVar()
        last_name_entry = ttk.Entry(frame, textvariable=last_name, width=30)
        last_name_entry.grid(row=3, column=2, columnspan=2, sticky=tk.W)

        date_of_birth = tk.StringVar()
        date_of_birth_entry = ttk.Entry(frame, textvariable=date_of_birth, width=30)
        date_of_birth_entry.grid(row=4, column=2, columnspan=2, sticky=tk.W)

        owner_label = ttk.Label(frame, text='Owner: ')
        owner_label.grid(row=5, column=1, sticky=tk.E)

        owner = tk.StringVar()
        owner_entry = ttk.Entry(frame, textvariable=owner, state='readonly', width=30)
        owner_entry.grid(row=5, column=2, sticky=tk.W)

        validate_account_button = ttk.Button(frame, text='Validate Account', command=validate_account)
        validate_account_button.grid(row=5, column=3, sticky=tk.E)

        continue_button = ttk.Button(frame, text='Continue', width=40, command=continueToCreateAccount)
        continue_button.grid(row=6, column=2, columnspan=2, sticky=tk.W)

        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=10)



