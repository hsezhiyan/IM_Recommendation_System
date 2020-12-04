import csv
import numpy as np
import math
import personality_cs_reading

def knn(data, query, k, distance_fn, choice_fn):
    neighbor_distances_and_indices = []
    
    # 3. For each example in the data
    for index, example in enumerate(data):
        # 3.1 Calculate the distance between the query example and the current
        # example from the data.
        distance = distance_fn(example[:-1], query)
        
        # 3.2 Add the distance and the index of the example to an ordered collection
        neighbor_distances_and_indices.append((distance, index))
    
    # 4. Sort the ordered collection of distances and indices from
    # smallest to largest (in ascending order) by the distances
    sorted_neighbor_distances_and_indices = sorted(neighbor_distances_and_indices)
    
    # 5. Pick the first K entries from the sorted collection
    k_nearest_distances_and_indices = sorted_neighbor_distances_and_indices[:k]

    return k_nearest_distances_and_indices

def euclidean_distance(point1, point2):
    sum_squared_distance = 0
    for i in range(len(point1)):
        sum_squared_distance += math.pow(point1[i] - point2[i], 2)
    return math.sqrt(sum_squared_distance)

def RunKNN(name, K =25):
    

    dict_data = personality_cs_reading.read_csv_file()
    reg_keys = list(dict_data.keys())
    reg_data = list(dict_data.values())
    # Question:
    # Given the data we have, what's the best-guess at someone's weight if they are 60 inches tall?
    #reg_query = range(0,22)
    reg_query = dict_data[name]
    reg_k_nearest_neighbors= knn(
        reg_data, reg_query, k=K, distance_fn=euclidean_distance, choice_fn=mean
    )   
    matchedUsers = []
    for distanceIndex in reg_k_nearest_neighbors:
        matchedUsers.append(reg_keys[distanceIndex[1]])  

    return (matchedUsers)
	

if __name__ == "__main__":
    userName = "fahmed@innovationminds.com"
    RunKNN(name = userName)
