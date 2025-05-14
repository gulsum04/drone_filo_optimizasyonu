import math

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def delivery_cost(start_pos, delivery):
    dist = euclidean_distance(start_pos, delivery.pos)
    return dist * delivery.weight + delivery.priority * 100

def build_adjacency_list(deliveries):
    graph = {d.id: [] for d in deliveries}
    for i in range(len(deliveries)):
        for j in range(len(deliveries)):
            if i != j:
                d1 = deliveries[i]
                d2 = deliveries[j]
                cost = delivery_cost(d1.pos, d2)
                graph[d1.id].append((d2.id, cost))
    return graph

def print_graph(graph):
    for node, edges in graph.items():
        print(f"Teslimat {node} -> ", end="")
        for neighbor, cost in edges:
            print(f"({neighbor}, maliyet={cost:.2f})", end=" ")
        print()
