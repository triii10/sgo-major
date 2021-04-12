from hashlib import new
from math import floor
from random import choice, uniform
from src.Logger import log
from src.Helpers import get_max_index, get_min_index, get_second_min_index, normalizer
import matplotlib.pyplot as plt 

class GA:
    """
    This class contains modules to implement the Genetic Algorithm algorithm on the cluster
    """

    def __init__(self, nclusters, nodes, cluster_obj) -> None:
        self._nclusters = nclusters
        self._nodes = nodes
        self._cluster = cluster_obj
        self._population = None
        self._fitness_vector = []
    
    def _initialize_population(self):
        """
        Initialize random initial population
        """
        init_population = []
        for i in range(self._nodes):
            row = []
            for j in range(self._nclusters):
                row.append(uniform(0, 1))
            init_population.append(row)
        self._population = init_population
        log(f"Population : {self._population}")

    def _generate_cluster_heads(self, row):
        """
        Generate the cluster heads from the population values
        """

        cluster_size = [len(value) for value in self._cluster.candidate_nodes.values()]
        cluster_heads = [min(floor(a * b), b-1) for a, b in zip(row, cluster_size)]
        
        log(f"Cluster Heads : {cluster_heads}")
        
        return cluster_heads
    
    def _generate_fitness_vector(self):
        """
        Generate the fitness vector and initialize it
        """

        for row in self._population:
            cluster_heads = self._generate_cluster_heads(row)
            fitness = self._calculate_fitness_of_row(cluster_heads)
            self._fitness_vector.append(fitness)

    def _calculate_fitness_of_row(self, cluster_heads):
        """
        Calculate the fitness value for a person in the population
        """
        x, y, z = 0.2, 0.3, 0.5

        dist1 = self._cluster.calculate_distance_1(cluster_heads)
        dist2 = self._cluster.calculate_distance_2(cluster_heads)
        energy_cluster = self._cluster.calculate_energy_consumed_for_cluster_nodes(cluster_heads)
        energy_cluster_head = self._cluster.calculate_energy_consumed_for_cluster_head(cluster_heads)

        total_energy = energy_cluster + energy_cluster_head

        dist1_norm = normalizer(dist1)
        dist2_norm = normalizer(dist2)
        total_energy_norm = normalizer(total_energy)

        log(f"Dist1_norm : {dist1_norm} Dist2_norm : {dist2_norm} Total_energy_norm : {total_energy_norm}")
        f = x*dist1_norm + y*dist2_norm + z*total_energy_norm

        log(f"Fitness value : {f}")
        return f

    def _add_offspring_to_population_and_death(self, offspring1, offspring2):
        """
        Add the offsprings generated to the population and update the fitness vector
        """

        death_index = get_max_index(self._fitness_vector)
        self._population.pop(death_index)
        self._fitness_vector.pop(death_index)
        
        death_index = get_max_index(self._fitness_vector)
        self._population.pop(death_index)
        self._fitness_vector.pop(death_index)
        
        self._population.append(offspring1)
        self._fitness_vector.append(self._calculate_fitness_of_row(self._generate_cluster_heads(offspring1)))

        self._population.append(offspring2)
        self._fitness_vector.append(self._calculate_fitness_of_row(self._generate_cluster_heads(offspring2)))

    def _get_fittest(self):
        return self._fitness_vector[get_min_index(self._fitness_vector)]

    def selection_crossover_mutation(self):
        """
        Perform the selection phase of GA
        """

        mutation_probability = 0.3
        log("------SELECTION PHASE-------")
        parent1 = self._population[get_min_index(self._fitness_vector)]
        parent2 = self._population[get_second_min_index(self._fitness_vector)]
        offspring1 = []
        offspring2 = []

        log("------CROSSOVER PHASE-------")
        crossover_point = choice([i for i in range(1, self._nclusters)])

        for i in range(self._nclusters):
            if i <= crossover_point:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])
            else:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])

        log("------MUTATION PHASE-------")
        if uniform(0, 1) >= mutation_probability:
            bit_mutate = [uniform(0, 1) for _ in range(self._nclusters)]
            new_offspring1 = []
            for index, j in enumerate(bit_mutate):
                if j >= mutation_probability:
                    new_offspring1.append(uniform(0, 1))
                else:
                    new_offspring1.append(offspring1[index])
            offspring1 = new_offspring1

        if uniform(0, 1) >= mutation_probability:
            bit_mutate = [uniform(0, 1) for _ in range(self._nclusters)]
            new_offspring2 = []
            for index, j in enumerate(bit_mutate):
                if j >= mutation_probability:
                    new_offspring2.append(uniform(0, 1))
                else:
                    new_offspring2.append(offspring2[index])
            offspring2 = new_offspring2

        self._add_offspring_to_population_and_death(offspring1=offspring1, offspring2=offspring2)

    def iterate(self, stopping_fitness=None, iterations=50):
        """
        Iterate over the steps of GA until ocnvergence
        """
        self._initialize_population()
        self._generate_fitness_vector()

        i = 0
        while stopping_fitness < self._get_fittest(): 
            self.selection_crossover_mutation()
            plt.plot(i, [self._get_fittest()], 'ro')
            i += 1

        plt.savefig("images/Fitness_vs_Iterations_GA.jpg")
        plt.close()
        solution = self._generate_cluster_heads(self._population[get_min_index(self._fitness_vector)])
        return solution