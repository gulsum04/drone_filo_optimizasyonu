import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.genetic_algorithm import optimize_routes
from utils.load_veri_seti import load_veri_seti

#  Tüm verileri al (drones, deliveries, no_fly_zones)
drones, deliveries, no_fly_zones = load_veri_seti()

def test_senaryo2():
    print(f"\n🧬 Senaryo 2: Genetik Algoritma")
    print(f"Toplam {len(drones)} drone, {len(deliveries)} teslimat mevcut.\n")
    print("🔄 Optimizasyon başlatılıyor...")

    best_assignment = optimize_routes(drones, deliveries, no_fly_zones)

    print("\n📋 En iyi eşleştirme sonucu:")
    for i, (drone_id, delivery_id) in enumerate(best_assignment):
        print(f"📦 Teslimat {delivery_id} → Drone {drone_id}")

if __name__ == "__main__":
    test_senaryo2()
