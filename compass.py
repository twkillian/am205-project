import numpy as np
import matplotlib.pyplot as plt
from math import *

def f(p, grid):
	""" Evaluates f at point p over the given grid. """
	err = 0
	x, y = p
	for i in range(grid.shape[0]):
		err += threshold(grid[i, 2]) * sqrt((x - grid[i, 0])**2 + (y - grid[i, 1])**2)
	return sqrt(err)

def threshold(p, t=1):
	if p > t:
		return p
	return 0

def move(dir, step):
	""" Returns a move in given direction of given size. """
	if (dir == 0):
		return step * np.array([0, 1])
	elif (dir == 1):
		return step * np.array([1, 0])
	elif (dir == 2):
		return step * np.array([0, -1])
	elif (dir == 3):
		return step * np.array([-1, 0])

newarray = np.loadtxt('popgrid.txt')
newarray = newarray[newarray[:, 2] > 0]
max_pop = np.max(newarray[:, 2])
min_lat, min_lon = min(newarray[:, 0]), min(newarray[:, 1]) # Get min lat and lon to subtract from pts
cart_array = 100*(newarray[:, 0:2] - [min_lat, min_lon]) # Scaling by 100 and sampling by every 50 to spread out the data
cart_array = np.concatenate((cart_array, newarray[:, 2]
	                  		 .reshape(newarray[:, 2].shape[0], 1)), axis=1)
cart_array[:, [1, 0]] = cart_array[:, [0, 1]] # swap first two columns

p = np.array([150., 135.]) # initial guess
directions = np.zeros(4) # north, east, south, west
curr = f(p, cart_array)
tol = 1e-5
step = 1
count = 0

while True:
	count += 1
	directions[0] = f(p + step * np.array([0, 1]), cart_array)
	directions[1] = f(p + step * np.array([1, 0]), cart_array)
	directions[2] = f(p - step * np.array([0, 1]), cart_array)
	directions[3] = f(p - step * np.array([1, 0]), cart_array)
	min_dir = np.argmin(directions)

	if directions[min_dir] < curr:
		p += move(min_dir, step)
		curr = f(p, cart_array)

	else:
		step *= 0.5
		if step < tol: break

	if count > 100000: break

print p, count, step

fig = plt.figure(figsize=(10, 8))
for i in range(cart_array.shape[0]):
	plt.plot(cart_array[i, 0], cart_array[i, 1],'.',markersize=8, color='b',
		     alpha=cart_array[i, 2] / max_pop)
# plt.scatter(cart_array[:, 0], cart_array[:, 1], alpha=cart_array[:, 2] / max_pop, s=25)
plt.xlim(-10, 370)
plt.ylim(-10, 200)
plt.plot(p[0], p[1], '.', markersize=40, color='r')
plt.axis('off')
plt.savefig('thresholdweight.png')
