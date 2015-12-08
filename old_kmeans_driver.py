import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from kmeans_clustering_nonlinLS import init_board, find_centers



N = 500 # Number of points
K = 5 # Number of clusters
X = init_board(N) # Initializes point spread

mu, clusters = find_centers(X,K)

palette = sns.hls_palette(K)

plt.figure()
for i_cluster in range(len(mu)):
	cur_cluster = clusters[i_cluster]
	for pt in cur_cluster:
		plt.plot(pt[0],pt[1],'.',markersize=8,color=palette[i_cluster])

	plt.plot(mu[i_cluster][0],mu[i_cluster][1],'ro',markersize=9)
plt.show()