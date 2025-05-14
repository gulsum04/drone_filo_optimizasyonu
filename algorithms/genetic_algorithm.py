import random
from deap import base, creator, tools

def optimize_routes(drones, deliveries):
    creator.create("FitnessMin", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initRepeat, creator.Individual, lambda: random.choice(drones).id, n=len(deliveries))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_func(individual):
        total_energy = 0
        penalty = 0
        for i, drone_id in enumerate(individual):
            drone = next(d for d in drones if d.id == drone_id)
            delivery = deliveries[i]
            if delivery.weight > drone.max_weight:
                penalty += 1000
            else:
                dist = ((drone.start_pos[0] - delivery.pos[0])**2 + (drone.start_pos[1] - delivery.pos[1])**2)**0.5
                total_energy += dist * delivery.weight
        return 1.0 / (1 + total_energy + penalty),

    toolbox.register("evaluate", eval_func)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=20)
    for _ in range(40):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid)
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring

    best = tools.selBest(pop, 1)[0]
    return best
