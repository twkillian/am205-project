from math import *
import numpy as np
# import shapefile

def dist(coords, r=6371000):
	"""
	Calculates the surface distance in meters between two points 
	on a sphere of radius r. Uses haversine formula from
	https://en.wikipedia.org/wiki/Great-circle_distance#Computational_formulas 
	"""
	y1, x1, y2, x2 = coords
	dphi = abs(x2 - x1)
	dlambda = abs(y2 - y1)
	return r*2*asin(sqrt((sin(dphi*0.5))**2 + cos(x1)*cos(x2)*(sin(dlambda*0.5))**2))

def center(coords):
	"""
	Calculates the center of a box given the coordinates of the lower left corner 
	and the upper right corner.
	"""
	y1, x1, y2, x2 = coords
	return [(y1 + y2)*0.5, (x1 + x2)*0.5]

def read(shp='geofiles/tabblock2010_25_pophu/tabblock2010_25_pophu'):
	sf = shapefile.Reader(shp)
	sr = sf.shapeRecords()
	for i in sr:
		yield center(i.shape.bbox), i.record[-1]

def euclidean(p, q):
	""" Euclidean distance. """
	return sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

def weight(cur_pop, wt='lin', max_pop=1, threshold=1): # User supplied weighting function of each 
	if wt == 'lin':       
		if cur_pop <= threshold:
			return 0
		else: return cur_pop
	elif wt == 'sq':     return cur_pop*cur_pop
	elif wt == 'sqrt': return np.sqrt(cur_pop)
	elif wt == 'log': return np.log(cur_pop)
	elif wt == 'max': return float(cur_pop)/max_pop
	else:             return cur_pop

def error(points, grid, pop, errfunc=euclidean, avg=False, wt='lin', max_pop=1, threshold=1):
	"""
	Calculates the sum of the minimum errors given by f, weighted by sqrt(population),
	of each gridpoint to a point in points.
	"""
	err = 0
	for i in range(grid.shape[0]):
		err += weight(pop[i], wt, max_pop, threshold) * np.min([errfunc(p, grid[i, :]) for p in points])

	if avg:
		return 1. * err / grid.shape[0]
	return err
