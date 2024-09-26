# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:03:37 2023

@author: Michael.Agonsi
"""
def FahrenheitToCelcius(fah) -> float:
    
    cel = ((fah - 32)*5)/9
    return cel


def CelciusToFahrenheit(cel) -> float:
    
    fah = ((cel * 9)/5) + 32
    return fah

def CelciusToKelvin(cel) -> float:
    
    kel = cel + 273 
    return kel

def FahrenheitToKelvin(fah) -> float:
    kel = (((fah - 32)*5)/9) + 273
    return kel

def KelvinToCelcius(kel) -> float:
    cel = kel - 273
    return cel

def KelvinToFahrenheit(kel) -> float:
    fah = (((kel - 273)*9)/5) + 32
    return fah