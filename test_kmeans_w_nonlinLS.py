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
	centers = [(random.uniform(0,150), \
		random.uniform(0,150)) for i in range(k)]
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

def weighting(pt, rad=50):
	cur_pop = pt[2]
	if cur_pop == 0: # effect of pt is removed if no population
		return 0
	
	denom = np.sum([kp[2] for kp in pts \
	 if np.linalg.norm(pt-kp) <= rad])
	
	return cur_pop / denom # pts weight is proportional to its neighborhood

# Euclidean distance function, to be minimized.
# def phi(ctr, x):
# 	s = 0
# 	for i in range(len(x)):
# 		dx = ctr[0]-x[i]
# 		dy = ctr[0]-y[i]
# 		ss = sqrt(dx*dx + dy*dy) # Could subtract some noise here
# 		s += pop[i] * ss*ss
# 	return s

# Gradient
def grad_phi(ctr, x, y, pop):
	f0, f1 = 0, 0
	for i in range(len(x)):
		dx = ctr[0]-x[i]
		dy = ctr[1]-y[i]
		d = 1/sqrt(dx*dx + dy*dy)
		# f0 += weighting([x[i],y[i],pop[i]])*(2*dx-2*n[i]*dx*d)
		# f1 += weighting([x[i],y[i],pop[i]])*(2*dy-2*n[i]*dx*d)
		f0 += pop[i]*(2*dx*d)
		f1 += pop[i]*(2*dy*d)
	return np.array([f0,f1])

# Adjust location position via non-lin LS
def adjust_centers(ctrs, clusters):
	new_ctrs = []
	keys = sorted(clusters.keys())
	for k in keys:
		pts = clusters[k]
		x = [pts[ii][0] for ii in range(len(pts))]
		y = [pts[ii][1] for ii in range(len(pts))]
		pop = [pts[ii][2] for ii in range(len(pts))]

		# Find the new cluster center according to non-lin LS
		new_ctrs.append(root(fun=grad_phi, x0=ctrs[k], args=(x, y, pop),
		 					 jac=False, method='lm').x)
	return new_ctrs

# Simple convergence check
def has_converged(ctrs, old_ctrs):
	return (set([tuple(a) for a in ctrs]) == set([tuple(a) for a in old_ctrs]))

# Cluster points as 
def find_centers(X, k):
	old_ctrs = random.sample(X[:,:2],k)
	ctrs = init_centers(k)
	iters = 0
	while not has_converged(ctrs, old_ctrs):
		# print "Working on iteration {}".format(iters)
		iters += 1
		old_ctrs = ctrs
		# Assign all points in X to clusters
		clusters = assign_points(X,ctrs)
		# Adjust locations of locations
		ctrs = adjust_centers(ctrs,clusters)
	return (ctrs, clusters)



