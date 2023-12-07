import numpy
from SA import simulated_annealing
from main import generate_rand_N
from GA import *

def HGASA(grid, difficulty):
    initial = read_puzzle(grid)
    population = make_population(POPULATION, initial)

    iterations = 0  # Initialize iteration counter

    for _ in range(REPETITION):
        iterations += 1  # Increment iteration counter for each generation

        mating_pool = r_get_mating_pool(population)
        rndm.shuffle(mating_pool)
        population = get_offsprings(mating_pool, initial, PM, PC)
        fit = [get_fitness(c) for c in population]
        m = max(fit)
        # arbitrary m fitness (adjusted to be quadratic due to nature of GA)
        if m > ((difficulty * 10) ** 2) / -2:
            m = max([get_fitness(c) for c in population])
            for c in population:
                if get_fitness(c) == m:
                    print(c)
                    x, iter2 = simulated_annealing(numpy.array(c))
                    return x, iterations + iter2

    return population, iterations

N = generate_rand_N(1, .3)
for i in N:
    print(HGASA(i, .3))
