from cryptography.fernet import Fernet

key = Fernet.generate_key()

cipher = Fernet(key)

pswd = 'Chidexstar1233'

encryptedData = cipher.encrypt(pswd.encode())

cipherDecrypt = Fernet(key)

decrypted = cipherDecrypt.decrypt(encryptedData).decode('utf-8')

Password = 'Chidexstar1233'

if decrypted == Password:
    print('Yes')
else:
    print('No')

