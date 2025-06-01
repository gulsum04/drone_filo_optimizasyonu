import sys
import os
import time
import heapq
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.a_star import a_star
from algorithms.constraint_solver import csp_assignments_multi
from algorithms.genetic_algorithm import optimize_routes, fitness
from utils.visualizer import plot_routes
from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone
from utils.time_utils import is_time_valid, time_to_minutes

# DİNAMİK VERİ : 10 drone, 50 teslimat, 5 dinamik no-fly zone TÜM ALGORİTMALAR

def generate_random_drones(count=10):
    return [Drone(
        id=i,
        max_weight=round(random.uniform(3.0, 6.0), 1),
        battery=random.randint(80, 100),
        speed=round(random.uniform(8.0, 12.0), 1),
        start_pos=(random.randint(0, 20), random.randint(0, 20))
    ) for i in range(count)]

def generate_random_deliveries(count=50):
    return [Teslimat(
        id=i,
        pos=(random.randint(0, 100), random.randint(0, 100)),
        weight=round(random.uniform(1.0, 4.0), 1),
        priority=random.randint(1, 5),
        time_window=(time_to_minutes("09:00"), time_to_minutes("11:00"))
    ) for i in range(count)]

def generate_random_noflyzones(count=5):
    return [NoFlyZone(
        id=i,
        coordinates=[(x := random.randint(20, 80), y := random.randint(20, 80)), (x+5, y), (x+5, y+5), (x, y+5)],
        active_time=(time_to_minutes("09:30"), time_to_minutes("11:30"))
    ) for i in range(count)]

current_time = time_to_minutes("10:00")
drones = generate_random_drones()
deliveries = generate_random_deliveries()
no_fly_zones = generate_random_noflyzones()

SARJ_LIMIT = 30
SARJ_SURESI = 20

def run_astar():
    print("\n🔹 A* Çalıştırılıyor")
    success_count = total_energy = total_charging_time = 0
    routes = []
    for drone in drones:
        teslimat_heap = [(-d.priority, d) for d in deliveries if d.weight <= drone.max_weight and not d.assigned]
        heapq.heapify(teslimat_heap)
        while teslimat_heap:
            _, delivery = heapq.heappop(teslimat_heap)
            route, energy = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, no_fly_zones, current_time)
            if route:
                if drone.battery - energy < SARJ_LIMIT:
                    drone.battery = 10000
                    total_charging_time += SARJ_SURESI
                drone.battery -= energy
                drone.start_pos = delivery.pos
                delivery.assigned = True
                drone.route = route
                routes.append(route)
                success_count += 1
                total_energy += energy
                break
    return success_count, total_energy, total_charging_time, routes

def run_csp():
    print("\n🔹 CSP + A* Çalıştırılıyor")
    assignments_list = csp_assignments_multi(drones, deliveries, no_fly_zones, current_time=current_time)
    if not assignments_list or not assignments_list[0]:
        return 0, 0, 0, []
    assignments = assignments_list[0]
    success = total_energy = total_charging_time = 0
    routes = []
    for delivery_id, drone_id in assignments.items():
        drone = next((d for d in drones if d.id == drone_id), None)
        delivery = next((d for d in deliveries if d.id == delivery_id), None)
        if not delivery or not is_time_valid(current_time, delivery):
            continue
        route, energy = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, no_fly_zones, current_time)
        if route:
            if drone.battery - energy < SARJ_LIMIT:
                drone.battery = 10000
                total_charging_time += SARJ_SURESI
            drone.battery -= energy
            drone.start_pos = delivery.pos
            delivery.assigned = True
            drone.route = route
            routes.append(route)
            success += 1
            total_energy += energy
    return success, total_energy, total_charging_time, routes

def run_ga():
    print("\n🔹 Genetik Algoritma (GA) Çalıştırılıyor")
    individual = optimize_routes(drones, deliveries, no_fly_zones, generations=50, population_size=10, current_time=current_time)
    score = fitness(individual, drones, deliveries, no_fly_zones, current_time)
    success = total_energy = charging = 0
    drone_positions = {d.id: d.start_pos for d in drones}
    drone_battery = {d.id: 10000 for d in drones}
    routes = []
    for drone_id, delivery_id in individual:
        drone = drones[drone_id - 1]
        delivery = deliveries[delivery_id - 1]
        route, energy = a_star(drone_positions[drone.id], delivery.pos, delivery.weight, delivery.priority, no_fly_zones, current_time)
        if route:
            if drone_battery[drone.id] - energy < SARJ_LIMIT:
                drone_battery[drone.id] = 10000
                charging += SARJ_SURESI
            drone_battery[drone.id] -= energy
            drone_positions[drone.id] = delivery.pos
            delivery.assigned = True
            routes.append(route)
            success += 1
            total_energy += energy
    return success, total_energy, charging, routes

def test_senaryo2():
    print("\n🚀 Senaryo 2: Dinamik 10 drone, 50 teslimat, 5 dinamik no-fly zone ile A*, CSP+A*, GA")
    start = time.time()
    s1, e1, c1, _ = run_astar()
    s2, e2, c2, _ = run_csp()
    s3, e3, c3, _ = run_ga()
    end = time.time()
    print("\n📊 METRİK ÖZETİ (Senaryo 2)")
    print(f"🔹 A*: Teslimat={s1}, Enerji={e1:.2f}, Şarj={c1} dk")
    print(f"🔹 CSP: Teslimat={s2}, Enerji={e2:.2f}, Şarj={c2} dk")
    print(f"🔹 GA: Teslimat={s3}, Enerji={e3:.2f}, Şarj={c3} dk")
    print(f"⏱️ Toplam Çalışma Süresi: {end - start:.2f} saniye")
    plot_routes(drones, deliveries, no_fly_zones, show=True)

if __name__ == "__main__":
    test_senaryo2()
