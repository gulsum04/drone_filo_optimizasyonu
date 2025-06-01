import random
import heapq
from algorithms.a_star import a_star
from utils.time_utils import is_time_valid, time_to_minutes


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

        if not is_time_valid(current_time, delivery):
            penalty += 500

        route, energy = a_star(drone.start_pos, delivery.pos, delivery.weight, delivery.priority, no_fly_zones, current_time)
        if route:
            success_count += 1
            total_energy += energy
        else:
            penalty += 1000

    return success_count * 100 - total_energy - penalty


def generate_initial_population(drones, deliveries, no_fly_zones, size=10, current_time=0):
    population = []
    for _ in range(size):
        individual = []
        used_deliveries = set()

        # Önceliğe göre sıralama
        teslimat_heap = [(-d.priority, d) for d in deliveries if is_time_valid(current_time, d)]
        heapq.heapify(teslimat_heap)

        for drone in drones:
            while teslimat_heap:
                _, delivery = heapq.heappop(teslimat_heap)
                if delivery.weight <= drone.max_weight and delivery.id not in used_deliveries:
                    used_deliveries.add(delivery.id)
                    individual.append((drone.id, delivery.id))
                    break

        if individual:  # Boş değilse popülasyona ekle
            population.append(individual)

    return population


def mutate(individual, deliveries, drones, current_time=0):
    if not individual:
        return individual
    new_individual = individual.copy()
    i = random.randint(0, len(new_individual) - 1)
    drone_id, _ = new_individual[i]
    drone = next((d for d in drones if d.id == drone_id), None)
    if drone:
        mevcut_teslimatlar = [pair[1] for pair in new_individual]
        uygunlar = [(-d.priority, d) for d in deliveries if d.weight <= drone.max_weight and d.id not in mevcut_teslimatlar and is_time_valid(current_time, d)]
        if uygunlar:
            heapq.heapify(uygunlar)
            _, yeni_teslimat = heapq.heappop(uygunlar)
            new_individual[i] = (drone_id, yeni_teslimat.id)
    return new_individual


def crossover(parent1, parent2):
    if len(parent1) < 2 or len(parent2) < 2:
        return parent1, parent2
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


def optimize_routes(drones, deliveries, no_fly_zones, generations=50, population_size=10, current_time="10:00"):
    current_time = time_to_minutes(current_time) if isinstance(current_time, str) else current_time
    population = generate_initial_population(drones, deliveries, no_fly_zones, size=population_size, current_time=current_time)

    if not population or len(population[0]) < 2:
        print("⚠️ GA için uygun başlangıç popülasyonu üretilemedi.")
        return []

    for g in range(generations):
        fitness_scores = [(ind, fitness(ind, drones, deliveries, no_fly_zones, current_time)) for ind in population]
        fitness_scores.sort(key=lambda x: -x[1])
        best_score = fitness_scores[0][1]
        print(f"🧬 Jenerasyon {g + 1}: En iyi skor = {best_score:.2f}")
        population = [ind for ind, _ in fitness_scores]

        new_population = population[:2]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:5], 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, deliveries, drones, current_time))
            if len(new_population) < population_size:
                new_population.append(mutate(child2, deliveries, drones, current_time))

        population = new_population

    for individual in population:
        if is_valid(individual):
            return individual
    return population[0]
