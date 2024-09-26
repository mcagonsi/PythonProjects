# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 06:54:40 2023

@author: Chidera
"""

import temp_calculator_structure as TCS

def main():
    TCS.title()
    loop = 'y'
    while loop.lower() == 'y':
        option = TCS.menu_input()
        if option == 1 :
            TCS.FahToCel()
            
        elif option == 2:
            TCS.CelToFah()
            
        elif option == 3:
            TCS.FahToKel()
            
        elif option == 4:
            TCS.KelToFah()
            
        elif option == 5:
            TCS.KelToCel()
            
        elif option == 6:
            TCS.CelToKel()
            
        else:
            print('Please Enter a valid option from above')
            continue
        loop = input("Convert another temperature? (y/n):\t")
    
    print("\nBye!")
    
if __name__ == '__main__':
        main()
    