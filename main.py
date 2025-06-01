import copy
import time
import heapq
import sys
import os

from algorithms.a_star import a_star
from algorithms.genetic_algorithm import optimize_routes, fitness
from algorithms.constraint_solver import csp_assignments_multi
from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone
from utils.visualizer import plot_routes
from utils.time_utils import time_to_minutes, is_time_valid
from utils.random_generator import (
    generate_random_drones,
    generate_random_deliveries,
    generate_random_noflyzones
)

#DİNAMİK VERİ SETİ ALGORİTMAYI SEÇEREK

# === VERİ SETİ (Rastgele) ===
drones_base = generate_random_drones(count=10)
deliveries_base = generate_random_deliveries(count=50)
nfz_list = generate_random_noflyzones(count=5)

def run_astar():
    drones = copy.deepcopy(drones_base)
    deliveries = copy.deepcopy(deliveries_base)
    success, energy, charging_time = 0, 0, 0
    current_time = 540  # 09:00
    routes = []

    for drone in drones:
        teslimat_heap = [(-d.priority, d) for d in deliveries if d.weight <= drone.max_weight and not d.assigned]
        heapq.heapify(teslimat_heap)

        while teslimat_heap:
            _, delivery = heapq.heappop(teslimat_heap)
            route, e = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, nfz_list, current_time)
            if route:
                routes.append(route)
                if drone.battery - e < 30:
                    charging_time += 20
                    drone.battery = 100
                else:
                    drone.battery -= e
                delivery.assigned = True
                drone.start_pos = delivery.pos
                success += 1
                energy += e
                break

    score = success * 100 - energy - charging_time
    return {
        "name": "A*",
        "success": success,
        "energy": round(energy, 2),
        "charging": charging_time,
        "score": round(score, 2),
        "routes": routes
    }

def run_csp():
    drones = copy.deepcopy(drones_base)
    deliveries = copy.deepcopy(deliveries_base)
    success, energy, charging_time = 0, 0, 0
    current_time = 540
    routes = []

    assignments_list = csp_assignments_multi(drones, deliveries, nfz_list, current_time)
    if not assignments_list or len(assignments_list[0]) == 0:
        return {"name": "CSP+A*", "success": 0, "energy": 0, "charging": 0, "score": 0}

    solution = assignments_list[0]
    sorted_assignments = sorted(solution.items(), key=lambda x: -next(d.priority for d in deliveries if d.id == x[0]))

    for delivery_id, drone_id in sorted_assignments:
        drone = next((d for d in drones if d.id == drone_id), None)
        delivery = next((d for d in deliveries if d.id == delivery_id), None)
        if delivery and is_time_valid(current_time, delivery):
            route, e = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, nfz_list, current_time)
            if route:
                if drone.battery - e < 30:
                    charging_time += 20
                    drone.battery = 100
                else:
                    drone.battery -= e
                drone.start_pos = delivery.pos
                delivery.assigned = True
                routes.append(route)
                success += 1
                energy += e

    score = success * 100 - energy - charging_time
    return {
        "name": "CSP+A*",
        "success": success,
        "energy": round(energy, 2),
        "charging": charging_time,
        "score": round(score, 2),
        "routes": routes
    }

def run_ga():
    drones = copy.deepcopy(drones_base)
    deliveries = copy.deepcopy(deliveries_base)
    current_time = 540

    best_individual = optimize_routes(drones, deliveries, nfz_list, generations=50, population_size=10, current_time=current_time)
    best_score = fitness(best_individual, drones, deliveries, nfz_list, current_time)

    success, energy_total, charging_time = 0, 0, 0
    drone_positions = {d.id: d.start_pos for d in drones}
    drone_battery = {d.id: 100 for d in drones}
    routes = []

    for drone_id, delivery_id in best_individual:
        drone = drones[drone_id]
        delivery = deliveries[delivery_id]
        route, e = a_star(drone_positions[drone_id], delivery.pos, delivery.weight, delivery.priority, nfz_list, current_time)
        if route:
            success += 1
            energy_total += e
            routes.append(route)
            if drone_battery[drone_id] - e < 30:
                charging_time += 20
                drone_battery[drone_id] = 100
            else:
                drone_battery[drone_id] -= e
            drone_positions[drone_id] = delivery.pos

    return {
        "name": "GA",
        "success": success,
        "energy": round(energy_total, 2),
        "charging": charging_time,
        "score": round(best_score, 2),
        "routes": routes
    }

if __name__ == "__main__":
    selected = "CSP"  # 🔁 Değiştir: "A*", "CSP", "GA"

    if selected == "A*":
        result = run_astar()
    elif selected == "CSP":
        result = run_csp()
    elif selected == "GA":
        result = run_ga()
    else:
        raise ValueError("Geçersiz algoritma seçimi")

    print(f"\n📊 {result['name']} Sonuçları")
    print(f"✅ Teslimat: {result['success']}")
    print(f"⚡ Enerji: {result['energy']}")
    print(f"🔋 Şarj Süresi: {result['charging']} dk")
    print(f"🏁 Skor: {result['score']}\n")

    plot_routes(drones_base, deliveries_base, nfz_list, show=True)
