from src.Helpers import get_adjacency_matrix
from src.Helpers import get_cost_matrix
from src.Helpers import get_time_matrix
from src.Helpers import generate_population
from src.Helpers import get_min_index
from src.Steps import calculate_next_hops
from src.Steps import calculate_next_phops
from src.Steps import fitness
from src.Steps import improve_phase
from src.Steps import acquiring_phase
from src.Logger import log
from matplotlib.pyplot import axes
import matplotlib.pyplot as plt
from copy import deepcopy

def run_algorithm(src, dest):

    nodes, adjacency_matrix = get_adjacency_matrix()
    time_matrix = get_time_matrix(nodes)
    cost_matrix = get_cost_matrix(nodes)

    solution = []

    terminate = 50
    run_step = 1
    
    init_population = generate_population(nodes)
    # print("init_population")
    # print(*init_population, sep='\n')
    phops, phops_modulus = calculate_next_phops(adjacency_matrix)
    init_fitness, g_best_pop = fitness(init_population, src, dest, cost_matrix, time_matrix, phops, phops_modulus)

    log("init_fitness : ", init_fitness)
    log("g_best_pop : ", g_best_pop)

    while(run_step <= terminate):

        log("{} : {}".format("Iteration", run_step))
        run_step += 1

        # print("#"*20, "Improving Phase", "#"*20)
        init_population, init_fitness = improve_phase(adjacency_matrix, init_population, g_best_pop, init_fitness, deepcopy(src), deepcopy(dest), cost_matrix, time_matrix, phops, phops_modulus)

        g_best_pop = init_population[get_min_index(init_fitness)]

        init_population, init_fitness = acquiring_phase(nodes, init_population, init_fitness, g_best_pop, src, dest, cost_matrix, time_matrix, phops, phops_modulus)

        _, solution = calculate_next_hops(g_best_pop, phops, phops_modulus)

        # print("Solution ", run_step-1, ": ")


        plt.plot([run_step-1], [init_fitness[get_min_index(init_fitness)]], 'ro')
        
        # print("Solution Fitness: ", g_best_pop)
    src_c, dest_c = deepcopy(src), deepcopy(dest)
    while src_c != dest_c:
        print(src_c, end=" -> ")
        src_c = solution[src_c]
    print(dest_c)
    plt.xlabel("Iterations")
    plt.ylabel("Fitness Value")
    plt.savefig("images/Iteration_vs_Fitness.jpg")
    plt.close()