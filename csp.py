from graph import euclidean_distance

def is_inside_no_fly(pos, zones):
    for zone in zones:
        xs = [x for x, y in zone.coordinates]
        ys = [y for x, y in zone.coordinates]
        if min(xs) <= pos[0] <= max(xs) and min(ys) <= pos[1] <= max(ys):
            return True
    return False

def is_valid_assignment(drone, delivery, current_pos, used_battery, no_fly_zones):
    if delivery.weight > drone.max_weight:
        return False
    dist = euclidean_distance(current_pos, delivery.pos)
    battery_cost = dist * delivery.weight
    if used_battery + battery_cost > drone.battery:
        return False
    if is_inside_no_fly(delivery.pos, no_fly_zones):
        return False
    return True
