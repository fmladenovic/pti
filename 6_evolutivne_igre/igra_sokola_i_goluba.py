import math
from random import randint
import matplotlib.pyplot as plt


PIGEON = 'pigeon'
FALCON = 'falcon'

V = 4.0
C = 5.0

POPULATION_SIZE = 100
PIGEON_PERCENTAGE = 0.3
FALCON_PERCENTAGE = 1.0 - PIGEON_PERCENTAGE
ROUNDS = 1000
POPULATION_ROTATIONS = 100

INDIVIDUALS_REMOVE_PERCENTAGE = 0.2 # x 2 from top to cross for new individuals


class Individual: 
    def __init__(self, strategy, reverds = []):
        self.strategy = strategy
        self.reverds = reverds

    def reverds_sum(self):
        return sum(self.reverds)

    def play_vs(self, individual ):
        if self.strategy == PIGEON and individual.strategy == FALCON:
            self.reverds.append(0)
            individual.reverds.append(V)
        elif self.strategy == FALCON and individual.strategy == PIGEON:
            self.reverds.append(V)
            individual.reverds.append(0)
        elif self.strategy == PIGEON and individual.strategy == PIGEON:
            self.reverds.append(V/2)
            individual.reverds.append(V/2)
        elif self.strategy == FALCON and individual.strategy == FALCON:
            fight = randint(0,1)
            self.reverds.append(V if fight == 0 else -C)
            individual.reverds.append(V if fight == 1 else -C)

        

class PopulationWrapper:
    def __init__(self, population_size, pigeon_percentage, falcon_percentage, individuals_remove_percentage):
        self.population_size = population_size
        self.population = self._generate_first_population(pigeon_percentage, falcon_percentage)

        self.individuals_remove_percentage = individuals_remove_percentage

    def _generate_first_population( self, pigeon_percentage, falcon_percentage ):
        population = []
        for _ in range( math.ceil(pigeon_percentage * self.population_size)): 
            population.append( Individual(PIGEON, []) )
        for _ in range(math.ceil(falcon_percentage * self.population_size)): 
            population.append( Individual(FALCON, []) )
        return population

    def _reverds_sum_from_individual(self, individual ):
        return individual.reverds_sum()

    def _sort_individuals(self):
        self.population.sort(key = self._reverds_sum_from_individual, reverse=True)

    
    def remove_worst_individuals(self):
        self._sort_individuals()
        self.population = self.population[:math.ceil((1 - self.individuals_remove_percentage) * self.population_size) ]

    def _get_individuals_for_cross(self):
        self._sort_individuals()
        return self.population[:math.ceil(( self.individuals_remove_percentage * 2) * self.population_size)]

    def _cross_individuals(self, parent1, parent2):
        if parent1.strategy != parent2.strategy:
            strategy = PIGEON if randint(0,1) == 1 else FALCON
        else:
            strategy = parent1.strategy

        return Individual(strategy, [(parent1.reverds_sum() + parent2.reverds_sum())/2])


    def cross_best_individuals(self):
        for_cross = self._get_individuals_for_cross()
        i = 0
        j = len(for_cross) - 1
        while True:
            parent1 = for_cross[i]
            parent2 = for_cross[j]
            self.population.append(self._cross_individuals(parent1, parent2))
            i+=1
            j-=1
            if i > j:
                break

    def pigeon_proportion(self):
        count = 0
        for individual in self.population:
            if individual.strategy == PIGEON:
                count += 1
        pigeon_percentage =  count / len(self.population)
        return pigeon_percentage


class Game:
    def __init__(self, population_wrapper, rounds, population_rotations):
        self.rounds = rounds
        self.population_wrapper = population_wrapper
        self.population_proportions = []
        self.population_rotations = population_rotations

    def play(self):

        for _ in range( self.population_rotations ):
            self.population_proportions.append(self.population_wrapper.pigeon_proportion())
            for _ in range(self.rounds):
                for (i, individual) in enumerate(self.population_wrapper.population):
                    random_individual_i = randint(0, len(self.population_wrapper.population)- 1)
                    while random_individual_i == i:
                        random_individual_i = randint(0, len(self.population_wrapper.population)- 1)
                    random_individual = self.population_wrapper.population[random_individual_i]
                    individual.play_vs(random_individual)

            self.population_wrapper.remove_worst_individuals()
            self.population_wrapper.cross_best_individuals()

    def plot(self):
        excluded_last = len(self.population_proportions) - 2
        xs = self.population_proportions[:excluded_last]
        ys = [0] * excluded_last

        plt.suptitle('Percentage of individuals in population which play strategy PIGEON')    
        plt.xlabel('PIGEON percentage')
        plt.plot( xs, ys, 'rx')
        plt.plot( game.population_proportions[-1], 0, 'bo')
        plt.show()

game = Game( PopulationWrapper(POPULATION_SIZE, PIGEON_PERCENTAGE, FALCON_PERCENTAGE, INDIVIDUALS_REMOVE_PERCENTAGE), ROUNDS, POPULATION_ROTATIONS )
game.play()
game.plot()
