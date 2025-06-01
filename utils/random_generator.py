import random
from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone
from utils.time_utils import time_to_minutes

def generate_random_drones(count=10):
    drones = []
    for i in range(count):
        drone = Drone(
            id=i,
            max_weight=round(random.uniform(3.0, 6.0), 1),
            battery=random.randint(80, 100),
            speed=round(random.uniform(8.0, 12.0), 1),
            start_pos=(random.randint(0, 20), random.randint(0, 20))
        )
        drones.append(drone)
    return drones

def generate_random_deliveries(count=50):
    deliveries = []
    for i in range(count):
        delivery = Teslimat(
            id=i,
            pos=(random.randint(0, 100), random.randint(0, 100)),
            weight=round(random.uniform(1.0, 4.0), 1),
            priority=random.randint(1, 5),
            time_window=(time_to_minutes("09:00"), time_to_minutes("11:00"))
        )
        deliveries.append(delivery)
    return deliveries

def generate_random_noflyzones(count=5):
    nfzs = []
    for i in range(count):
        x, y = random.randint(20, 80), random.randint(20, 80)
        coordinates = [
            (x, y),
            (x+5, y),
            (x+5, y+5),
            (x, y+5)
        ]
        nfz = NoFlyZone(
            id=i,
            coordinates=coordinates,
            active_time=(time_to_minutes("09:30"), time_to_minutes("11:30"))
        )
        nfzs.append(nfz)
    return nfzs
