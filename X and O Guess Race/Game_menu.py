# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 13:06:12 2023

@author: Chidera
"""

import start_game
import rules
import about

def title():
    print('X and O GUESS   RACE   GAME')
    print('Welcome to Guess Race game by Michael Agonsi')
    print('I hope you do enjoy the game!')

def menu():
    print('MENU    OPTIONS')
    print('1. Start the game!' +
          '\n2. How to play?' +
          '\n3. About game' +
          '\n4. Exit')
def main():
    title()
    menu()
    while True:
        option = int(input('Option: '))
        if option == 1:
            start_game.main()
        elif option == 2:
            rules.rules()
            print()
        elif option == 3:
            about.about()
            print()
        elif option ==4 :
            print()
            print('Thank you for playing!' +
                  '\n\nBye!')
            break
        else:
            print('Please enter a valid option.')
if __name__ == '__main__':
    main()
    