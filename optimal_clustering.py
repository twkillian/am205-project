import numpy as np
import random

from scipy.optimize import root 
from math import *

'''
The following subfunctions have been put together to allow us to solve 
for the optimal location of multiple service locations via the utilization
of clustering. What this entails is determining distance from each point
to a potential location, "grouping" them by the location they are 
closest to and then adjusting the location toward the mean position 
of the points, weighted by the porportion of population at each point 
within some servicable radius.
------------------------------------------------------------------------
Written by TWK, 23 Nov 2015. 
Adapted from https://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/
'''

# Randomly initialize the position of clustering locations
def init_centers(k):
	#Randomly draw x and y pts betweeen grid_bdy max and mins in each dim
	centers = [(random.uniform(0,400), \
		random.uniform(0,180)) for i in range(k)]
	return centers

# Assign points to closest location
def assign_points(X,ctrs):
	clusters = {}
	for x in X:
		bestLoc = min([(i[0], np.linalg.norm(x[:2]-ctrs[i[0]])) \
			for i in enumerate(ctrs)], key=lambda t: t[1])[0]

		try:
			clusters[bestLoc].append(x)
		except KeyError:
			clusters[bestLoc] = [x]

	return clusters

# Gradient
def grad_phi(ctr, x, y, pop, wt='lin', max_pop=1, threshold=1):
	
	def weight(cur_pop, wt='lin', max_pop=1): # User supplied weighting function of each 
		if wt == 'lin':       
			if cur_pop <= threshold:
				           return 0
			else:          return cur_pop
		elif wt == 'sq':   return cur_pop*cur_pop
		elif wt == 'sqrt': return sqrt(cur_pop)
		elif wt == 'log':  return np.log(cur_pop)
		elif wt == 'max':  return float(cur_pop)/max_pop
		else:              return cur_pop


	f0, f1 = 0, 0
	for i in range(len(x)):
		dx = ctr[0]-x[i]
		dy = ctr[1]-y[i]
		d = 1/sqrt(dx*dx + dy*dy)
		f0 += weight(pop[i],wt,max_pop)*(2*dx*d)
		f1 += weight(pop[i],wt,max_pop)*(2*dy*d)
	return np.array([f0,f1])

# Adjust location position via non-lin LS
def adjust_centers(ctrs, clusters, wt='lin', threshold=1):
	new_ctrs = []
	keys = sorted(clusters.keys())
	for k in keys:
		pts = clusters[k]
		x = [pts[ii][0] for ii in range(len(pts))]
		y = [pts[ii][1] for ii in range(len(pts))]
		pop = [pts[ii][2] for ii in range(len(pts))]

		max_pop = max(pop)

		# Find the new cluster center according to non-lin LS
		new_ctrs.append(root(fun=grad_phi, x0=ctrs[k], args=(x, y, pop, wt, max_pop, threshold),
		 					 jac=False, method='lm').x)
	return new_ctrs

# Simple convergence check
def has_converged(ctrs, old_ctrs):
	return (set([tuple(a) for a in ctrs]) == set([tuple(a) for a in old_ctrs]))

# Cluster points as 
def find_centers(X, k, wt='lin', threshold=1):
	old_ctrs = random.sample(X[:,:2],k)
	ctrs = init_centers(k)
	iters = 0
	while not has_converged(ctrs, old_ctrs):
		# print "Working on iteration {}".format(iters)
		iters += 1
		old_ctrs = ctrs
		# Assign all points in X to clusters
		clusters = assign_points(X, ctrs)
		# Adjust locations of locations
		ctrs = adjust_centers(ctrs, clusters, wt, threshold)
	return (ctrs, clusters)



