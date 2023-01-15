def add(num1:int, num2: 2):
    return num1 + num2 
    
def subtract(num1:int, num2: 2):
    return num1 - num2 
    
def multiply(num1:int, num2: 2):
    return num1 * num2 
    
def divide(num1:int, num2: 2):
    return num1 / num2 


class InsufficientFunds(Exception):   # This is extending the Exception class, so it is an exception. 
    pass                              # There are no properties, so just say pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance 
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *=1.1