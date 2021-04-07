import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans
from math import sqrt
from src.Logger import log
from random import choice 

class Clusters:

    def __init__(self, N=50) -> None:
        self.N = N
        self.data = None
        self.kmeans = None
        self.candidate_nodes = None

    def generate_random_data(self):
        """
        Generate some random data
        """
        log("Generating Random Data...")
        self.data = np.vstack(((np.random.randn(self.N - 25, 2) * 0.5 + np.array([1, 0])),
                        (np.random.randn(self.N - 15, 2) * 0.5 + np.array([1, 0])),
                        (np.random.randn(10, 2) * 0.5 + np.array([1, 0]))))

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
        
        log("Saving generated clusters to /images/cluster.jpg...")
        plt.savefig("images/cluster.jpg")
        plt.close()

    def run_workflow(self):
        self.generate_random_data()
        self.display_random_plot()
        self.generate_elbow()
        self.generate_cluster()
        self.return_candidate_nodes()
        
    def return_candidate_nodes(self):
        return self.candidate_nodes