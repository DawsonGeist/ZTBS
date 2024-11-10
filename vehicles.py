import time
from npc import Person
from land import Territory
class Truck:
    id: str
    home: Territory
    located_at: Territory
    health: int
    gas: int
    cargo: dict
    # Dictionaries are passed by reference so they are, basically static variables. SO all the trucks will share updates
    world: dict
    world_ref: dict
    status:str
    driver: Person
    crew: list
    def __init__(self, id, home, world_ref, world, driver, crew=[], cargo={}):
        self.id = id
        self.home = world[home]
        self.located_at = world[home]
        self.health = 1000
        self.gas = 100
        self.world = world
        self.world_ref = world_ref
        self.status= 'IDLE'
        self.driver = driver
        self.crew = crew
        self.cargo = cargo

    def send_on_route(self, destination: Territory):
        import functions as fns
        import random
        cost, route = fns.get_path_A_B(self.world_ref, self.located_at.name, destination.name)
        print(f'{self.id}: BEGIN ROUTE: {route}')
        for step in route:
            distance = self.located_at.get_travel_cost_to_neighbor(destination=step[1])
            if self.gas > distance and distance > 0:
                # TODO: This is fucked cause objects are not in sync
                # TODO: Make World the only ref on objects... let territories hold only the road conditions between territories
                # NOTE: I might have fixed it when I did build connections
                destination = self.located_at.get_neighbor(neighbor=step[1]) 
                #destination = self.world[step[1]]
                self.drive(destination, distance)
                print(f'{self.id}: ARRIVED AT {step[1]}')
                self.status="IDLE"
                # Do any trading or bartering while here?
                self.driver.cash += round(random.random()*30,2)
            elif distance == -1:
                print(f'{self.id}: ROAD OUT: {self.located_at.name} -> {step[1]}')
                self.located_at.repair_road(step[1], self.driver)
                self.status="ROAD OUT"
                break
            else:
                # Do any trading or bartering while here?
                gas_obtained = self.driver.exchange_cash_for_gas(self.located_at) # TODO: Add person function for this
                if gas_obtained > 0:
                    self.gas += gas_obtained
                else:
                    self.status = 'STRANDED'
                    break

    def drive(self, destination: Territory, cost: int):
        import random
        self.status = "DRIVING"
        print(f'{self.id}: DRIVING TO {destination.name}')
        # Does anything happen? odds?
        time.sleep(round(cost))
        # We arrived
        self.located_at = self.world[destination.name]
        self.gas -= cost
    
    def wander(self):
        import random
        while self.status != 'STANDED':
            choices = []
            for dest in self.world:
                choices.append(self.world[dest])
            destination = random.choice(choices)
            self.send_on_route(destination)

        
