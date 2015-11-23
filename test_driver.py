from math import *
import numpy as np
import matplotlib.pyplot as plt
import random

from scipy.optimize import root
from test_kmeans import find_centers

newarray = np.loadtxt('popgrid.txt')
min_lat, min_lon = min(newarray[:,0]), min(newarray[:,1])# Get min lat and lon to subtract from pts
cart_array = 100*(newarray[:,:2] - [min_lat, min_lon]) # Scaling by 100 and sampling by every 50 to spread out the data
cart_array = np.concatenate((cart_array, newarray[:,2] \
	.reshape(newarray.shape[0],1)),axis=1)

num_clusters = 2 # Testing, find optimal location for two clusters!

centers, clusters = find_centers(cart_array,num_clusters)

palette = sns.hls_palette(num_clusters)

plt.figure()
for ii in range(num_clusters):
	cur_cluster = clusters[ii]
	for pt in cur_cluster:
		plt.plot(pt[0],pt[1],'.',markersize=8, color=palette[ii])

	plt.plot(centers[ii][0],centers[ii][1],'ro', markersize=10)
plt.show()