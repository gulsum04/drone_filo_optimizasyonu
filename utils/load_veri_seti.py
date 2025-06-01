from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone

def load_veri_seti(path="data/veri_seti.txt"):
    veri = {}
    with open(path, "r", encoding="utf-8") as f:
        exec(f.read(), {}, veri)

    drones = [Drone(**d) for d in veri["drones"]]
    deliveries = [Teslimat(**d) for d in veri["deliveries"]]
    no_fly_zones = [NoFlyZone(**z) for z in veri["no_fly_zones"]]

    return drones, deliveries, no_fly_zones
