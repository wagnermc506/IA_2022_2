"""
This code was taken from https://medium.com/turing-talks/turing-talks-8-algoritmos-gen%C3%A9ticos-a791c25bd7ba
"""

import numpy as np
import random
from chrome_trex import DinoGame

CHANCE_MUT = .20
CHANCE_CO = .20
NUM_INDIVIDUOS = 15
NUM_MELHORES = 3

NUM_GERACOES = 100

def generate_population(n):
    populacao = []
    for i in range(n):
        populacao.append(np.random.uniform(-10, 10, (3, 10)))
    return populacao

def action_values(indivual, state):
    return indivual @ state

def best_(individual, state):
    values = action_values(individual, state)
    return np.argmax(values)

def mutation(individual):
    for i in range(3):
        for j in range(10):
            if np.random.uniform(0, 1) < CHANCE_MUT:
                individual[i][j] *= np.random.uniform(-1.5, 1.5)

def crossover(individual1, individual2):
    filho = individual1.copy()
    for i in range(3):
        for j in range(10):
            if np.random.uniform(0, 1) < CHANCE_CO:
                filho[i][j] = individual2[i][j]
    return filho

def calcular_fitness(game, individual):
    game.reset()
    while not game.game_over:
        state = game.get_state()
        action = best_(individual, state)
        game.step(action)
    return game.get_score()

def sort_list(list_, sorting, dec=True):
    return [x for _, x in sorted(zip(sorting, list_), key=lambda p: p[0], reverse=dec)]

def next_gen(population, fitness):
    list_ = sort_list(population, fitness)
    next_ = list_[:NUM_MELHORES]

    while len(next_) < NUM_INDIVIDUOS:
        ind1, ind2 = random.choices(population, k=2)
        filho = crossover(ind1, ind2)
        mutation(filho)
        next_.append(filho)

    return next_

if __name__ == "__main__":
    game = DinoGame(fps=50_000)

    population = generate_population(NUM_INDIVIDUOS)

    for gen in range(NUM_GERACOES):
        fitness = []
        for ind in population:
            fitness.append(calcular_fitness(game, ind))

        population = next_gen(population, fitness)

    fitness = []
    for ind in population:
        fitness.append(calcular_fitness(game, ind))

    game.fps = 60
    list_ = sort_list(population, fitness)
    best = list_[0]
    print('Melhor individuo:', best)
    fit = calcular_fitness(game, best)
    print('Fitness: {:4.1f}'.format(game.get_score()))
