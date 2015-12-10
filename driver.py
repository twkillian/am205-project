from math import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

from scipy.optimize import root
from sklearn.cross_validation import train_test_split
from optimal_clustering import find_centers
from helpers import error

# Driver function that loads data, runs the modified Lloyd's algorithm, and produces plots.

# Load the data
newarray = np.loadtxt('popgrid.txt')
newarray = newarray[newarray[:, 2] > 0]
pop = newarray[:, 2]
min_lat, min_lon = min(newarray[:,0]), min(newarray[:,1])# Get min lat and lon to subtract from pts
cart_array = 100*(newarray[:,:2] - [min_lat, min_lon]) # Scaling by 100 to spread out the data
cart_array = np.concatenate((cart_array, newarray[:,2] \
	.reshape(newarray.shape[0],1)),axis=1)

cart_array[:, [1, 0]] = cart_array[:, [0, 1]] # swap first two columns to get [lat, lon, pop]

# Split data into test and validation sets
test_array, validation_array = train_test_split(cart_array, test_size = 0.15)
test_pop = test_array[:,2]
validation_pop = validation_array[:,2]

# Initialization and setup
tol = 250                 # Terminate if cost function falls below this value
max_clusters = 10         # Terminate after trying at most this many clusters
tries_per_iter = 3        # Try this many choices of initial points
max_pop = float(max(pop)) # Largest population at a single point in the grid
thres = 1                 # Threshold for population filter

for i_weight in ['lin', 'sq', 'sqrt', 'log', 'max']:

	print "Using {} weighting".format(i_weight)

	# Compute the scale for weight normalization
	if i_weight == 'lin': scale = float(np.sum(test_pop))
	elif i_weight == 'sq': scale = np.sum(test_pop**2)
	elif i_weight == 'sqrt': scale = np.sum(np.sqrt(test_pop))
	elif i_weight == 'log': scale = np.sum(np.log(test_pop))
	elif i_weight == 'max': scale = max_pop
	else: scale = 1

	# Per separate weighting problem initialization
	num_clusters = 0
	min_centers = None
	min_clusters = None
	min_err = np.inf

	# Iteratively add new distribution centers and find their optimal location 
	# until either tol, or max_clusters, is reached
	while (min_err > float(tol)/scale) and (num_clusters < max_clusters):
		num_clusters += 1
		min_err = np.inf

		# Perform clustering tries_per_iter times choosing random starting points 
		# At each iteration, save the best result 
		for i in range(tries_per_iter):

			# Find optimal placement for number of distribution centers specified.
			centers, clusters = find_centers(test_array, num_clusters, wt=i_weight, scale=scale, threshold=thres)
			# Measure average consumer distance from distribution center
			err = error(centers, test_array[:,:2], test_pop, avg=True, wt=i_weight, scale=scale, max_pop=max_pop, threshold=thres)

			if min_err > err: # Check whether current soln has improved the previous soln
				min_err = err
				min_centers = centers
				min_clusters = clusters

		print num_clusters, min_err # Keep the user updated

	print "Found solution! With weighting function {0}, there are {1} clusters with error {2}. Plotting result now...".format(i_weight, num_clusters, min_err)

	if i_weight == 'lin': validation_scale = float(np.sum(validation_pop))
	elif i_weight == 'sq': validation_scale = np.sum(validation_pop**2)
	elif i_weight == 'sqrt': validation_scale = np.sum(np.sqrt(validation_pop))
	elif i_weight == 'log': validation_scale = np.sum(np.log(validation_pop))
	elif i_weight == 'max': validation_scale = max_pop
	else: validation_scale = 1
	validation_error = error(centers, validation_array[:,:2], validation_pop, avg=True, wt=i_weight, scale=validation_scale, max_pop=max_pop, threshold=thres)

	# Plotting takes a while
	palette = sns.hls_palette(num_clusters)
	plt.figure()
	i = 0
	for key in clusters.keys():
		cur_cluster = clusters[key]
		for pt in cur_cluster:
			plt.plot(pt[0], pt[1],'.',markersize=8, color=palette[i], alpha=pt[2]/max_pop)
		plt.plot(centers[key][0], centers[key][1],'ko', markersize=10)
		i += 1
		
	plt.axis('off')
	plt.annotate('Cost: %0.5f' % validation_error, xy=(15,20), xytext=(15,20), fontsize=30)
	plt.savefig('images/solution_{0}wt_clusters{1}_minpop{2}.png'.format(i_weight,num_clusters,thres))
