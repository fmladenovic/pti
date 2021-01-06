import math
from random import randint
import matplotlib.pyplot as plt


PAPER = 'paper'
ROCK = 'rock'
SCISSORS = 'scissors'

PAPER_PERCENTAGE = 0.6
ROCK_PERCENTAGE = 0.2
SCISSORS_PERCENTAGE = 1 - PAPER_PERCENTAGE - ROCK_PERCENTAGE

POPULATION_SIZE = 100
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
        if self.strategy == PAPER and individual.strategy == PAPER:
            self.reverds.append(0)
            individual.reverds.append(0)
        elif self.strategy == PAPER and individual.strategy == ROCK:
            self.reverds.append(1)
            individual.reverds.append(-1)
        elif self.strategy == PAPER and individual.strategy == SCISSORS:
            self.reverds.append(-1)
            individual.reverds.append(1)

        elif self.strategy == ROCK and individual.strategy == PAPER:
            self.reverds.append(-1)
            individual.reverds.append(1)
        elif self.strategy == ROCK and individual.strategy == ROCK:
            self.reverds.append(0)
            individual.reverds.append(0)
        elif self.strategy == ROCK and individual.strategy == SCISSORS:
            self.reverds.append(1)
            individual.reverds.append(-1)

        elif self.strategy == SCISSORS and individual.strategy == PAPER:
            self.reverds.append(1)
            individual.reverds.append(-1)
        elif self.strategy == SCISSORS and individual.strategy == ROCK:
            self.reverds.append(-1)
            individual.reverds.append(1)
        elif self.strategy == SCISSORS and individual.strategy == SCISSORS:
            self.reverds.append(0)
            individual.reverds.append(0)

        

class PopulationWrapper:
    def __init__(self, population_size, paper_percentage, rock_percentage, scissors_percentage, individuals_remove_percentage):
        self.population_size = population_size
        self.population = self._generate_first_population(paper_percentage, rock_percentage, scissors_percentage)

        self.individuals_remove_percentage = individuals_remove_percentage

    def _generate_first_population( self, paper_percentage, rock_percentage, scissors_percentage ):
        population = []
        for _ in range( math.ceil(paper_percentage * self.population_size)): 
            population.append( Individual(PAPER, []) )
        for _ in range(math.ceil(rock_percentage * self.population_size)): 
            population.append( Individual(ROCK, []) )
        for _ in range(math.ceil(scissors_percentage * self.population_size)): 
            population.append( Individual(SCISSORS, []) )
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

        if  randint(0, 3) == 0:
            strategy = [ el for el in [PAPER, ROCK, SCISSORS] if el != parent1.strategy and el != parent2.strategy ][0] # mutation in 25%
        else: 
            if parent1.strategy != parent2.strategy:
                strategy = parent1.strategy if randint(0,1) == 1 else parent2.strategy
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

    def population_proportion(self):
        count_paper = 0
        count_rock = 0
        for individual in self.population:
            if individual.strategy == PAPER:
                count_paper += 1
            if individual.strategy == ROCK:
                count_rock += 1
        paper_percentage =  count_paper / len(self.population)
        rock_percentage =  count_rock / len(self.population)

        return paper_percentage, rock_percentage


class Game:
    def __init__(self, population_wrapper, rounds, population_rotations):
        self.rounds = rounds
        self.population_wrapper = population_wrapper
        self.population_proportions = []
        self.population_rotations = population_rotations

    def play(self):

        for _ in range( self.population_rotations ):
            self.population_proportions.append(self.population_wrapper.population_proportion())
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

        plt.suptitle('Percentage of individuals in population per strategy')    
        plt.xlabel('PAPER percentage')
        plt.ylabel('ROCK percentage')

        excluded_last = len(self.population_proportions) - 2

        xs = [ el[0] for el in self.population_proportions[:excluded_last] ]
        ys = [ el[1] for el in self.population_proportions[:excluded_last] ]

        last_x = [ self.population_proportions[-1][0] ]
        last_y = [ self.population_proportions[-1][1] ]

        plt.plot(xs, ys, 'rx')
        plt.plot(last_x, last_y, 'bo')

        plt.plot([0, 0, 1, 0], [0, 1, 0, 0])
        plt.show()

game = Game( PopulationWrapper(POPULATION_SIZE, PAPER_PERCENTAGE, ROCK_PERCENTAGE, SCISSORS_PERCENTAGE, INDIVIDUALS_REMOVE_PERCENTAGE), ROUNDS, POPULATION_ROTATIONS )
game.play()
game.plot()
