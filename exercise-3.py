import numpy as np
import csv

datafile = '/data/2023-DAT470-DIT065/open_pubs.csv'


# Distance from a point 𝑝 to the box (ℓ, ℎ) can be computed as follows:
# Initialize 𝐷 = 0
# for 𝑖 ← 1,2, ... , 𝑑 do
# if 𝑝" < ℓ " then
# 𝐷 ← 𝐷 + 𝑝" − ℓ " #
# else if 𝑝" > ℎ " then
# 𝐷 ← 𝐷 + 𝑝" − ℎ " #
# end if
# end for
# return 𝐷
#Note that this routine returns 0 if the point is inside the box

# Constructor for BoxNode is BoxNode(median, left_child, right_child)
class BoxNode:
    def __init__(self, median, left_child, right_child):
        self.median = median
        self.left_child = left_child
        self.right_child = right_child

def read_pub_csv(file):
    with open(file, 'r') as f:
        pub_names = []
        pub_coords = []
        file_contents = csv.reader(f)
        next(file_contents) #skip headers
        for i,line in enumerate(file_contents):
            name, easting, northing = line[1], float(line[4]), float(line[5])
            pub_names.append(name)
            pub_coords.append((i, easting, northing)) # keep track of name index
    arr_dtypes = [('pub_idx', int), ('easting', float), ('northing', float)]
    return pub_names, np.array(pub_coords, dtype=arr_dtypes)

def kdtree(dataset, depth):
    n = len(dataset)
    if n == 2:
        return BoxNode(None, dataset[0], dataset[1])
    elif n == 1:
        return BoxNode(None, dataset[0], None)
    else:
        # 0 is x-axis(easting) and 1 is y-axis(northing)
        axis = 0 if depth %2 == 0 else 1
        if axis == 0:
            dataset = np.sort(dataset, order='easting')
        elif axis == 1:
            dataset = np.sort(dataset, order='northing')
        else:
            raise ValueError(f'Axis needs to be 0 or 1, not {axis}')
        median_idx = len(dataset) // 2
        median = dataset[median_idx]
        left_child = kdtree(dataset[:median_idx], depth+1)
        right_child = kdtree(dataset[median_idx+1:], depth+1)
        return BoxNode(median, left_child, right_child)
        

if __name__ == '__main__':
    pub_names, coordinates = read_pub_csv(datafile)
    