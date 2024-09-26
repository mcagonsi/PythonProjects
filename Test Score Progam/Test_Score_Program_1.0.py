# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 10:39:57 2023

@author: Michael.Agonsi
"""

#The console for the Test Scores Program

print('The Test Scores Program')
print('')
print('Enter 3 test scores')
print('='*22)

#Requesting inputs and assigning variables
counter = 0
t1 = float(input('Enter test score:\t'))
t2 = float(input('Enter test score:\t'))
t3 = float(input('Enter test score:\t'))
counter+=3

#formula for the calculation
#note that we dont use chaining statements here to avoid semantic errors
t_total = t1+t2+t3
avg_score= t_total/counter

#giving output or result
print(22*'=')
print('Total Score:\t',int(t_total))
print('Average Score:\t', int(avg_score))
print('')
print("Good Bye")
