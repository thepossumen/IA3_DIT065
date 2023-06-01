import numpy as np
import csv
from math import sqrt

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
        axis = depth % 2
        if axis == 0:
            dataset = np.sort(dataset, order='easting')
        elif axis == 1:
            dataset = np.sort(dataset, order='northing')
        else:
            raise ValueError(f'Axis needs to be 0 or 1, not {axis}')
        median_idx = len(dataset) // 2
        median = dataset[median_idx][axis+1]
        left_child = kdtree(dataset[:median_idx], depth+1)
        right_child = kdtree(dataset[median_idx+1:], depth+1)
        return BoxNode(median, left_child, right_child)

def euclid_distance(p1, p2):
    return sqrt(float((p1[0] - p2[0])**2) + float((p1[1] - p2[1])**2))


def find_local(node, query, depth):
    if not node.median:
        # the node is a leaf
        # find point (child) closest to query
        shortest_dist = 9999999
        closest_point = None
        for child in [node.left_child, node.right_child]:
            if child != None:
                dist = euclid_distance(child.tolist()[1:], query)
                if dist < shortest_dist:
                    shortest_dist = dist
                    closest_point = child
        return closest_point
    else:
        axis = depth % 2
        if query[axis] <= node.median:
            return find_local(node.left_child, query, depth+1)
        else:
            return find_local(node.right_child, query, depth+1)

def update_global(node, query, best_neighbor, best_distance, depth):
    if not node.median:
        for child in [node.left_child, node.right_child]:
            if child != None:
                dist = euclid_distance(child.tolist()[1:], query)
                if dist < best_distance:
                    best_neighbor = child
                    best_distance = dist
        return best_neighbor, best_distance
    else:
        axis = depth % 2
        if query[axis] <= node.median:
            best_neighbor, best_distance = update_global(\
                node.left_child, query, best_neighbor, best_distance\
                    , depth+1)
            if query[axis]+best_distance > node.median:
                best_neighbor, best_distance = update_global(\
                    node.right_child, query, best_neighbor, best_distance\
                        , depth+1)
        else:
            best_neighbor, best_distance = update_global(\
                node.right_child, query, best_neighbor, best_distance\
                    , depth+1)
            if query[axis]-best_distance <= node.median:
                best_neighbor, best_distance = update_global(\
                    node.left_child, query, best_neighbor, best_distance\
                        , depth+1)
        return best_neighbor, best_distance

def nearest_neighbor(root, query):
    p = find_local(root, query, 0)
    r = euclid_distance(p, query)
    p, r = update_global(root, query, p, r, 0)
    return p


if __name__ == '__main__':
    pub_names, coordinates = read_pub_csv(datafile)
    
    # should return Basildon something club
    # query = (571686, 190376)
    # Carriers Arms
    query = (607463.0,235397.0)

    root = kdtree(coordinates, 0)
    
    closest_pub = nearest_neighbor(root, query)
    #print('closest pub point:', closest_pub, 'type:', type(closest_pub))
    
    print('Query:', query)
    print("closest pub:", pub_names[closest_pub[0]])

    result_coords = closest_pub.tolist()[1:]
    print('distance:',euclid_distance(query, result_coords))