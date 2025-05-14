import random
from data_structures import Drone, Delivery, NoFlyZone

def generate_drones(n=1):
    drones = []
    for i in range(n):
        drones.append(Drone(
            id=i,
            max_weight=random.uniform(5, 10),
            battery=random.randint(2000, 5000),
            speed=random.uniform(5, 15),
            start_pos=(random.randint(0, 100), random.randint(0, 100))
        ))
    return drones

def generate_deliveries(n=5):
    deliveries = []
    for i in range(n):
        deliveries.append(Delivery(
            id=i,
            pos=(random.randint(0, 100), random.randint(0, 100)),
            weight=random.uniform(1, 5),
            priority=random.randint(1, 5),
            time_window=("09:00", "10:00")
        ))
    return deliveries

def generate_no_fly_zones(n=1):
    zones = []
    for i in range(n):
        coords = [(random.randint(20, 80), random.randint(20, 80)) for _ in range(4)]
        zones.append(NoFlyZone(
            id=i,
            coordinates=coords,
            active_time=("09:30", "11:00")
        ))
    return zones
