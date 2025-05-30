import random
from algorithms.a_star import a_star

def fitness(route_set, drones, deliveries, no_fly_zones, current_time=0):
    success_count = 0
    total_energy = 0
    penalty = 0

    for drone_id, delivery_id in route_set:
        drone = next((d for d in drones if d.id == drone_id), None)
        delivery = next((d for d in deliveries if d.id == delivery_id), None)

        if drone is None or delivery is None:
            penalty += 1000
            continue

        route, energy = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, no_fly_zones, current_time)

        if route:
            success_count += 1
            total_energy += energy
        else:
            penalty += 1000

    return success_count * 100 - total_energy - penalty

def generate_initial_population(drones, deliveries, no_fly_zones, size=10):
    population = []
    for _ in range(size):
        individual = []
        used_deliveries = set()
        for drone in drones:
            available = [d for d in deliveries if d.weight <= drone.max_weight and d.id not in used_deliveries]
            if available:
                chosen = random.choice(available)
                used_deliveries.add(chosen.id)
                individual.append((drone.id, chosen.id))
        population.append(individual)
    return population

def mutate(individual, deliveries, drones):
    if not individual:
        return individual

    new_individual = individual.copy()
    i = random.randint(0, len(new_individual) - 1)
    drone_id, _ = new_individual[i]
    drone = next((d for d in drones if d.id == drone_id), None)

    if drone:
        mevcut_teslimatlar = [pair[1] for pair in new_individual]
        uygunlar = [d for d in deliveries if d.weight <= drone.max_weight and d.id not in mevcut_teslimatlar]

        if uygunlar:
            yeni_teslimat = random.choice(uygunlar)
            new_individual[i] = (drone_id, yeni_teslimat.id)

    return new_individual

def crossover(parent1, parent2):
    point = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def is_valid(individual):
    seen = set()
    for _, delivery_id in individual:
        if delivery_id in seen:
            return False
        seen.add(delivery_id)
    return True

def optimize_routes(drones, deliveries, no_fly_zones, generations=50, population_size=10):
    population = generate_initial_population(drones, deliveries, no_fly_zones, size=population_size)
    for _ in range(generations):
        fitness_scores = [(ind, fitness(ind, drones, deliveries, no_fly_zones)) for ind in population]
        fitness_scores.sort(key=lambda x: -x[1])
        population = [ind for ind, _ in fitness_scores]

        new_population = population[:2]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:5], 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, deliveries, drones))
            if len(new_population) < population_size:
                new_population.append(mutate(child2, deliveries, drones))
        population = new_population

    # 🔒 Geçerli bir birey döndür (her teslimat bir drone'a ait olacak şekilde)
    for individual in population:
        if is_valid(individual):
            return individual

    # Hiçbiri geçerli değilse ilkini döndür
    return population[0]
