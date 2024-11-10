import random 
from land import Territory
class Person:
    name: str
    cash: float
    def __init__(self, name) -> None:
        self.name = name
        self.cash = round(random.random() * 201, 2) 
    
    def exchange_cash_for_gas(self, territory: Territory):
        gas_price = 1
        print(f'{self.name}: ${gas_price} a gallon is pretty reasonable....')
        gas_obtained = (self.cash * 1 / gas_price)
        if territory.gas > gas_obtained:
            territory.gas -= gas_obtained
            territory.cash += self.cash
            self.cash = 0
        elif territory.gas == gas_obtained:
            print(f'{self.name}: Damn, must be lucky...')
            territory.gas -= gas_obtained
            territory.cash += self.cash
            self.cash = 0
        elif territory.gas == 0:
            print(f"{self.name}: Shit, I guess we're gonna be here awhile...")
            gas_obtained = 0
        else: 
            print(f"{self.name}: It's not alot, but it will do...")
            gas_obtained = territory.gas
            amount_paid = territory.gas * gas_price
            territory.gas = 0
            territory.cash += amount_paid
            self.cash -= amount_paid
        return gas_obtained
    
    def pay_for_something(self, amount, reason):
        if amount > self.cash:
            print(f"{self.name}: I can't afford that")
        else:
            print(f"{self.name}: I guess I'll pay ${amount} for {reason}")
            self.cash -= amount