import time
from data_generator import generate_drones, generate_deliveries, generate_no_fly_zones
from astar import a_star
from genetic_algorithm import genetic_algorithm
from visualization import draw_combined_routes
from graph import build_adjacency_list, print_graph
from csp import is_valid_assignment

def main():
    print("🚀 Drone Teslimat Optimizasyon Sistemi Başlatılıyor...\n")

    drones = generate_drones(1)
    deliveries = generate_deliveries(5)
    no_fly_zones = generate_no_fly_zones(1)
    drone = drones[0]

    print("📍 Drone Bilgisi:")
    print(vars(drone))
    print("\n📦 Teslimat Noktaları:")
    for d in deliveries:
        print(vars(d))
    print("\n🚫 No-Fly Zone'lar:")
    for z in no_fly_zones:
        print(vars(z))

    print("\n🗺️ Teslimat Grafı:")
    graph = build_adjacency_list(deliveries)
    print_graph(graph)

    # A* hesapla
    print("\n🧠 A* Algoritması Çalışıyor...")
    start_time = time.time()
    astar_route, astar_cost = a_star(drone, deliveries, no_fly_zones)
    astar_time = time.time() - start_time
    print(f"✅ A* Tamamlanan: {len(astar_route)} | 💰 Maliyet: {astar_cost:.2f} | ⏱️ Süre: {astar_time:.3f} sn")

    # GA hesapla
    print("\n🧬 Genetik Algoritma Çalışıyor...")
    start_time = time.time()
    ga_route, ga_score = genetic_algorithm(drone, deliveries, no_fly_zones)
    ga_time = time.time() - start_time
    ga_completed = sum(
        1 for i in ga_route if is_valid_assignment(
            drone,
            next((d for d in deliveries if d.id == i), None),
            drone.start_pos,
            0,
            no_fly_zones
        )
    )
    print(f"✅ GA Tamamlanan: {ga_completed} | 💡 Skor: {ga_score:.2f} | ⏱️ Süre: {ga_time:.3f} sn")

    # Ortak görsel çizim (tek pencerede iki algoritma)
    draw_combined_routes(
        drone, deliveries, astar_route, ga_route, no_fly_zones,
        astar_info=f"A* Tamamlanan: {len(astar_route)} | Maliyet: {astar_cost:.2f} | Süre: {astar_time:.3f} sn",
        ga_info=f"GA Tamamlanan: {ga_completed} | Skor: {ga_score:.2f} | Süre: {ga_time:.3f} sn"
    )

if __name__ == "__main__":
    main()
