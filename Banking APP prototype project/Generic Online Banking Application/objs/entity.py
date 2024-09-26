from dataclasses import dataclass
from datetime import datetime
import sys
sys.path.append("..")
from DBs import writeDB as wdb
from DBs import readDB as rdb
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
import mysql.connector as db
con = db.connect(host='localhost',user='root',passwd='root',port=3306,database='bankdb')
c = con.cursor()


@dataclass
class Bank:
    _BankName: str
    _Employees=None
    _Customers=dict
    _AccountsIDs=dict
    _Accounts=None
    _Address: str
    _City: str
    _Country: str
    _PostalCode: str
    _Branch:str

    @property
    def bankName(self):
        return self._BankName
    @property
    def customers(self):
        return self._Customers

    @property
    def accounts(self):
        return self._Accounts
    @property
    def accountsids(self):
        return self._AccountsIDs

    def __post_init__(self):
        self._Accounts = rdb.getBankAccounts()
        self._Customers = rdb.getBankCustomers()
        self._AccountsIDs = rdb.getBankAccountsIDs()


    def validateAccountNumber(self,AccountNumber):
        if AccountNumber in self._Accounts:
            account = self._Accounts[AccountNumber]
            customerid = self._AccountsIDs[account.accountsID]
            customer = self._Customers[customerid]
            return account,customer
        else:
            return None,None
        pass


@dataclass
class AccountType:
    _ID:int
    _Name = ''

    @property
    def id(self):
        return self._ID
    @property
    def name(self):
        return self._Name


    def __post_init__(self):

        query = 'select * from `AccountType`;'
        c.execute(query)
        types = c.fetchall()
        for t in types:
            if self._ID == t[0]:
                self._Name = t[1]

@dataclass
class Accounts:
    _ID:int
    _Accounts = {}
    _customerID:int


    def __post_init__(self):
        CON = db.connect(host='localhost', user='root', passwd='root', port=3306, database='bankdb')
        C = CON.cursor()

        getaccounts = 'select * from `Account` where Accounts_ID = %s '
        C.execute(getaccounts, (self._ID,))
        Accounts = C.fetchall()
        for a in Accounts:
            if a[2] ==1:
                self._Accounts[a[0]] = Account(a[0],a[1],a[2],AccountType(a[3]),a[4])
        CON.close()



    def getTotalBalance(self):
        total_balance = 0
        for acct in self._Accounts.values():
            total_balance += acct.balance

        return total_balance

    def showAccounts(self):
        return self._Accounts





@dataclass
class Account:
    _AccountNumber:int
    _Balance: float
    _Active: bool
    _AccountType: AccountType
    _AccountsID: int




    @property
    def accountNumber(self):
        return self._AccountNumber
    @property
    def accountsID(self):
        return self._AccountsID

    @property
    def accountType(self):
        return self._AccountType
    @property
    def balance(self):
        return self._Balance
    @property
    def active(self):
        return self._Active

    def getBalance(self):
        return locale.currency(self._Balance,grouping=True)

    def creditAccount(self,Trns):
        creditAccount ="insert into `Transaction`(ID,type,amount,FromBankName,FromName,FromAccountNumber,ToBankName,ToAccountNumber) values (default,'CREDIT',%s,%s,%s,%s,%s,%s);"
        c.execute(creditAccount,(Trns.amount,Trns.fromBankName,Trns.From,Trns.fromAccountNumber,Trns.toBankName,Trns.toAccountNumber))
        con.commit()

        return True

    def debitAccount(self,Trns):
        debitAccount = "insert into `Transaction`(ID,type,amount,FromBankName,FromAccountNumber,ToBankName,ToName,ToAccountNumber) values (default,'DEBIT',%s,%s,%s,%s,%s,%s);"
        c.execute(debitAccount,(Trns.amount,Trns.fromBankName,Trns.fromAccountNumber,Trns.toBankName,Trns.to,Trns.toAccountNumber))
        con.commit()

        return True

    def showTransactionHistory(self):
        rdb.getTransactionHistory(self)



@dataclass
class Transaction:
    _transactionID :int
    _AccountID : int
    _type :str
    _Amount :float
    _Date :datetime
    _FromBankName:str
    _From :str
    _FromAccountNumber:int
    _ToBankName: str
    _To:str
    _ToAccountNumber:int
    _status : str

    # based on the account number

    @property
    def transactionID(self):
        return self._transactionID
    @property
    def type(self):
        return self._type

    @property
    def amount(self):
        return self._Amount

    @property
    def date(self):
        return self._Date
    @property
    def status(self):
        return self._status
    @property
    def accountID(self):
        return self._AccountID

    @property
    def fromBankName(self):
        return self._FromBankName

    @property
    def From(self):
        return self._From

    @property
    def fromAccountNumber(self):
        return self._FromAccountNumber

    @property
    def toBankName(self):
        return self._ToBankName

    @property
    def to(self):
        return self._To

    @property
    def toAccountNumber(self):
        return self._ToAccountNumber

@dataclass
class TransactionHistory:
    _accountsID:int
    _history = {}

    def __post_init__(self):
        c.fetchall()
        trnsHistory = rdb.getTransactionHistory(self._accountsID)
        if trnsHistory is not None:
            for t in trnsHistory:
                self._history[t.transactionID] = t
        else:
            pass

    @property
    def accountsID(self):
        return self._accountsID

    @property
    def history(self):
        return self._history







@dataclass
class OnlineBankingAccount:
    _ID:int
    _email:str
    _password:str
    _CustomerID:int
    _AccountsID:int

    def createOnlineBankingAccount(self):
        return wdb.createOnlineBankingAcct(self)
    def changeLoginDetails(self):
        return wdb.changeLoginDetails(self)


    @property
    def ID(self):
        return self._ID
    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def customerID(self):
        return self._CustomerID
    @property
    def accountsID(self):
        return self._AccountsID



def main():

    pass







if __name__ == '__main__':
    main()