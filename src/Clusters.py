import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans
from math import sqrt
from src.Helpers import calculate_distance_from_base_station, calculate_euclidean_distance
from src.Logger import log
from random import choice 

class Clusters:

    def __init__(self, N=50) -> None:
        self.N = N
        self.data = None
        self.kmeans = None
        self.candidate_nodes = None
        self.cluster_head_count = None
        self.base_station = None

    def generate_random_data(self):
        """
        Generate some random data
        """
        log("Generating Random Data...")
        self.data = np.vstack(((np.random.randn(self.N - 25, 2) * 0.5 + np.array([1, 0])),
                        (np.random.randn(self.N - 15, 2) * 0.5 + np.array([1, 0])),
                        (np.random.randn(10, 2) * 0.5 + np.array([1, 0]))))
        self.base_station = np.random.randn(3)      # The dimensions are as x, y, z

    def display_random_plot(self):
        """
        Display the plot generated
        """
        log("Saving generated data to /images/random_data.jpg...")

        sns.set_style("darkgrid")
        ax = sns.scatterplot(x=self.data[:, 0], y=self.data[:, 1])
        ax.set_xlabel('X-Axis')
        ax.set_ylabel('Y-Axis')
        plt.savefig("images/random_data.jpg")
        plt.close()

    def generate_elbow(self):
        # Using K Means to find out the clusters

        log("Generate Graph for WCSS to find elbow point...")
        wcss = []
        for i in range(1, int(sqrt(self.N))):
            kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
            kmeans.fit(self.data)
            # inertia method returns wcss for that model
            wcss.append(kmeans.inertia_)

        plt.figure(figsize=(10,5))
        sns.lineplot(x=range(1, int(sqrt(self.N))), y=wcss,marker='o',color='red')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.savefig("images/elbow_method.jpg")
        plt.show()
        plt.close()

    def generate_cluster(self,nclusters = 3):

        log("Generate clusters on the dataset...")

        self.kmeans = KMeans(n_clusters = nclusters, init = 'k-means++', random_state = 42)
        self.kmeans.fit(self.data)

        y_kmeans = self.kmeans.fit_predict(self.data)

        candidate_nodes = {}
        for cluster in range(nclusters):
            candidate_nodes[f'cluster_{cluster}'] = self.data[y_kmeans == cluster]
        self.candidate_nodes = candidate_nodes

        plt.figure(figsize=(10,5))
        plt.xlabel('X-Axis')
        plt.ylabel('Y-Axis')
        for i in range(nclusters):
            sns.scatterplot(x=self.data[y_kmeans == i, 0], y=self.data[y_kmeans == i, 1], color = "#"+''.join(choice('0123456789ABCDEF') for j in range(6)), label = f'Cluster {i}',s=50)
        print(self.base_station)
        sns.scatterplot(x=[self.base_station[0]], y=[self.base_station[1]], color="#"+''.join(choice('0123456789ABCDEF') for j in range(6)), s=100, label='Base Station')
        log("Saving generated clusters to /images/cluster.jpg...")
        plt.savefig("images/cluster.jpg")
        plt.close()

    def run_workflow(self):
        self.generate_random_data()
        self.display_random_plot()
        self.generate_elbow()

        nclusters = int(input("Enter number of clusters : "))
        self.cluster_head_count = nclusters
        self.generate_cluster(nclusters=nclusters)
        self.return_candidate_nodes()
        
    def return_candidate_nodes(self):
        return self.candidate_nodes

    def calculate_distance_1(self, cluster_heads):
        """
        Calculate and return the the average distance 
        between a member cluster node to its cluster head node
        """

        dist1 = []
        for cluster_head, nodes in zip(cluster_heads, self.candidate_nodes.values()):
            total_dist = 0.0
            for obj in nodes:
                total_dist += calculate_euclidean_distance(nodes[cluster_head], obj)
            dist1.append(total_dist/len(nodes))

        log(f"Distance 1 : {dist1}")
        return max(dist1)

    def calculate_distance_2(self, cluster_heads):
        """
        Calculate and return the max distance between the cluster heads and base station
        """

        dist2 = []
        for cluster_head, nodes in zip(cluster_heads, self.candidate_nodes.values()):
            cluster_head_dim = nodes[cluster_head]
            dist2.append(calculate_distance_from_base_station(cluster_head_dim, self.base_station))

        log(f"Distance 2 : {dist2}")
        return max(dist2)
    
    def calculate_energy_consumed_for_cluster_nodes(self, cluster_heads, k_bits=200):
        """
        Calculate and return the total energy in a cluster
        """

        energy = 0.0
        nodes_list = self.candidate_nodes.values()
        for cluster_head, nodes in zip(cluster_heads, nodes_list):
            cluster_head_dim = nodes[cluster_head]
            for node in nodes:
                energy += (500*k_bits*k_bits*(calculate_euclidean_distance(cluster_head_dim, node)**2))/(pow(10, -24))

        log(f"Total Cluster Energy : {energy}")
        return energy

    def calculate_energy_consumed_for_cluster_head(self, cluster_heads, k_bits=200):
        """
        Calculate the energy consumed to transmit by cluster head to the base station
        """
        energy = 0.0

        node_list = self.candidate_nodes.values()
        for cluster_head, nodes in zip(cluster_heads, node_list):
            cluster_head_dim = nodes[cluster_head]
            energy += (50*0.0013*k_bits*k_bits*(calculate_distance_from_base_station(cluster_head_dim, self.base_station)**4))/(pow(10, -24))
        
        log(f"Total Cluster Head Energy : {energy}")
        return energy 
