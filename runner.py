from algorithm import run_algorithm
from src.Clusters import Clusters
from src.Logger import log

if __name__ == "__main__":

    n = int(input("Number of cluster nodes : "))
    cluster = Clusters(N=n)
    candidate_nodes = cluster.run_workflow()
    log(candidate_nodes)

    src, dest = 0, 10
    run_algorithm(src, dest)

