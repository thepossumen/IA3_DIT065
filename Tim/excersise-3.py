import numpy as np
import pandas as pd


class BoxNode:
    def __init__(self, median, left=None, right=None):
        self.median = median
        self.left = left
        self.right = right


def KDtree(dataset, depth=0):
    if len(dataset) == 2:
        return BoxNode(None, dataset.iloc[0], dataset.iloc[1])
    elif len(dataset) == 1:
        return BoxNode(None, dataset.iloc[0], None)
    else:
        axis = depth % 2
        if axis == 0:
            dataset = dataset.sort_values(by=["easting"])
        else:
            dataset = dataset.sort_values(by=["northing"])

        median_idx = len(dataset) // 2
        median = dataset.iloc[median_idx]
        depth += 1
        left_child = KDtree(dataset.iloc[:median_idx], depth)
        right_child = KDtree(dataset.iloc[median_idx+1:], depth)

        return BoxNode(median, left_child, right_child)
    
def distance(p1, p2):
    return np.sqrt(((p1[0] - p2.iloc[0])**2) + ((p1[1] - p2.iloc[1])**2))


def find_local(node, query, depth):
    if node.median is None:
        # in case one of the nodes is none
        try:
            if distance(query, node.right) < distance(query, node.left):
                closest_point = node.right
            else:
                closest_point = node.left
        except:
            if node.left is None:
                closest_point = node.right
            else:
                closest_point = node.left
        return closest_point
    else:
        axis = depth % 2
        if float(query[axis]) < float(node.median[axis]):
            return find_local(node.left, query, depth + 1)
        else:
             return find_local(node.right, query, depth + 1)
        
def update_global(node, query, best_neighbor, best_distance, depth):
    if node.median is None:
        if node.left is not None and node.right is not None:
            if distance(query, node.right) < best_distance:
                return node.right, distance(query, node.right)
            elif distance(query, node.left) < best_distance:
                return node.left, distance(query, node.left)
            else:
                return best_neighbor, best_distance
        else:
            if node.left is None:
                if distance(query, node.right) < best_distance:
                    return node.right, distance(query, node.right)
            elif node.right is None:
                if distance(query, node.left) < best_distance:
                    return node.left, distance(query, node.left)
            else:
                return best_neighbor, best_distance
    else:
        axis = depth % 2
        if query[axis] < node.median[axis]:
            best_neighbor, best_distance = update_global(node.left, query, best_neighbor, best_distance, depth + 1)
            if query[axis] + best_distance > node.median[axis]:
                best_neighbor, best_distance = update_global(node.right, query, best_neighbor, best_distance, depth + 1)
        else:
            best_neighbor, best_distance = update_global(node.right, query, best_neighbor, best_distance, depth + 1)
            if query[axis] - best_distance <= node.median[axis]:
                best_neighbor, best_distance = update_global(node.left, query, best_neighbor, best_distance, depth + 1)
    return best_neighbor, best_distance

def nearest_neighbor(root, query):
    p = find_local(root, query, 0)
    r = distance(query, p)
    p, r = update_global(root, query, p, r, 0)
    return p["name"]


if __name__ == "__main__":
    df = pd.read_csv("/data/2023-DAT470-DIT065/open_pubs.csv", usecols=["name", "easting", "northing"])
    df = df[["easting", "northing", "name"]]
    root = KDtree(df)

    #should return Basildon something club
    query = (571686, 190376)
   

    nearest_pub = nearest_neighbor(root, query)
    print(nearest_pub)