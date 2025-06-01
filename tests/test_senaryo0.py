import sys
import os
import time
import heapq

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.a_star import a_star
from algorithms.constraint_solver import csp_assignments_multi
from algorithms.genetic_algorithm import optimize_routes, fitness
from utils.visualizer import plot_routes
from utils.load_veri_seti import load_veri_seti
from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone
from utils.time_utils import is_time_valid

#SABİT VERİ SETİ İLE TÜM ALGORTİMALAR

current_time = 600  # 10:00

drones, deliveries, no_fly_zones = load_veri_seti()  # Kullanıcının sabit veri seti

SARJ_LIMIT = 30
SARJ_SURESI = 20

def run_astar():
    print("\n🔹 A* Çalıştırılıyor")
    success_count = 0
    total_energy = 0
    total_charging_time = 0
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
    if not assignments_list or len(assignments_list[0]) == 0:
        return 0, 0, 0, []
    assignments = assignments_list[0]

    success = 0
    total_energy = 0
    total_charging_time = 0
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

    success = 0
    total_energy = 0
    charging = 0
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

def test_senaryo0():
    print("\n🚀 Senaryo 0: Kendi sabit veri seti ile A*, CSP+A*, GA")
    start = time.time()

    # A*
    s1, e1, c1, _ = run_astar()
    # CSP + A*
    s2, e2, c2, _ = run_csp()
    # GA
    s3, e3, c3, _ = run_ga()

    end = time.time()
    print("\n📊 METRİK ÖZETİ (Senaryo 0)")
    print(f"🔹 A*: Teslimat={s1}, Enerji={e1:.2f}, Şarj={c1} dk")
    print(f"🔹 CSP: Teslimat={s2}, Enerji={e2:.2f}, Şarj={c2} dk")
    print(f"🔹 GA: Teslimat={s3}, Enerji={e3:.2f}, Şarj={c3} dk")
    print(f"⏱️ Toplam Çalışma Süresi: {end - start:.2f} saniye")

    plot_routes(drones, deliveries, no_fly_zones, show=True)

if __name__ == "__main__":
    test_senaryo0()

