from math import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

from scipy.optimize import root
from test_kmeans_w_nonlinLS import find_centers
from helpers import error


newarray = np.loadtxt('popgrid.txt')
newarray = newarray[newarray[:, 2] > 0]
pop = newarray[:, 2]
min_lat, min_lon = min(newarray[:,0]), min(newarray[:,1])# Get min lat and lon to subtract from pts
cart_array = 100*(newarray[:,:2] - [min_lat, min_lon]) # Scaling by 100 and sampling by every 50 to spread out the data
cart_array = np.concatenate((cart_array, newarray[:,2] \
	.reshape(newarray.shape[0],1)),axis=1)

# Need to switch lat and lon since we are now in cartesian space
temp, temp2 = np.copy(cart_array[:,0]), np.copy(cart_array[:,1])
cart_array[:,0] = temp2
cart_array[:,1] = temp

tol = 200 # for average distance, this should not be above 400; otherwise, >1e6 is ok
num_clusters = 0
max_clusters = 7
tries_per_iter = 1
max_pop = float(max(pop)) # Largest population at a single point in the grid
thres = 10 # Thresholding for minimum population size that we adjust our centers for.
min_centers = None
min_clusters = None
min_err = np.inf

while (min_err > tol) and (num_clusters < max_clusters):
	num_clusters += 1
	min_err = np.inf

	# Try tries_per_iter starting points and pick the best result 
	for i in range(tries_per_iter):
		centers, clusters = find_centers(cart_array, num_clusters, wt=1, threshold=thres)
		err = error(centers, cart_array, pop, avg=True)
		if min_err > err:
			min_err = err
			min_centers = centers
			min_clusters = clusters

	print num_clusters, min_err

print "Found solution with error {}! Working on plotting now...".format(min_err)

palette = sns.hls_palette(num_clusters)
plt.figure()
i = 0
for key in clusters.keys():
	cur_cluster = clusters[key]
	for pt in cur_cluster:
		plt.plot(pt[0], pt[1],'.',markersize=8, color=palette[i], alpha=pt[2]/max_pop)

	plt.plot(centers[key][0], centers[key][1],'ro', markersize=10)
	i += 1
plt.show()