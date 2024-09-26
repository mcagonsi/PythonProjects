# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:22:21 2023

@author: Michael.Agonsi
"""
loop = 'y'
loop = loop.lower()
while loop == "y":
    monthlyInvestment = float(input('Enter monthly investment:\t'))
    yearlyInterestRate = float(input('Enter yearly interest rate:\t'))
    numberOfYears = int(input('Enter number of years:\t'))

    def futureValueCalculator (mon_inv, yr_intr, num_yr):
        mon_rate = (yr_intr/12)/100
        total_mon = num_yr*12
        futureValue = 0
        for i in range(0,total_mon):
            futureValue += mon_inv
            mon_intr = futureValue * mon_rate
            futureValue += mon_intr
        return futureValue
    futureValue=futureValueCalculator (monthlyInvestment, yearlyInterestRate, numberOfYears)
    print(f'Future Value:\t{futureValue:.2f}') 
    loop = input('Continue? (y/n): ')
   

   




