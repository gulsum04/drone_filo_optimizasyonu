import sys
import os
import time
import heapq

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.a_star import a_star
from algorithms.constraint_solver import csp_assignments_multi
from models.drone import Drone
from models.teslimat import Teslimat
from models.noflyzone import NoFlyZone
from utils.visualizer import plot_routes
from utils.time_utils import is_time_valid, time_to_minutes

def test_senaryo3():
    print("🚀 Senaryo 3: CSP + A*")
    start_time = time.time()

    current_time = "10:00"
    current_min = time_to_minutes(current_time)
    SARJ_LIMIT = 30
    SARJ_SURESI = 20

    drones = [Drone(i, max_weight=5.0, battery=100, speed=10.0, start_pos=(0, 0)) for i in range(5)]
    deliveries = [
        Teslimat(i, pos=(i*3, (i % 5)*4), weight=1.0 + (i % 2), priority=(i % 5) + 1, time_window=("09:00", "11:00"))
        for i in range(10)
    ]
    no_fly_zones = [
        NoFlyZone(0, coordinates=[(10, 10), (15, 10), (15, 15), (10, 15)], active_time=("09:00", "12:00"))
    ]

    assignments_list = csp_assignments_multi(drones, deliveries, no_fly_zones, current_time=current_time)
    end_time = time.time()

    if not assignments_list or len(assignments_list[0]) == 0:
        print("❌ Uygun drone-teslimat eşleşmesi bulunamadı.")
        return

    assignments = assignments_list[0]

    # 📌 Min-Heap kullanarak öncelikli teslimatları sırala (priority büyük olan önce)
    heap = []
    for delivery_id, drone_id in assignments.items():
        delivery = next((d for d in deliveries if d.id == delivery_id), None)
        if delivery:
            heapq.heappush(heap, (-delivery.priority, delivery_id, drone_id))  # eksiyle büyükten küçüğe

    print("📦 Öncelikli teslimat sırasına göre atamalar:")
    routes = []
    success = 0
    total_energy = 0
    total_charging_time = 0

    while heap:
        _, delivery_id, drone_id = heapq.heappop(heap)
        drone = next((d for d in drones if d.id == drone_id), None)
        delivery = next((d for d in deliveries if d.id == delivery_id), None)

        if drone and delivery:
            route, energy = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, no_fly_zones, current_min)
            if not route:
                print(f"Teslimat {delivery.id} → Drone {drone.id} ❌ Rota bulunamadı")
                continue

            if drone.battery - energy < SARJ_LIMIT:
                print(f"🔋 Drone {drone.id} batarya yetersiz ({drone.battery:.2f}), şarj ediliyor.")
                drone.battery = 100
                current_min += SARJ_SURESI
                total_charging_time += SARJ_SURESI

            drone.battery -= energy
            drone.start_pos = delivery.pos
            routes.append(route)
            total_energy += energy
            success += 1
            print(f"Teslimat {delivery.id} → Drone {drone.id} ✅ Enerji: {energy:.2f}")

    score = success * 100 - total_energy - total_charging_time
    duration = end_time - start_time

    print("\n📊 METRİK ÖZETİ SENARYO 3")
    print(f"✅ Başarılı teslimat: {success} / {len(assignments)}")
    print(f"⚡ Toplam enerji tüketimi: {total_energy:.2f}")
    print(f"🔋 Toplam şarj süresi: {total_charging_time} dk")
    print(f"🏁 Skor: {round(score, 2)}")
    print(f"⏱️ CSP + A* çözüm süresi: {duration:.2f} saniye")

    print("📍 Rotalar görselleştiriliyor...")
    plot_routes(drones, deliveries, no_fly_zones, show=True)

if __name__ == "__main__":
    test_senaryo3()
