from utils.load_veri_seti import load_veri_seti
from algorithms.a_star import a_star
from utils.visualizer import plot_routes


def main():
    drones, deliveries, no_fly_zones = load_veri_seti("data/veri_seti.txt")

    for drone in drones:
        print(f"\n🚁 Drone {drone.id} için teslimat aranıyor...")
        for delivery in deliveries:
            if delivery.weight <= drone.max_weight and not delivery.assigned:
                print(f"  → Teslimat {delivery.id} deneniyor...")
                route, cost = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, no_fly_zones)
                if route:
                    print(f"    ✔ Teslimat {delivery.id} için rota bulundu.")
                    drone.route = route
                    delivery.assigned = True
                    break
                else:
                    print(f"    ❌ Rota bulunamadı.")
        else:
            print(f"⚠️ Drone {drone.id} için uygun teslimat bulunamadı.")

    plot_routes(drones, deliveries, no_fly_zones)

if __name__ == "__main__":
    main()
