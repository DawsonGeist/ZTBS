import networkx as nx
import functions as fns
from vehicles import Truck
from npc import Person
import threading
import time

world_ref = fns.get_world_adj_dict()
world = fns.build_starting_world(world_ref)

d1 = Person('DRIVER1')
# d2 = Person('DRIVER2')

v1 = Truck(id='t1', home='H', world_ref=world_ref, world=world, driver=d1)
# v2 = Truck('t2', 'A', world_ref, world, d2)
# fleet = [v1, v2]

t1 = threading.Thread(target=v1.wander)
# t2= threading.Thread(target=v2.wander)
t1.start()
# t2.start()
while t1.is_alive(): # or t2.is_alive():
    time.sleep(1)
t1.join()
# t2.join()


