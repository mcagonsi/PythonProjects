# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 11:06:54 2023

@author: Michael.Agonsi
"""

import random

def get_num():
    return random.randrange(0,50)

def get_tuple(length):
    data = ([get_num() for n in range(length)])
    return data
    
def get_list(length):
     data = [get_num() for n in range(length)]
     return data
 
def get_avg(collection):
     avg = sum(collection)/2
     return avg

def median(collection):
    length = len(collection)
    if length % 2 == 0:
        indexes = [(length/2)-1, length /2]
    else:
        indexes = [length // 2]
    median = 0
    sort_collection = sorted(collection)
    for i in indexes:
        median += sort_collection[int(i)]
    median = median/len(indexes)
    return median

def get_min (collection):
    return min(collection)

def get_max (collection):
    return max(collection)

def get_duplicate (collection):
    dups = []
    for num in collection:
        count = collection.count(num)
        if count >= 2 and (num not in dups):
            dups.append(num)
            
    return dups

def main():
 
        num_int = int(input('How many number of integers do you want? : '))
     
        print()
        tuples = get_tuple(num_int)
        tuple_avg = get_avg(tuples)
        tuple_median = median(tuples)
        tuple_min = get_min(tuples)
        tuple_max = get_max(tuples)
        tuple_dup = get_duplicate(tuples)
        
        list_data = get_list(num_int)
        list_avg = get_avg(list_data)
        list_median = median(list_data)
        list_min = get_min(list_data)
        list_max = get_max(list_data)
        list_dups = get_duplicate(list_data)
        
        
        
        print('TUPLE DATA:',tuples) 
        print("Average = {}  Median = {}  Min = {}  Max = {}   Dups = {} ".format(tuple_avg, tuple_median, tuple_min, tuple_max, tuple_dup))
        
        print()
        print()
        print('RANDOM DATA:',list_data) 
        print("Average = {}  Median = {}  Min = {}  Max = {}   Dups = {} ".format(list_avg, list_median, list_min, list_max, list_dups))
        
    
    
    
    
    
    
    
    
    
    
    
    
main()
                                
