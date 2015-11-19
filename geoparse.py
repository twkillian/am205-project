# Parses geographic population shapefiles into a list using pyshp
# pyshp can be found at https://github.com/GeospatialPython/pyshp
from helpers import dist, center, read

if __name__ == "__main__":
	geogen = read()
	with open('popgridtest.dat', 'w') as f:
		for i in geogen:
			f.write('{}, {},{}\n'.format(i[0][0], i[0][1], i[1]))