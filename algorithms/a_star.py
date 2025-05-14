import heapq
from utils.distance import distance_cost, euclidean

def a_star(start, goal, weight, priority, nfz_list):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        neighbors = generate_neighbors(current)

        for neighbor in neighbors:
            tentative_g = g_score[current] + distance_cost(current, neighbor, weight, priority)

            if in_noflyzone(neighbor, nfz_list):
                tentative_g += 10000  # No-fly zone cezası

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None  # Ulaşılamıyor

def generate_neighbors(pos):
    step = 10
    return [
        (pos[0] + step, pos[1]),
        (pos[0] - step, pos[1]),
        (pos[0], pos[1] + step),
        (pos[0], pos[1] - step),
    ]

def in_noflyzone(pos, nfz_list):
    for nfz in nfz_list:
        if is_inside_polygon(pos, nfz.coordinates):
            return True
    return False

def is_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    px1, py1 = polygon[0]
    for i in range(n+1):
        px2, py2 = polygon[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                        if px1 == px2 or x <= xinters:
                            inside = not inside
        px1, py1 = px2, py2
    return inside

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]
