import sys
sys.path.append('../')
from dataclasses import dataclass
from objs import entity as E
import mysql.connector as db
from objs import actors as A



@dataclass
class API:
    _name = None
    _status = None
    _headers = None
    _body = None
    _endpoint = None

    def __post_init__(self):
        self._name = E.Bank('ROYAL BANK OF CANADA','2 Skywalket Avenue', 'Oacis', 'Marsian City', 'Mars','184 3DE').bankName
        self._headers = (getBankCustomers(),getBankAccountsIDs())
        self._body = getBankAccounts()
        self._endpoint = db.connect(host='localhost', user='root', passwd='root', port=3306, database='rbcdb')
    @property
    def name(self):
        return self._name
    @property
    def headers(self):
        return self._headers
    @property
    def body(self):
        return self._body


    @property
    def status(self):
        return self._status
    def get(self,accountNumber):
        customers, accountIDs = self._headers
        accounts = self._body
        bank_name = self._name

        account, customer = validateAccountNumber(customers,accountIDs,accounts,accountNumber)

        if account != None and customer != None:
            self._status = 200
            return bank_name,account,customer
        else:
           self._status = 404
    def post(self,Transaction):
        pass
        Recipient = self._body[Transaction.toAccountNumber]
        status = Recipient.creditAccount(self._endpoint, Transaction)
        if status is True:
            self._status = 200
        else:
            self._status = 400

        # a credit alert should always deposit into the checkings account,external client will be gotten from the api.get() return


def validateAccountNumber(customers,accountsIDs,accounts,accountNumber):
    if accountNumber in accounts:
        account = accounts[accountNumber]
        customerid = accountsIDs[account.accountsID]
        customer = customers[customerid]
        return account, customer
    else:
        return None, None
    pass

#connection dependencies for the api
def getBankAccountsIDs():
    CON = db.connect(host='localhost', user='root', passwd='root', port=3306, database='rbcdb')
    C = CON.cursor()
    getBankAccountsIDs = 'select * from `Accounts`;'
    C.execute(getBankAccountsIDs)
    ACCOUNTSIDs = {}
    AccountsIDs = C.fetchall()
    if AccountsIDs is not None:
        for accountsID in AccountsIDs:
            ACCOUNTSIDs[accountsID[0]] = accountsID[1]
        CON.close()
        return ACCOUNTSIDs
    else:
        CON.close()
        return None

def getBankCustomers():
    CON = db.connect(host='localhost', user='root', passwd='root', port=3306, database='rbcdb')
    C = CON.cursor()
    getCustomers = 'select * from `Customer`'
    C.execute(getCustomers)
    CUSTOMERS = {}
    customers = C.fetchall()

    if customers is not None:
        for cust in customers:
           CUSTOMERS[cust[0]] = A.Customer(cust[1], cust[2], cust[3], cust[4].isoformat(), cust[5], cust[6], cust[7], cust[8], cust[9],
                                  cust[10], cust[11], cust[12], cust[0])

        CON.close()
        return CUSTOMERS
    else:
        CON.close()
        return None



def getBankAccounts():
    CON = db.connect(host='localhost', user='root', passwd='root', port=3306, database='rbcdb')
    C = CON.cursor()
    getBankAccounts = 'select * from `Account`;'
    C.execute(getBankAccounts)
    Accounts = {}
    readAccts = C.fetchall()
    if readAccts is not None:
        for account in readAccts:
            if account[3]==1:

                Accounts[account[0]] = E.Account(account[0], account[1], account[2], E.AccountType(account[3]), account[4])

        CON.close()
        return Accounts

    else:
        return None
