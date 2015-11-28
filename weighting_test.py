import numpy as np
import random

from scipy.optimize import root 
from math import *

newarray = np.loadtxt('popgrid.txt')
newarray = newarray[newarray[:, 2] > 0]
pop = newarray[:, 2]
min_lat, min_lon = min(newarray[:,0]), min(newarray[:,1])# Get min lat and lon to subtract from pts
cart_array = 100*(newarray[:,:2] - [min_lat, min_lon]) # Scaling by 100 and sampling by every 50 to spread out the data
cart_array = np.concatenate((cart_array, newarray[:,2] \
	.reshape(newarray.shape[0],1)),axis=1)

def weighting(x, y, pop, idx, rad=10):
	cur_x, cur_y, cur_pop = x[idx], y[idx], pop[idx]
	if cur_pop == 0: # effect of pt is removed if no population
		return 0
	
	denom = np.sum([pop[ii] for ii in range(len(pop)) \
		if (np.linalg.norm(np.array([cur_x,cur_y])-np.array([x[ii],y[ii]])) <= rad and ii != idx)])
	
	return 1e3*(cur_pop / denom)


x_pts = cart_array[:,0]
y_pts = cart_array[:,1]
pop = cart_array[:,2]


for ii in range(len(x_pts)):
	print weighting(x_pts, y_pts, pop, ii)