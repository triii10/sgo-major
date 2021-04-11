from math import ceil, dist, floor
from random import choice, random, uniform
import matplotlib.pyplot as plt

from sklearn.utils import gen_batches
from src.Helpers import get_min_index, normalizer

from src.Logger import log

class SGO:
    """
    This class contains contains modules to implement the SGO algoritm on the clusters
    """
    def __init__(self, nclusters, nodes, cluster_obj) -> None:
        self._nclusters = nclusters
        self._nodes = nodes
        self._cluster = cluster_obj
        self._population = None
        self._gbest_pop = None
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

    def _calculate_X_new(self, x_old, g_best_pop_val):
        """
        Calculate the new X value
        """        
        c_val = 0.2
        r_val = random()

        return (c_val*x_old) + (r_val*(g_best_pop_val - x_old))

    def _calculate_gbest(self):
        """
        Identify the gbest and initialize the gbest object with population
        """
        gbest_index = get_min_index(self._fitness_vector)
        self._gbest_pop = self._population[gbest_index]

    def improve_phase(self):
        log("------IMPROVING PHASE-------")
        """
        Perform the improving phase and return the new matrix
        """

        new_fitness_vector = []
        new_population = []

        for (i, row) in enumerate(self._population):
            log(f"Improve Phase for row {i}")
            new_row = []

            # Calculating new X value for row i
            for val, g_best_pop_val in zip(row, self._gbest_pop):
                new_row.append(min(abs(self._calculate_X_new(val, g_best_pop_val)), 1))

            new_row_fitness = self._calculate_fitness_of_row(self._generate_cluster_heads(row=new_row))
            if new_row_fitness < self._fitness_vector[i]:
                new_fitness_vector.append(new_row_fitness)
                new_population.append(new_row)
            else: 
                new_fitness_vector.append(self._fitness_vector[i])
                new_population.append(row)

        # Reinitalize the fitness vector and the population 
        self._fitness_vector = new_fitness_vector
        self._population = new_population
    
    def acquiring_phase(self):
        log("------ACQUIRING PHASE-------")
        """
        Perform the acquiring phase step of SGO algorithm
        """

        for i in range(self._nodes):
            X_r_index = choice([x for x in range(self._nodes) if x != i])

            r1_val = uniform(0, 1)
            r2_val = uniform(0, 1)

            x_new = []
            if self._fitness_vector[X_r_index] < self._fitness_vector[i]:
                for x, x_r, x_gbest in zip(self._population[i], self._population[X_r_index], self._gbest_pop):
                    x_new.append(min(abs(x + (r1_val * (x_r-x)) + (r2_val * (x_gbest - x))), 1))
            
            else:
                for x, x_r, x_gbest in zip(self._population[i], self._population[X_r_index], self._gbest_pop):
                    x_new.append(min(abs(x + (r1_val * (x-x_r)) + (r2_val * (x_gbest - x))), 1))

            new_fitness_of_row = self._calculate_fitness_of_row(self._generate_cluster_heads(x_new))
            if new_fitness_of_row < self._fitness_vector[i]:
                self._fitness_vector[i] = new_fitness_of_row
                self._population[i] = x_new

    def iterate(self, stopping_criteria):
        """
        Interate over the steps of SGO until the stopping criteria has been met
        """
        self._initialize_population()
        self._generate_fitness_vector()
        self._calculate_gbest()
        for i in range(stopping_criteria):

            # Perform the improving phase
            self.improve_phase()
            self._calculate_gbest()

            # Perform the acquring phase
            self.acquiring_phase()
            self._calculate_gbest()

            # Plot the fitness value of the gbest of the iteration
            plt.plot([i], [self._calculate_fitness_of_row(self._generate_cluster_heads(self._gbest_pop))], 'ro')
            
        # The solution is generated by the best population 
        plt.savefig("images/Fitness_vs_Iterations.jpg")
        solution = self._generate_cluster_heads(self._gbest_pop)
        return solution 