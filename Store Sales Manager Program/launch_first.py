# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 22:38:29 2023

@author: Chidera
"""

import software_functions as sf
import manager as mg
import sales_program

def title():
    print()
    print()
    print('***********STORE  SALES  MANAGER  PROGRAM***********')
    print()
    print("To login as Admin enter 'admin' as username and password." +
          '\nElse enter your staff login details...')
    print()

def main():
    
    '''A login access to login as an admin and have manager tools or just login directly as a worker,
        only if a workers details has been added by the admin using the manager tools. Once a worker is able to
        login he/she gets access to the sales program to process transactions'''
    
    while True:
        title()
        
        print('+'*50)
        print()
        username = input("Username ('exit to end program'):  ").upper()
        if username.lower() == 'exit':
            break
        else:
            print()
            if len(username)>= 4:
                if username.lower() == 'admin':
                    password = input('Password:  ')
                    if password.lower() == username.lower() :
                        mg.main()
                        
                    else:
                        print('Wrong admin password')
                else:
                    check = sf.checkUsername(username)
                    if check == True:
                        while True:
                            print()
                            password = input('Password:  ')
                            print()
                            login = input('Login ? (y/n):  ').lower()
                            if login == 'y':
                                check = sf.checkPassword(password)
                                if check == True:
                                    validate = sf.validatePassword(username, password)
                                    if validate == True:
                                        sales_program.main()
                                        break
                                    else:
                                        print('Wrong username or password. Please try again!')
                                        continue
                                else:
                                    continue
                            else:
                                break
                    else:
                        continue
            else:
                print('Username must be atleast 4 characters!')

if __name__ == '__main__':
    main()
                        