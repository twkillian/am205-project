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

tol = 200 # for average distance, this should not be above 400; otherwise, >1e6 is ok
num_clusters = 0
max_clusters = 7
tries_per_iter = 3
min_centers = None
min_clusters = None
min_err = np.inf

while (min_err > tol) and (num_clusters < max_clusters):
	num_clusters += 1
	min_err = np.inf

	# Try tries_per_iter starting points and pick the best result 
	for i in range(tries_per_iter):
		centers, clusters = find_centers(cart_array, num_clusters)
		err = error(centers, cart_array, pop, avg=True)
		if min_err > err:
			min_err = err
			min_centers = centers
			min_clusters = clusters

	print num_clusters, min_err

print "Found solution with error {}! Working on plotting now...".format(err)

palette = sns.hls_palette(num_clusters)
plt.figure()
for ii in range(num_clusters):
	cur_cluster = clusters[ii]
	for pt in cur_cluster:
		plt.plot(pt[1], pt[0],'.',markersize=8, color=palette[ii])

	plt.plot(centers[ii][1], centers[ii][0],'ro', markersize=10)
plt.show()