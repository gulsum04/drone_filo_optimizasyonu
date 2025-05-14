import heapq
from graph import euclidean_distance, delivery_cost
from csp import is_inside_no_fly

def heuristic(current_pos, goal_pos, zones):
    base = euclidean_distance(current_pos, goal_pos)
    penalty = 1000 if is_inside_no_fly(goal_pos, zones) else 0
    return base + penalty

def a_star(drone, deliveries, no_fly_zones):
    open_set = []
    heapq.heappush(open_set, (0, drone.start_pos, [], 0))
    while open_set:
        cost_so_far, current_pos, path, used_battery = heapq.heappop(open_set)
        if len(path) == len(deliveries):
            return path, cost_so_far
        for d in deliveries:
            if d.id not in path:
                cost = delivery_cost(current_pos, d)
                battery_cost = cost
                if used_battery + battery_cost > drone.battery or d.weight > drone.max_weight:
                    continue
                heur = heuristic(d.pos, d.pos, no_fly_zones)
                total_cost = cost_so_far + cost + heur
                new_path = path + [d.id]
                heapq.heappush(open_set, (total_cost, d.pos, new_path, used_battery + battery_cost))
    return [], float('inf')
