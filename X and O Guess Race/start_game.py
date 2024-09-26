# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 12:02:14 2023

@author: Chidera
"""
import random
def race_track():
    '''
    

    Returns
    -------
    None.

    '''
    print('s----------------------------------------------------------' +
          '\nt====================================================**|s' +
          '\na| | | | | | | | | | | | | | | | **|t' +
          '\nr| | | | | | | | | | | | | | | | **|o' +
          '\nt====================================================**|p' +
          '\n---------------------------------------------------------')
    
    
def player_position()->list:
    '''
    

    Returns
    -------
    list
        DESCRIPTION.

    '''
    player1 = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    player2 = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    return player1, player2


def track_view(p1:list,p2:list):
    '''
    

    Parameters
    ----------
    p1 : list
        DESCRIPTION.
    p2 : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    print('s------------------------------------' +
          '\nt================================**|s' +
          f'\na|{p1[0]}|{p1[1]}|{p1[2]}|{p1[3]}|{p1[4]}|{p1[5]}|{p1[6]}|{p1[7]}|{p1[8]}|{p1[9]}|{p1[10]}|{p1[11]}|{p1[12]}|{p1[13]}|{p1[14]}|{p1[15]}**|t' +
          f'\nr|{p2[0]}|{p2[1]}|{p2[2]}|{p2[3]}|{p2[4]}|{p2[5]}|{p2[6]}|{p2[7]}|{p2[8]}|{p2[9]}|{p2[10]}|{p2[11]}|{p2[12]}|{p2[13]}|{p2[14]}|{p2[15]}**|o' +
          '\nt================================**|p' +
          '\n-------------------------------------')

def player_name()-> str and str and str and str and list and list:
    '''
    

    Returns
    -------
    str and str and str and str and list and list
        DESCRIPTION.

    '''
    #takes the player names
    print('Player 1 - X and Player 2 - O')
    print()
    player1 = input('Player 1 Name: ').title()
    player2 = input('Player 2 Name: ').title()
    print()
    print('{} vs {} '.format(player1,player2))
    print()
    p1, p2 = player_position()
    n1 = 'X'
    n2 = 'O'
    p1[0] = n1
    p2[0] = n2
    #initializes the position of the players ans assigns the avatar for each player i.e X and O
    track_view(p1, p2)
    return player1, player2, n1, n2,p1,p2

def random_number ()-> int:
    '''
    

    Returns
    -------
    int
        DESCRIPTION.

    '''
    #this generates a random number for each player
    print('I have selected a number from 1 - 5. Now guess the number! You have 2 tries only  ;)')
    randnum = random.randint(1,5)
    return randnum

def main():
    '''
    

    Returns
    -------
    None.

    '''
    player1, player2, n1, n2,p1,p2= player_name()
    print()
    print('Ready, Set, and Go!')
    print()
    
    while True:
        
        
        #starts the play
        print(f"{player1}'s turn")
        print()
        random = random_number()
        c=0 #for counting the number of tries
        while c < 2:
            try:
                guess = int(input('Your guess: ')) #guess input from player
                if guess >=1 and guess <=5:
                    c+=1 
                    #2 steps awarded to right guess on first try and 1step to right guess on two tries and no steps to wrong guesses
                    if guess == random and c == 1:
                        i = p1.index(n1)
                        p1[i]= ' ' #replaces the current position with an empty space
                        i+=2 
                        p1[i] = n1 #replacs the new player position with the avatar
                        print()
                        print('Great guess! You move 2 steps!')
                        break
                    elif guess == random and c == 2:
                        i = p1.index(n1)
                        p1[i]= ' '
                        i+=1 
                        p1[i] = n1
                        print()
                        print('Nice guess! You move 1 step')
                        break
                    if c == 2 and guess != random: #if guesses are wrong after two tries
                        print()
                        print(':( Too bad wrong guesses. You stay put')
                        print()
                        break
                    
                else:
                    print()
                    print('Your guess is out of range')
                    print()
                
            except ValueError:
                print('You must enter an integer')
                print()
       
       #checks the win conditions
        if p1.index(n1) >= 15:
            print()
            print(f'{player1} wins the race! :) ')
            print()
            break
        elif p2.index(n2) >= 15:
            print()
            print(f'{player2} wins the race! :)')
            print()
            break
        
        track_view(p1, p2)
        print()
        print()
        
        
        print(f"{player2}'s turn")
        print()
        random = random_number()
        c=0
        while c < 2:
            try:
                guess = int(input('Your guess: '))
                if guess >=1 and guess <=5:
                    c+=1
                    if guess == random and c == 1:
                        i = p2.index(n2)
                        p2[i]= ' '
                        i+=2 
                        p2[i] = n2
                        print()
                        print('Great guess! You move 2 steps!')
                        print()
                        break
                    elif guess == random and c == 2:
                        i = p2.index(n2)
                        p2[i]= ' '
                        i+=1 
                        p2[i] = n2
                        print()
                        print('Nice guess! You move 1 step')
                        print()
                        break
                    if c == 2 and guess != random:
                        print()
                        print(':(  Too bad wrong guesses. You stay put.')
                        print()
                        break
                    
                else:
                    print()
                    print('Your guess is out of range')
                    print()
                
            except ValueError:
                print('You must enter an integer')
                print()
        
        #checks the win condition
        if p1.index(n1) >= 15:
            print()
            print(f'{player1} wins the race! :) ')
            print()
            break
        elif p2.index(n2) >= 15:
            print()
            print(f'{player2} wins the race! :)')
            print()
            break
        track_view(p1, p2)
        print()
        print()
        
    
    
if __name__ == "__main__":
    #this module contains the actual game to be played
    
    main()