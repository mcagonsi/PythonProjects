
import sys
sys.path.append("../")
sys.path.append("../encryp/psd.encryp.locked")
from objs import actors as A
from objs import entity as E
import mysql.connector as db

con = db.connect(host='localhost', user='root', passwd='root', port=3306, database='scotiadb')
c = con.cursor()
DATE_FORMAT = '%m/%d/%Y'

def searchOnlineAccount(email):
    c.fetchall()
    searchOnlineBankingAcct = 'SElECT * from `OnlineBankingAcct` where `Email` = %s'
    c.execute(searchOnlineBankingAcct, (email,))

    onlineAccount = c.fetchone()

    if onlineAccount is not None:
        return E.OnlineBankingAccount(onlineAccount[0], onlineAccount[1], onlineAccount[2], onlineAccount[3], onlineAccount[4])

    else:
        return None


def validateFinancialAccountandCheckOnlineAcct(chequing_no,lName,DOB):

    try:

        validateFinancialAccount = 'SELECT `ID`, `accounts_id` from `Customer_Accounts_Account` where `AccountNumber` = %s and `LastName` = %s '
        c.execute(validateFinancialAccount, (chequing_no, lName))
        custinfo = c.fetchone()

        if custinfo is not None:
            custID = custinfo[0]
            accountsID = custinfo[1]
            c.fetchall()
            searchCustomerInfo = 'SELECT `FirstName` from `Customer` where `ID` = %s and `DOB` = %s;'
            c.execute(searchCustomerInfo, (custID,DOB))
            firstName = c.fetchone()[0]

            return custID, firstName, accountsID
        else:
            return None
    except Exception :
        return None
def checkOnlineAccountExists(custID):

    c.fetchall()
    checkingOnlineAcctExists = 'SELECT `ID` from `OnlineBankingAcct` where `customerID` = %s;'
    c.execute(checkingOnlineAcctExists, (custID,))
    OnlineID = c.fetchone()
    if OnlineID is not None:
        return True
    else:
        return False

def getCustomerInfo(custID):

    getcustomer = 'select * from `Customer` where `ID` = %s'
    c.execute(getcustomer, (custID,))
    cust = c.fetchone()
    customer = A.Customer(cust[1], cust[2], cust[3], cust[4].isoformat(), cust[5], cust[6], cust[7], cust[8], cust[9], cust[10], cust[11], cust[12], cust[0])
    return customer
def getTransactionHistory(accountsID):
    getTransHistory = 'select * from `Transaction` where `accountID` = %s order by `ID` desc'
    c.execute(getTransHistory, (accountsID,))
    transHistory = c.fetchall()

    TranscHistoryList = []
    if transHistory is not None:
        for trns in transHistory:
            Trnsc = E.Transaction(trns[0], trns[1], trns[2], trns[3], trns[4],trns[5], trns[6], trns[7], trns[8], trns[9], trns[10], trns[11])
            TranscHistoryList.append(Trnsc)
        return TranscHistoryList
    else:
        return None

def getBankAccounts():
    CON = db.connect(host='localhost', user='root', passwd='root', port=3306, database='scotiadb')
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
def getBankCustomers():
    CON = db.connect(host='localhost', user='root', passwd='root', port=3306, database='scotiadb')
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

def getBankAccountsIDs():
    CON = db.connect(host='localhost', user='root', passwd='root', port=3306, database='scotiadb')
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





def main():
    pass
if __name__ == '__main__':
    main()