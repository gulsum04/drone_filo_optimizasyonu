import sys
import os
import time
import heapq
import copy
import random
import matplotlib.pyplot as plt
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.a_star import a_star
from algorithms.genetic_algorithm import generate_initial_population, fitness
from algorithms.constraint_solver import csp_assignments_multi
from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone
from utils.visualizer import plot_routes
from utils.time_utils import is_time_valid, time_to_minutes
from utils.load_veri_seti import load_veri_seti

#SABİT VERİ SETİ:TÜM ALGORİTMALARIN KIYASLANMASI


# === Sabit Veri Setini Yükle ===
drones_base, deliveries_base, nfz_list = load_veri_seti()

# === A* Sadece Testi ===
def test_astar_only():
    drones = copy.deepcopy(drones_base)
    deliveries = copy.deepcopy(deliveries_base)
    success, energy, charging_time = 0, 0, 0
    start = time.time()
    current_time = 540
    routes = []

    for drone in drones:
        for delivery in deliveries:
            if delivery.weight <= drone.max_weight and not delivery.assigned:
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

    end = time.time()
    score = success * 100 - energy - charging_time
    return {
        "name": "A*",
        "success": success,
        "energy": round(energy, 2),
        "charging": charging_time,
        "score": round(score, 2),
        "time": end - start,
        "routes": routes
    }

# === CSP + A* Kombinasyonu ===
def test_csp_combined():
    drones = copy.deepcopy(drones_base)
    deliveries = copy.deepcopy(deliveries_base)
    current_time = 540
    success, energy, charging_time = 0, 0, 0
    start = time.time()
    assignments_list = csp_assignments_multi(drones, deliveries, nfz_list, current_time)
    if not assignments_list or len(assignments_list[0]) == 0:
        return {"name": "CSP+A*", "success": 0, "energy": 0, "charging": 0, "score": 0, "time": 0}

    solution = assignments_list[0]
    for drone in drones:
        for delivery_id, drone_id in solution.items():
            if drone.id == drone_id:
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
                        success += 1
                        energy += e
                        break
    end = time.time()
    score = success * 100 - energy - charging_time
    return {
        "name": "CSP+A*",
        "success": success,
        "energy": round(energy, 2),
        "charging": charging_time,
        "score": round(score, 2),
        "time": end - start
    }

# === Genetik Algoritma Testi ===
def test_ga_only():
    drones = copy.deepcopy(drones_base)
    deliveries = copy.deepcopy(deliveries_base)
    start = time.time()

    population = generate_initial_population(drones, deliveries, nfz_list, size=10)
    if not population:
        print("❌ GA: Başlangıç populasyonu boş, uygun birey üretilemedi.")
        return {"name": "GA", "success": 0, "energy": 0, "charging": 0, "score": 0, "time": 0}

    scores = [fitness(ind, drones, deliveries, nfz_list) for ind in population]
    best_index = scores.index(max(scores))
    best_individual = population[best_index]
    best_score = scores[best_index]

    success = 0
    energy_total = 0
    charging_time = 0
    current_time = 540

    drone_positions = {d.id: d.start_pos for d in drones}
    drone_battery = {d.id: 100 for d in drones}

    for drone_id, delivery_id in best_individual:
        drone = next((d for d in drones if d.id == drone_id), None)
        delivery = next((d for d in deliveries if d.id == delivery_id), None)
        if not drone or not delivery:
            continue

        route, e = a_star(
            drone_positions[drone_id],
            delivery.pos,
            delivery.weight,
            delivery.priority,
            nfz_list,
            current_time
        )

        if route:
            success += 1
            energy_total += e
            if drone_battery[drone_id] - e < 30:
                charging_time += 20
                drone_battery[drone_id] = 100
            else:
                drone_battery[drone_id] -= e
            drone_positions[drone_id] = delivery.pos

    end = time.time()

    return {
        "name": "GA",
        "success": success,
        "energy": round(energy_total, 2),
        "charging": charging_time,
        "score": round(best_score, 2),
        "time": round(end - start, 2)
    }

# === Ana Çalıştırma ===
if __name__ == "__main__":
    print("🚀 Karşılaştırmalı Algoritma Testi")
    astar_result = test_astar_only()
    csp_result = test_csp_combined()
    ga_result = test_ga_only()

    results = [astar_result, csp_result, ga_result]

    print("\n📊 Algoritma Karşılaştırması")
    print("-" * 70)
    print(f"{'Algoritma':<10} | {'Teslimat':<10} | {'Enerji':<10} | {'Şarj(dk)':<10} | {'Skor':<10} | {'Süre(sn)':<10}")
    print("-" * 70)
    for res in results:
        print(f"{res['name']:<10} | {res.get('success','-'):<10} | {res.get('energy','-'):<10} | {res.get('charging','-'):<10} | {res.get('score','-'):<10} | {res['time']:<10.2f}")

    print("\n📍 A* Algoritmasında üretilen rotalar çiziliyor...")
    plot_routes(drones_base, deliveries_base, nfz_list, show=False)

    print("📊 Algoritma performans grafikleri oluşturuluyor...")

    names = [r["name"] for r in results]
    times = [r["time"] for r in results]
    successes = [r["success"] if isinstance(r["success"], int) else 0 for r in results]
    energies = [r["energy"] if isinstance(r["energy"], (int, float)) else 0 for r in results]
    scores = [r["score"] if isinstance(r["score"], (int, float)) else 0 for r in results]

    fig, axs = plt.subplots(1, 4, figsize=(20, 4))
    axs[0].bar(names, successes, color='green')
    axs[0].set_title("Teslimat Sayısı")
    axs[1].bar(names, energies, color='orange')
    axs[1].set_title("Toplam Enerji")
    axs[2].bar(names, times, color='blue')
    axs[2].set_title("Çalışma Süresi (s)")
    axs[3].bar(names, scores, color='purple')
    axs[3].set_title("Skor")

    for ax in axs:
        ax.set_ylabel("Değer")
        ax.set_xlabel("Algoritma")
        ax.grid(True)

    plt.tight_layout()
    plt.show()

    csv_path = "algoritma_karsilastirmaSBT.csv"
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Algoritma", "Teslimat", "Enerji", "Şarj(dk)", "Skor", "Süre(sn)"])
        writer.writeheader()
        for row in results:
            writer.writerow({
                "Algoritma": row.get("name", "-"),
                "Teslimat": row.get("success", "-"),
                "Enerji": row.get("energy", "-"),
                "Şarj(dk)": row.get("charging", "-"),
                "Skor": row.get("score", "-"),
                "Süre(sn)": round(row.get("time", 0), 2)
            })

    print(f"📁 Sonuçlar başarıyla CSV dosyasına kaydedildi: {csv_path}")
