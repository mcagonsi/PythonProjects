# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 03:46:38 2023

@author: Chidera
"""
import random

def display_rule():
    print("LET'S PLAY PIG")
    print()
    print('See how many turns it takes you to get exactly 20 points')
    print('Turn ends when you hold or role a 1')
    print('If you roll a 1 you loose all the points for the turn')
    print('if you hold you save all the points for the turn')
    print()

def roll_die():
    die = random.randint(1,6)
    return die

def main():
    display_rule()
    score = 0
    turn = 1
    while True:
        
        print('TURN'+ str(turn))
        option = input('Roll or Hold? (r/h):\t')
        
        if option.lower() == 'r':
            die = roll_die()
            print('Die: {}'.format(die))
            print()
            if die > 1:
                score += die
                turn += 1
                if score >= 20:
                    break
                else:
                    continue
            else:
                print('Turn over. No score.')
                score = 0
                break
        
        elif option.lower() == 'h':
            print('Score for turn: {}'.format(die))
            print('Total score: {}'.format(score))
            break
        else:
            print('Invalid choice. Try again.')
    print('='*25)
    print('You finished in {} turns!'.format(turn))
            
main()
        
        
        
        
        
        
        
        