import sys
sys.path.append("UIs")
sys.path.append("../encryp/psd.encryp.locked")
sys.path.append('APIs')
import login_create_account as Bank_App

def main():

    BankApp = Bank_App.Login()
    BankApp.mainloop()

if __name__ == '__main__':
    main()

