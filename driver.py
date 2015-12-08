from math import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

from scipy.optimize import root
from sklearn.cross_validation import train_test_split
from optimal_clustering import find_centers
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

#Split data for validation purposes across different weighting functions
test_array, validation_array = train_test_split(cart_array, test_size = 0.15)
test_pop = test_array[:,2]
validation_pop = validation_array[:,2]

# Initialization and setup
tol = 250                 # maximum acceptable average distance from consumer to distributor, this should not be above 400; otherwise, >1e6 is ok
max_clusters = 15
tries_per_iter = 3        # Stochastically vary intialization points to avoid being stuck in local minima
max_pop = float(max(pop)) # Largest population at a single point in the grid
thres = 1                # Thresholding for minimum population size that we adjust our centers for.

for i_weight in ['lin', 'sq', 'sqrt', 'log', 'max']:

	print "Using {} weighting".format(i_weight)

	# Compute the scale by which we'll normalize the weights
	if i_weight == 'lin': scale = 1
	elif i_weight == 'sq': scale = float(np.sum(test_pop))/np.sum(test_pop**2)
	elif i_weight == 'sqrt': scale = float(np.sum(test_pop))/np.sum(np.sqrt(test_pop))
	elif i_weight == 'log': scale = float(np.sum(test_pop))/np.sum(np.log(test_pop))
	elif i_weight == 'max': scale = 1/max_pop
	else: scale = 1

	# Per separate weighting problem initialization
	num_clusters = 0
	min_centers = None
	min_clusters = None
	min_err = np.inf

	# Iteratively add new distribution centers and find their optimal location 
	# until population is provided sufficient access to distribution centers
	while (min_err > tol) and (num_clusters < max_clusters):
		num_clusters += 1
		min_err = np.inf

		# Perform clustering tries_per_iter times choosing random starting points 
		# at each iteration, save the best result 
		for i in range(tries_per_iter):

			# Find optimal placement for number of distribution centers specified.
			centers, clusters = find_centers(test_array, num_clusters, wt=i_weight, scale=scale, threshold=thres)
			# Measure average consumer distance from distribution center
			err = error(centers, test_array[:,:2], test_pop, avg=True, wt=i_weight, scale=scale, max_pop=max_pop, threshold=thres)

			if min_err > err: # Check whether current sol'n has improved the previous sol'n
				min_err = err
				min_centers = centers
				min_clusters = clusters

		print num_clusters, min_err # Algorithm progress notification

	print "Found solution! With weighting function {0}, there are {1} clusters with error {2}. Plotting result now...".format(i_weight, num_clusters, min_err)

	if i_weight == 'lin': validation_scale = 1
	elif i_weight == 'sq': validation_scale = float(np.sum(validation_pop))/np.sum(validation_pop**2)
	elif i_weight == 'sqrt': validation_scale = float(np.sum(validation_pop))/np.sum(np.sqrt(validation_pop))
	elif i_weight == 'log': validation_scale = float(np.sum(validation_pop))/np.sum(np.log(validation_pop))
	elif i_weight == 'max': validation_scale = 1/max_pop
	else: validation_scale = 1
	validation_error = error(centers, validation_array[:,:2], validation_pop, avg=True, wt=i_weight, scale=validation_scale, max_pop=max_pop, threshold=thres)

	# Plotting
	palette = sns.hls_palette(num_clusters)
	plt.figure()
	i = 0
	for key in clusters.keys():
		cur_cluster = clusters[key]
		for pt in cur_cluster:
			plt.plot(pt[0], pt[1],'.',markersize=8, color=palette[i], alpha=pt[2]/max_pop)

		plt.plot(centers[key][0], centers[key][1],'ko', markersize=10)

		i += 1
	plt.grid(b=False)
	plt.xticks([])
	plt.yticks([])
	plt.axes(axisbg='white',frameon=False)
	plt.annotate('Cost: %0.5f' % validation_error, xy=(15,20), xytext=(15,20), fontsize=30)
	plt.savefig('images/solution_clusters{0}_minpop{1}_{2}wt.png'.format(num_clusters,thres,i_weight))
	# plt.show()



