# Parses geographic shapefiles using pyshp
# pyshp can be found at https://github.com/GeospatialPython/pyshp
import shapefile

def read(shp='geofiles/tabblock2010_25_pophu/tabblock2010_25_pophu'):
	sf = shapefile.Reader(shp)
	sr = sf.shapeRecords()
	for i in xrange(10):
		print 'Box coords: {}\nPopulation: {}\n'.format(sr[i].shape.bbox,
														  sr[i].record[-1])


if __name__ == "__main__":
	read()
