import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.constraint_solver import solve_csp
from utils.visualizer import plot_routes
from utils.load_veri_seti import load_veri_seti

drones, deliveries, no_fly_zones = load_veri_seti()

def test_senaryo3():
    print(f"\n🧩 Senaryo 3: CSP (Constraint Solver)")
    print(f"Toplam {len(drones)} drone, {len(deliveries)} teslimat, {len(no_fly_zones)} no-fly zone mevcut.")
    print("⏱️ Simülasyon zamanı: 30. dakikada başlatılıyor.\n")

    assignments = solve_csp(drones, deliveries, no_fly_zones, current_time=30)

    if assignments:
        print("📋 Drone-Teslimat eşleştirmesi:")
        for d_id, deliv_id in assignments:
            print(f"📦 Drone {d_id} → Teslimat {deliv_id}")
    else:
        print("❌ Hiçbir eşleştirme yapılamadı.")

    plot_routes(drones, deliveries, no_fly_zones)

if __name__ == "__main__":
    test_senaryo3()
