****************************************************************
README for the functions and methods prepared for Fall 2015 Final Project for AM205, used to optimally determine distribution centers atop a densely spaced grid with a third dimension to optimize over. 

Project completed by Jonathan Friedman and Taylor Killian
***************************************************************

There are three .py files that are necessary to run and operate our code.
-- driver.py : Driver file that sets up and organizes the types of weights and clusterings that are to be used to locate the optimal placement of distribution centers.
-- optimal_clustering.py : file that contains the modules and functions used to perform the clustering according to weighted least squares.
-- helpers.py : a set of helper functions that were used to clean and process the data, as well as measure the error of our intermediate and final solutions. [The shapefile module is not as common and your python distribution may not have it loaded. If you were desirous to run our code, you can simply comment out that import statement so as to not have an error thrown.]

driver.py reads in a text file of points that are derived from the 2010 US Census for Massachusetts (popgrid.txt). Each point is representative of a census block and is designated by the latitude and longitude of that location as well as the total population of individuals with that block as their residence.

Within driver.py, the latitude,longitude pairings are converted and scaled to a magnified cartesian grid for easier use with the numpy module. We split this data 85/15 into a test and validation set. The validation set is used to compare different weighting functions that were used to influence the adjustment of cluster centers during the intermediate step of our algorithm.

We left our code in it's more complex form so that you could get a sense of how we ultimately used it to run different numerical experiments to evaluate and quantify the effect our weighting and error functions had on the performance of our method.

We left commented out simpler versions of certain portions of code so that if you wanted to run a basic version of our project, you could without having large runtimes. 

