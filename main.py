"""
We will be using a genetic algorithm to solve the knapsack problem! 
The Knapsack Problem is a classic optimization challenge: given items 
with weights and values, select a subset to maximize total value within a 
fixed weight capacity, deciding whether to take an item or leave it (0/1) 
or take fractions (Fractional Knapsack)
"""

from typing import Callable, List
from random import choices
from collections import namedtuple  


Genome = List[int] # induviduals, represented as lists of 0s and 1s
Population = List[Genome] # one population is a list of genomes!
Thing = namedtuple("Thing", ["name", "value", "weight"]) # Thing(value, weight)
FitnessFunc = Callable[[Genome], int] # a function that takes a genome and returns an int (fitness score)

things = [
    Thing('Laptop',value=500, weight=2200), 
    Thing('Headphones', value=150, weight=160),
    Thing('Coffee Mug', value=60, weight=350),
    Thing('Notepad', value=40, weight=333),
    Thing('Water Bottle', value=30, weight=192),
    ]

def generate_genome(length: int) -> Genome: 
    # generates a random genome made of 0s and 1s, and a given length
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    # generates a population of given size, each genome having the given length
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome: Genome, things: List[Thing], weight_limit: int) -> int:
    # calculates the fitness of a genome based on the things and weight limit
    if len(genome) != len(things):
        raise ValueError("Genome length and number of things must be the same")
    weight = 0 
    value = 0 

    for i, thing in enumerate(things): 
        # a genetic sequence will determine whether we include a thing or not! 
        if genome[i] == 1: # if the gene is 1, we include the thing
            weight += thing.weight
            value += thing.value
            if weight > weight_limit: # if we exceed the weight limit, return 0
                return 0
    return value

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
   # randomly select two genomes, with the fitter genomes having a higher chance of being choosen (aka, parents for crossover)
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],# build a list of fitness scores for each genome
        k=2 
    )  
