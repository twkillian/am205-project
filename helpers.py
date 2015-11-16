from math import *
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