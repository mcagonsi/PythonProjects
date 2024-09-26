# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 02:30:06 2023

@author: Chidera
"""
import random


def title (): #introduces the game
    print('CAST THE DIE GAME')
    print('='*50)
    print('\nThis is a game that involves two(2) players.')
    print('\nThe rules of the game:' +
          '\n1. You are given a pair of dice to roll' + 
          '\n2. First player to get the same number in each die\n\twins the game')
    print('='*50,'\n')
def roll_die1() -> int: #rolls the die1
    '''
    

    Returns
    -------
    int
        DESCRIPTION.

    '''
    die1 = random.randint(1,6)
    return die1

def roll_die2() -> int: #rolls the die2
    '''
    

    Returns
    -------
    int
        DESCRIPTION.

    '''
    die2 = random.randint(1,6)
    return die2

def main(): #plays the game
    title()
    play = input('Start the game? (y/n):\t')
    while play.lower() == 'y': #starts the game
        
        next_player = input('Type \'R\' to roll the dice:\t') #takes response to roll the die and start a loop
        while next_player.lower() =='r':
            die_1 = roll_die1()
            die_2 = roll_die2()
            if die_1 == die_2: # checks for a win
                print()
                print('$'*10)
                print('You Win!')
                print('$'*10)
                print()
                break
            else: # chesks for no win
                print('+'*15)
                print("You got {} | {}".format(die_1, die_2))
                print('+'*15)
                print('You did not win. Please pass to the next player')
                print()
                next_player = input('Type \'R\' to roll the dice:\t')
                continue
        print()
        play = input('Play Again? (y/n):\t') #takes input to continue game
        
    #exits the game
    print('\nThanks for playing!'+
          '\n\nBye!')

if __name__ == '__main__':
    main()
        
