import numpy as np
import random

from scipy.optimize import root 
from math import *

'''
Functions to solve our clustering problem by applying weighted Lloyd's algorithm.
------------------------------------------------------------------------
Written by TWK, 23 Nov 2015
Modified repeatedly by TWK and JHF
Adapted from https://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/
'''

def init_centers(k):
	""" Randomly initialize clustering centers within MA. """
	centers = [(random.uniform(50, 250), \
		random.uniform(80 ,140)) for i in range(k)]
	return centers

def assign_points(X,ctrs):
	""" Assign points to the closest center. """
	clusters = {}
	for x in X:
		bestLoc = min([(i[0], np.linalg.norm(x[:2]-ctrs[i[0]])) \
			for i in enumerate(ctrs)], key=lambda t: t[1])[0]

		try:
			clusters[bestLoc].append(x)
		except KeyError:
			clusters[bestLoc] = [x]

	return clusters

def grad_phi(ctr, x, y, pop, wt='lin', scale=1, max_pop=1, threshold=1):
	""" Gradient of cost function. """
	def weight(cur_pop, wt='lin', max_pop=1): # User supplied weighting function of each 
		if wt == 'lin':       
			if cur_pop < threshold:
				           return 0
			else:          return cur_pop
		elif wt == 'sq':   return cur_pop*cur_pop
		elif wt == 'sqrt': return sqrt(cur_pop)
		elif wt == 'log':  return np.log(cur_pop)
		elif wt == 'max':  return cur_pop
		else:              return cur_pop

	f0, f1 = 0, 0
	for i in range(len(x)):
		dx = ctr[0]-x[i]
		dy = ctr[1]-y[i]
		d = 1/sqrt(dx*dx + dy*dy)
		f0 += float(weight(pop[i],wt,max_pop))/scale*(2*dx*d)
		f1 += float(weight(pop[i],wt,max_pop))/scale*(2*dy*d)
	return np.array([f0,f1])

def adjust_centers(ctrs, clusters, wt='lin', scale=1, threshold=1):
	""" Adjust center location using our version of Lloyd's algorithm. """
	new_ctrs = []
	keys = sorted(clusters.keys())
	for k in keys:
		pts = clusters[k]
		x = [pts[ii][0] for ii in range(len(pts))]
		y = [pts[ii][1] for ii in range(len(pts))]
		pop = [pts[ii][2] for ii in range(len(pts))]

		max_pop = max(pop)

		# Find the new clusters
		new_ctrs.append(root(fun=grad_phi, x0=ctrs[k], args=(x, y, pop, wt, scale, max_pop, threshold),
		 					 jac=False, method='lm').x)
	return new_ctrs

def has_converged(ctrs, old_ctrs):
	""" Simple convergence check. """
	return (set([tuple(a) for a in ctrs]) == set([tuple(a) for a in old_ctrs]))

def find_centers(X, k, wt='lin', scale=1, threshold=1):
	""" Cluster points and find optimal center locations. """
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
		ctrs = adjust_centers(ctrs, clusters, wt, scale, threshold)
	return (ctrs, clusters)



