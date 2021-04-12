from src.Helpers import get_min_index
from src.GA import GA
from src.SGO import SGO
from src.Clusters import Clusters
from src.Logger import log

if __name__ == "__main__":

    n = int(input("Number of cluster nodes : "))
    cluster = Clusters(N=n)
    candidate_nodes = cluster.run_workflow()
    log(candidate_nodes)

    sgo_obj = SGO(n, cluster.cluster_head_count, cluster)

    stopping_criteria = int(input("Enter number of rounds for stopping criteria : "))
    sgo_solution = sgo_obj.iterate(stopping_criteria=stopping_criteria)

    print(f"SGO Solution : {sgo_solution}")

    ga_obj = GA(n, cluster.cluster_head_count, cluster)
    ga_solution = ga_obj.iterate(stopping_fitness=sgo_obj._fitness_vector[get_min_index(sgo_obj._fitness_vector)])

    print(f"GA Solution : {ga_solution}")