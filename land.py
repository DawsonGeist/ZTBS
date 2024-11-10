class Territory():
    name: str
    cash: float
    gas: float
    population: int
    contracts: list
    neighbors: dict
    def __init__(self, name, cash=1000, population=10, contracts=[]):
        import random
        self.name = name
        self.cash = cash
        self.gas = random.randint(10, 100)
        self.population = population
        self.contracts = []
        self.neighbors = {}
    
    def add_connection(self, territory, cost: int, road_condition: int):
        # Add territory to our dict of neighbors if we havent already
        self.neighbors[territory.name] = {
            "object": territory,
            "cost": cost,
            "road_condition": road_condition
        }
        # Add ourself to the territory's dict of neighbors if they havent already
        territory.neighbors[self.name] = {
            "object": self,
            "cost": cost,
            "road_condition": road_condition
        }
    
    def get_travel_cost_to_neighbor(self, destination):
        if destination in self.neighbors.keys():
            if self.neighbors[destination]['road_condition'] > 0:
                return round(self.neighbors[destination]['cost'] / self.neighbors[destination]['road_condition'])
            else:
                return -1
        else: 
            print(f'{self.name} is not connected to {destination}')
            return -1
    
    def get_neighbor(self, neighbor):
        return self.neighbors[neighbor]['object']
    
    def repair_road(self, neighbor_key: str, person):
        import math
        if neighbor_key in self.neighbors.keys():
            connection = self.neighbors[neighbor_key]
            repair_points = math.floor(person.cash / 100)
            if repair_points > 3:
                repair_points = 3
                cash_spent = 300
            elif repair_points == 0:
                cash_spent = 0
            else:
                cash_spent = repair_points * 100
            connection['road_condition'] += repair_points
            if repair_points > 0:
                person.pay_for_something(cash_spent, "ROAD_REPAIR")
        else:
            print(f'(repair_road) {self.name} is not connected to {neighbor_key}')


