import heapq
from utils.distance import distance_cost, euclidean

def a_star(start, goal, weight, priority, nfz_list, current_time=0):
    """
    A* algoritması ile en uygun rotayı bulur.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    iteration = 0
    MAX_ITER = 50000

    while open_set and iteration < MAX_ITER:
        iteration += 1
        _, current = heapq.heappop(open_set)

        if euclidean(current, goal) < 5:
            return reconstruct_path(came_from, current), g_score[current]

        neighbors = generate_neighbors(current)

        for neighbor in neighbors:
            tentative_g = g_score[current] + distance_cost(current, neighbor, weight, priority)

            penalty = 0
            if in_noflyzone(neighbor, nfz_list, current_time):
                penalty = 10000
                tentative_g += penalty  # g-score'a ceza

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean(neighbor, goal) + penalty  # heuristic + nofly penalty
                heapq.heappush(open_set, (f_score, neighbor))

    print(f"⚠️ A* ({start} → {goal}) maksimum iterasyona ulaştı.")
    return None, float('inf')


def generate_neighbors(pos):
    step = 5
    return [
        (pos[0] + step, pos[1]),
        (pos[0] - step, pos[1]),
        (pos[0], pos[1] + step),
        (pos[0], pos[1] - step),
        (pos[0] + step, pos[1] + step),
        (pos[0] - step, pos[1] - step),
        (pos[0] + step, pos[1] - step),
        (pos[0] - step, pos[1] + step),
    ]

def in_noflyzone(pos, nfz_list, current_time=0):
    """
    Pozisyon, aktif no-fly zone içindeyse True döner.
    """
    def time_to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    for nfz in nfz_list:
        if isinstance(nfz.active_time[0], str):
            start_min = time_to_minutes(nfz.active_time[0])
            end_min = time_to_minutes(nfz.active_time[1])
        else:
            start_min = nfz.active_time[0]
            end_min = nfz.active_time[1]

        if start_min <= current_time <= end_min:
            if is_inside_polygon(pos, nfz.coordinates):
                return True
    return False

def is_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    px1, py1 = polygon[0]
    for i in range(n + 1):
        px2, py2 = polygon[i % n]
        if y > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1 + 1e-9) + px1
                        if px1 == px2 or x <= xinters:
                            inside = not inside
        px1, py1 = px2, py2
    return inside

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]
