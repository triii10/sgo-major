from src.SGO import SGO
from algorithm import run_algorithm
from src.Clusters import Clusters
from src.Logger import log

if __name__ == "__main__":

    n = int(input("Number of cluster nodes : "))
    cluster = Clusters(N=n)
    candidate_nodes = cluster.run_workflow()
    log(candidate_nodes)

    sgo_obj = SGO(n, cluster.cluster_head_count, cluster)

    stopping_criteria = int(input("Enter number of rounds for stopping criteria : "))
    solution = sgo_obj.iterate(stopping_criteria=stopping_criteria)

    print(f"Solution : {solution}")

