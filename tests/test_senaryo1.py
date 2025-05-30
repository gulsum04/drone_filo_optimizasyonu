import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.a_star import a_star
from utils.visualizer import plot_routes
from utils.load_veri_seti import load_veri_seti

drones, deliveries, no_fly_zones = load_veri_seti()

def test_senaryo1():
    print(f"\n🚀 Senaryo 1: A* Algoritması")
    print(f"Toplam {len(drones)} drone, {len(deliveries)} teslimat, {len(no_fly_zones)} no-fly zone mevcut.\n")

    for drone in drones:
        print(f"🔍 Drone {drone.id} teslimat arıyor...")
        for delivery in deliveries:
            if delivery.weight <= drone.max_weight and not delivery.assigned:
                print(f"  → Teslimat {delivery.id} deneniyor...")
                route, energy = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, no_fly_zones)
                if route:
                    print(f"    ✅ Rota bulundu! Teslimat {delivery.id} → Drone {drone.id} | Enerji: {energy:.2f}")
                    drone.route = route
                    delivery.assigned = True
                    break
                else:
                    print(f"    ❌ Rota bulunamadı.")
        else:
            print(f"⚠️ Uygun teslimat yok. Drone {drone.id} boşa çıktı.")

    plot_routes(drones, deliveries, no_fly_zones)

if __name__ == "__main__":
    test_senaryo1()
