import sys
sys.path.append("../UIs")
sys.path.append("../encryp/psd.encryp.locked")

from cryptography.fernet import Fernet
import pickle


def storekey(key):
    with open('psd.encryp.locked','wb') as k:
        pickle.dump(key,k)

def getkey():
    with open('psd.encryp.locked','rb') as k:
        return pickle.load(k)

def encrypt(pswd):
    secret_key = Fernet.generate_key()

    cipherEncrypt = Fernet(secret_key)

    encrypted_pswd = cipherEncrypt.encrypt(pswd.encode())

    storekey(secret_key)

    return encrypted_pswd

def decrypt(encrypted_pswd):
    key = getkey()

    cipherDecrypt = Fernet(key)

    decrypted_pswd = cipherDecrypt.decrypt(encrypted_pswd).decode('utf-8')

    return decrypted_pswd

def checkpassword(pswd):
    num = 0
    upper = 0
    for char in pswd:
        if char.isupper():
            upper += 1
        elif char.isdigit():
            num += 1

    if len(pswd) > 8 and num > 0 and upper > 0 :
        return True
    else:
        return False


def checkemail(email):

    if '@' in email:
        return True
    else:
        return False
def savepin(pin):
    try:
        with open('pin.encryp.locked','wb') as Pin:
            pickle.dump(pin,Pin)
        return True
    except Exception as e:
        return False
def getpin():
    try:
        with open('pin.encryp.locked','rb') as Pin:
            return pickle.load(Pin)

    except Exception as e:
        return None

# password = encrypt('michael')
# str_password = password.decode('utf-8')
# print(str_password)
# dpassword = str_password.encode('utf-8')
# print(dpassword)