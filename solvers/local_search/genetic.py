import random
from utils.helpers import goal_state, find_blank, swap, heuristic

def genetic_algorithm(start_state, population_size=100, max_generations=1000, mutation_rate=0.1):
    def apply_moves(state, moves):
        current_state = [row[:] for row in state]
        for move in moves:
            x, y = find_blank(current_state)
            if move == "RIGHT" and y + 1 < 3:
                current_state = swap(current_state, x, y, x, y + 1)
            elif move == "DOWN" and x + 1 < 3:
                current_state = swap(current_state, x, y, x + 1, y)
            elif move == "LEFT" and y - 1 >= 0:
                current_state = swap(current_state, x, y, x, y - 1)
            elif move == "UP" and x - 1 >= 0:
                current_state = swap(current_state, x, y, x - 1, y)
        return current_state

    def fitness(moves):
        result_state = apply_moves(start_state, moves)
        return heuristic(result_state)

    def generate_individual(length):
        moves = ["RIGHT", "DOWN", "LEFT", "UP"]
        return [random.choice(moves) for _ in range(length)]

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(individual):
        moves = ["RIGHT", "DOWN", "LEFT", "UP"]
        if random.random() < mutation_rate:
            mutate_point = random.randint(0, len(individual) - 1)
            individual[mutate_point] = random.choice(moves)
        return individual

    def convert_to_path(moves):
        current_state = [row[:] for row in start_state]
        path = []
        for move in moves:
            x, y = find_blank(current_state)
            if move == "RIGHT" and y + 1 < 3:
                new_x, new_y = x, y + 1
            elif move == "DOWN" and x + 1 < 3:
                new_x, new_y = x + 1, y
            elif move == "LEFT" and y - 1 >= 0:
                new_x, new_y = x, y - 1
            elif move == "UP" and x - 1 >= 0:
                new_x, new_y = x - 1, y
            else:
                continue
            current_state = swap(current_state, x, y, new_x, new_y)
            path.append((move, (x, y), (new_x, new_y)))
        return path

    individual_length = 20
    population = [generate_individual(individual_length) for _ in range(population_size)]

    for generation in range(max_generations):
        population_with_fitness = [(ind, fitness(ind)) for ind in population]
        population_with_fitness.sort(key=lambda x: x[1])

        best_individual, best_fitness = population_with_fitness[0]
        if apply_moves(start_state, best_individual) == goal_state:
            return convert_to_path(best_individual)

        elite_size = population_size // 2
        new_population = [ind for ind, _ in population_with_fitness[:elite_size]]

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(new_population, 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

    best_individual = population_with_fitness[0][0]
    return convert_to_path(best_individual)