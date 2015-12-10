# am205-project

****************************************************************
README for the functions and methods prepared for Fall 2015 Final Project for AM205, used to optimally determine distribution centers over a set of geographic points with population information. 

Project by Jonathan Friedman and Taylor Killian
***************************************************************
There are three .py files that are necessary to run and operate our code.
-- <code>driver.py</code> : Driver file that sets up and organizes the types of weights and clusterings that are to be used to locate the optimal placement of distribution centers.
-- <code>optimal_clustering.py</code> : file that contains the modules and functions used to perform the clustering according to weighted least squares.
=======
There are three .py files that are necessary to run and operate our code.   
-- <code>driver.py</code> : Driver file that sets up and organizes the types of weights and clusterings that are to be used to locate the optimal placement of distribution centers.   
-- <code>optimal_clustering.py</code> : file that contains the modules and functions used to perform the clustering according to weighted least squares.   
>>>>>>> 30a62e68a381d03e1d45a7781175d4815b1d49b1
-- <code>helpers.py</code> : a set of helper functions used to clean and process the data, as well as measure the error of our intermediate and final solutions. (If you want to use your own geographical shapefiles, you can uncomment <code>import shapefile</code> and use [pyshp](https://github.com/GeospatialPython/pyshp), or the GIS of your choice.) 

There is also <code>geoparse.py</code> which demonstrates how to read in a shapefile using our code.

<code>driver.py</code> reads in a text file of points that are derived from the 2010 US Census for Massachusetts (popgrid.txt). Each point represents a census block and has a latitude and longitude, as well the total population of that census block.

Within <code>driver.py</code>, the latitude,longitude pairings are converted and scaled to a magnified cartesian grid for easier use with the numpy module. We split this data 85/15 into a test and validation set. The validation set is used to compare different weighting functions that were used to influence the adjustment of cluster centers during the intermediate step of our algorithm.

We left our code in its more complex form so that you could get a sense of how we ultimately used it to run different numerical experiments to evaluate and quantify the effect our weighting and error functions had on the performance of our method. However, in some places we left commented-out simpler versions to try out. 
