# IA3_DIT065
Individual assignment 3 for course DIT065

The file `/data/2023-DAT470-DIT065/open_pubs.csv` contains information about pubs in the UK. In particular, the file contains the coordinates of the pub, langitudinal and longitudinal. Luckily, the surface of a sphere (as we can model the Earth, for example), is a manifold; this means we can treat a local, small area (such as the UK) as an Euclidean plane. For our convenience, the dataset already contains Euclidean coordinates for the pubs (called easting and northing), in meters, so it will be easy to treat the data with little error as Euclidean.

Your task is to implement nearest neighbor search using a k-d tree. Use the simplifications from the lecture slides: use the same data structure for the box nodes, that is, the simple node structure that has a median, and left and right children; you do not have to implement the complex (but much more efficient) version that is given in Numerical Recipes. Follow the slides.

Your implementation should be able to read in the data from the file given above, and return the name of the nearest pub to a location, given in Euclidean coordinates (that is, northing and easting).

Return your solution as a file named exercise-3.py.
