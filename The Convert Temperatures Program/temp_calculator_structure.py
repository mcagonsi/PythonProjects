# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 05:34:05 2023

@author: Chidera
"""
import temperature_formulas as TCF

def title():
    print('MENU' + 
          '\n1. Fahrenheit to Celcuis' + 
          '\n2  Celcius to Fahrenheit' + 
          '\n3. Fahrenheit to Kelvin' + 
          '\n4. Kelvin to Fahrenheit' +
          '\n5. Kelvin to Celcius' +
          '\n6. Celcius to Kelvin')
def menu_input():
        menu =int(input("Enter a menu option:\t"))
     
        return menu
          
    
    

def FahToCel():
    fah = float(input("Enter degrees Fahrenheit:\t"))
    cel = TCF.FahrenheitToCelcius(fah)
    print(f"Degrees Celcius:\t{cel:.1f}")

def CelToFah():
    cel = float(input("Enter Degrees Celcius:\t"))
    fah = TCF.CelciusToFahrenheit(cel)
    print(f"Degrees Fahrenheit:\t{fah}")

def FahToKel():
    fah = float(input("Enter Degrees Fahrenheit:\t"))
    kel = TCF.FahrenheitToKelvin(fah)
    print(f'Degrees Kelvin:\t{kel:.1f}')

def KelToFah():
    kel = float(input("Enter Degrees Kelvin:\t"))
    fah = TCF.KelvinToFahrenheit(kel)
    print(f"Degrees Fahrenheit:\t{fah:.1f}")

def KelToCel():
    kel = float(input("Enter Degrees Kelvin:\t"))
    cel = TCF.KelvinToCelcius(kel)
    print(f"Degrees Celcius:\t{cel:.1f}")

def CelToKel():
    cel = float(input("Enter Degrees Celcius:\t"))
    kel = TCF.CelciusToKelvin(cel)
    print(f"Degrees Kelviin:\t{kel:.1f}")