from dataclasses import dataclass
from datetime import datetime
DATE_FORMAT = '%m/%d/%Y'
@dataclass
class Person:
    _FirstName: str
    _LastName: str
    _Gender: str
    _DateOfBirth: str
    _Relationship: str
    _PhoneNumber: str
    _StateOfOrigin:str
    _CountryOfOrigin:str
    _StreetAddress:str
    _City:str
    _Country:str
    _PostalCode:str

    @property
    def FirstName(self):
        return self._FirstName
    @property
    def LastName(self):
        return self._LastName
    @property
    def Gender(self):
        return self._Gender
    @property
    def DateOfBirth(self):
        return self._DateOfBirth
    @property
    def Relationship(self):
        return self._Relationship

    @property
    def PhoneNumber(self):
        return self._PhoneNumber

    @PhoneNumber.setter
    def PhoneNumber(self, value):
        try:
            phone = int(value)
            self._PhoneNumber = phone
        except ValueError:
            pass

    @property
    def StateOfOrigin(self):
        return self._StateOfOrigin

    @property
    def CountryOfOrigin(self):
        return self._CountryOfOrigin
    @property
    def StreetAddress(self):
        return self._StreetAddress
    @property
    def City(self):
        return self._City
    @property
    def Country(self):
        return self._Country
    @property
    def PostalCode(self):
        return self._PostalCode

    @property
    def FullAddress(self):
        return self._StreetAddress + ', \n' + self._City + ', \n' + self._Country + ', ' + self._PostalCode

    @property
    def FullName(self):
        return self._FirstName + ' ' + self._LastName


@dataclass
class Employee(Person):
    _EmployeeID: int
    _Role:str
    _Active:bool

    @property
    def Role(self):
        return self._Role
    @property
    def Active(self):
        return self._Active
    @Active.setter
    def Active(self,status):
        self._Active = status

    @property
    def EmployeeID(self):
        return self._EmployeeID


@dataclass
class Customer(Person):
    _CustomerID: int

    @property
    def CustomerID(self):
        return self._CustomerID



@dataclass
class ExternalClient:
    _Bank: str # this will have to take a bank class as the input.
    _FullName:str
    _AccountNumber:int
    _Amount:float


    def __post_init__(self):
        pass
        # self._Bank = Bank() #this should instantiate the selected bank class and accounts for validating client

    @property
    def FullName(self):
        return self._FullName

    @property
    def accountNumber(self):
        return self._AccountNumber

    @property
    def amount(self):
        return self._Amount

    @property
    def bankName(self):
        return self._Bank



def main():
    pass

if __name__ == '__main__':
    main()