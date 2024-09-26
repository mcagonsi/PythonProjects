import sys
sys.path.append("../")
sys.path.append("../funcs")
from objs import actors as A, entity as E
import mysql.connector as db
from funcs import biz_rules as br
con = db.connect(host='10.0.0.55', user='dera', passwd='', port=3306, database='scotiadb')
c = con.cursor()

def createOnlineBankingAcct(online_acct):

    try:

        create_online_account = 'INSERT INTO `OnlineBankingAcct` (`ID`,`Email`,`Password`,`customerID`,`AccountsID`) VALUES (DEFAULT,%s,%s,%s,%s)'
        c.execute(create_online_account,(online_acct.email, online_acct.password, online_acct.customerID, online_acct.accountsID))
        con.commit()
        c.fetchall()
        con.close()
        return True
        print('Online Banking Account Created')
    except Exception  as e:
        print(e)
        return False

def updatePhoneNumber(phone_number,customerID):
    try:
        updatePhone = 'UPDATE `Customer` SET `PhoneNumber`=%s WHERE `ID`=%s'
        c.execute(updatePhone,(phone_number,customerID))
        con.commit()
        return True
    except Exception as e:
        return False

def changePassword(password,OnlineBankingID):
    new_pswd = br.encrypt(password)
    try:

        changePassword = 'update `OnlineBankingAcct` set `Password`=%s where `ID`=%s'
        c.execute(changePassword,(new_pswd.decode('utf-8'),OnlineBankingID))
        con.commit()
        return True
    except Exception as e:
        return False
def createSavingsAccount(AccountsID):
    try:
        checkSavings = 'Select * from `Account` where `Accounts_ID`=%s and `AccountType_ID`=%s'
        c.execute(checkSavings,(AccountsID,2))
        exists = c.fetchall()
        if len(exists) ==0:

            createSavings = 'INSERT INTO `Account` VALUES (default,0, 1,2,%s)'
            c.execute(createSavings,(AccountsID,))
            con.commit()

            return True
        else:

            return False
    except Exception as e:

        return None
def createInvestmentAccount(AccountsID):
    try:
        checkInvestment = 'Select * from `Account` where `Accounts_ID`=%s and `AccountType_ID`=%s'
        c.execute(checkInvestment,(AccountsID,3))
        exists = c.fetchall()
        if len(exists) ==0:

            createSavings = 'INSERT INTO `Account` VALUES (default,0, 1,3,%s)'
            c.execute(createSavings,(AccountsID,))
            con.commit()

            return True
        else:

            return False
    except Exception as e:

        return None
def closeSavingsAccount(AccountsID):
        try:
            checkSavings = 'Select `AccountNumber`,`Balance` from `Account` where `Accounts_ID`=%s and `AccountType_ID`=%s'
            c.execute(checkSavings,(AccountsID,2))
            Acct = c.fetchall()[0]

            if Acct is not None:
                if Acct[1] == 0:
                    closeSavings = 'DELETE FROM `Account` where `AccountNumber`=%s'
                    c.execute(closeSavings,(Acct[0],))
                    con.commit()

                    return True
                elif Acct[1] > 0:
                    return False
            else:
                return None
        except Exception as e:
            return None


def closeInvestmentAccount(AccountsID):

    try:
        checkInvestment = 'Select `AccountNumber`,`Balance` from `Account` where `Accounts_ID`=%s and `AccountType_ID`=%s'
        c.execute(checkInvestment, (AccountsID, 3))
        Acct = c.fetchall()[0]

        if Acct is not None:
            if int(Acct[1]) == 0:

                closeSavings = 'DELETE FROM `Account` where `AccountNumber`=%s'
                c.execute(closeSavings, (Acct[0],))
                con.commit()
                return True
            elif Acct[1] > 0:
                return False
        else:

            return None
    except Exception as e:

        return None

def closeOnlineBankingAccount(OnlineBankingID):
    try:
        closeOnlineAcct = 'DELETE FROM `OnlineBankingAcct` where `ID`=%s'
        c.execute(closeOnlineAcct, (OnlineBankingID,))
        con.commit()
        c.fetchall()
        con.close()
        return True
    except Exception as e:
        return False

def recordTransferTransaction(AccountsID,amount,fromAccount,toAccount):
    try:
        recordTransfer = "insert into `Transaction`(`ID`,`type`,`amount`,`FromAccountNumber`,`ToAccountNumber`,`Status`,`accountID`) values (default,'TRANSFER', %s ,%s,%s,Status,%s)"
        recordDTransfer = "insert into `Transaction`(`ID`,`type`,`amount`,`FromAccountNumber`,`ToAccountNumber`,`Status`,`accountID`) values (default,'T_DEPOSIT', %s ,%s,%s,Status,%s)";

        c.execute(recordTransfer,(amount,fromAccount.accountNumber,toAccount.accountNumber,AccountsID))
        c.fetchall()
        c.execute(recordDTransfer,(amount,fromAccount.accountNumber,toAccount.accountNumber,AccountsID))
        con.commit()
        return True
    except Exception as e:
        return False


def main():
    pass

if __name__ == '__main__':
    main()