from math import *
import numpy as np
# import shapefile

def center(coords):
	"""
	Calculates the center of a box given the coordinates of the lower left corner 
	and the upper right corner.
	"""
	y1, x1, y2, x2 = coords
	return [(y1 + y2)*0.5, (x1 + x2)*0.5]

def read(shp='geofiles/tabblock2010_25_pophu/tabblock2010_25_pophu'):
	"""
	Reads shapefile. The default file is the population data from the 2010 census, which
	can be found at http://www2.census.gov/geo/tiger/TIGER2010/TABBLOCK/2010/
	"""
	sf = shapefile.Reader(shp)
	sr = sf.shapeRecords()
	for i in sr:
		yield center(i.shape.bbox), i.record[-1]

def euclidean(p, q):
	""" Euclidean distance. """
	return sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

def weight(cur_pop, wt='lin', max_pop=1, threshold=1):
	""" Weights points according to the given weighting function. """ 
	if wt == 'lin':       
		if cur_pop < threshold:
			return 0
		else: return cur_pop
	elif wt == 'sq':     return cur_pop*cur_pop
	elif wt == 'sqrt': return np.sqrt(cur_pop)
	elif wt == 'log': return np.log(cur_pop)
	elif wt == 'max': return cur_pop
	else:             return cur_pop

def error(points, grid, pop, errfunc=euclidean, avg=False, wt='lin', scale=1, max_pop=1, threshold=1):
	"""
	Calculates the sum of the minimum errors given by f, weighted by weight(population) and 
	scaled by scale, of each gridpoint to a point in points.
	"""
	err = 0
	for i in range(grid.shape[0]):
		err += float(weight(pop[i], wt, max_pop, threshold))/scale * np.min([errfunc(p, grid[i, :]) for p in points])

	if avg:
		return 1. * err / grid.shape[0]
	return err
