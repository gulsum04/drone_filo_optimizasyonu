import random
from graph import delivery_cost
from csp import is_valid_assignment

def calculate_fitness(drone, route, deliveries, zones):
    pos = drone.start_pos
    battery = 0
    completed = 0
    violations = 0
    for i in route:
        d = next((x for x in deliveries if x.id == i), None)
        if is_valid_assignment(drone, d, pos, battery, zones):
            cost = delivery_cost(pos, d)
            battery += cost
            pos = d.pos
            completed += 1
        else:
            violations += 1
    return (completed * 50) - (battery * 0.1) - (violations * 1000)

def crossover(p1, p2):
    size = len(p1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None]*size
    child[start:end] = p1[start:end]
    pointer = 0
    for gene in p2:
        if gene not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = gene
    return child

def mutate(route, rate=0.1):
    for i in range(len(route)):
        if random.random() < rate:
            j = random.randint(0, len(route)-1)
            route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(drone, deliveries, zones, gen=50, pop_size=20):
    ids = [d.id for d in deliveries]
    pop = [random.sample(ids, len(ids)) for _ in range(pop_size)]
    for _ in range(gen):
        scores = [calculate_fitness(drone, r, deliveries, zones) for r in pop]
        best = [x for _, x in sorted(zip(scores, pop), reverse=True)][:10]
        new_gen = best.copy()
        while len(new_gen) < pop_size:
            p1, p2 = random.sample(best, 2)
            c = crossover(p1, p2)
            new_gen.append(mutate(c))
        pop = new_gen
    final = max(pop, key=lambda r: calculate_fitness(drone, r, deliveries, zones))
    return final, calculate_fitness(drone, final, deliveries, zones)
