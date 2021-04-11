from random import uniform

from Logger import log

class SGO:
    """
    This class contains contains modules to implement the SGO algoritm on the clusters
    """
    def __init__(self, nclusters, nodes, cluster_obj) -> None:
        self._nclusters = nclusters
        self._nodes = nodes
        self._cluster = cluster_obj
        self._cluster_heads = []
        self._population = None

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

        cluster_size = [len(value) for _, value in self._cluster.candidate_nodes.items()]
        cluster_heads = [a * b for a, b in zip(row, cluster_size)]
        
        log(f"Cluster Heads : {cluster_heads}")
        
        return cluster_heads

    def calculate_fitness(self):
        pass