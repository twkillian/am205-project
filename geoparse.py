# Parses geographic shapefiles using pyshp
# pyshp can be found at https://github.com/GeospatialPython/pyshp
import shapefile
from helpers import dist, center

def read(shp='geofiles/tabblock2010_25_pophu/tabblock2010_25_pophu'):
	sf = shapefile.Reader(shp)
	sr = sf.shapeRecords()
	for i in xrange(10):
		print """Box coords: {}\nPopulation: {}
			   Center: {}\nDist: {}\n""".format(sr[i].shape.bbox,
											    sr[i].record[-1],
											    center(sr[i].shape.bbox),
											    dist(sr[i].shape.bbox))


if __name__ == "__main__":
	read()