from utils.time_utils import is_within_time_window
from algorithms.a_star import a_star

def solve_csp(drones, deliveries, nfzs, current_time=30):
    """
    Basit bir constraint satisfaction çözümü:
    - Her teslimatın zaman penceresine uygun olup olmadığı kontrol edilir.
    - Ağırlığı taşıyabilecek ve uygun olan dronlar belirlenir.
    - Her teslimat için en kısa rota (en az maliyetli) olan drone seçilir.
    """
    assignments = []

    for delivery in deliveries:
        if delivery.assigned:
            continue

        # Zaman penceresi kontrolü
        if not is_within_time_window(current_time, delivery.time_window):
            continue

        eligible_drones = []

        for drone in drones:
            if not drone.available or delivery.weight > drone.max_weight:
                continue

            # A* algoritması ile yol hesaplama
            route, cost = a_star(
                start=drone.start_pos,
                goal=delivery.pos,
                weight=delivery.weight,
                priority=delivery.priority,
                nfz_list=nfzs,
                current_time=current_time
            )

            if route:
                eligible_drones.append((drone, route, cost))

        if eligible_drones:
            # En az maliyetli (kısa) rotaya sahip drone seçilir
            best_drone, best_route, _ = min(eligible_drones, key=lambda x: x[2])
            best_drone.route = best_route
            best_drone.available = False
            assignments.append((best_drone.id, delivery.id))
            delivery.assigned = True

    return assignments
