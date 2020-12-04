from makeVectors import returnAllVectors
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


'''
Usage: python3 clustering.py <k(max range of number of clusters)>
'''


"""
Reference code from: https://medium.com/analytics-vidhya/how-to-determine-the-optimal-k-for-k-means-708505d204eb
"""

# function returns WSS score for k values from 1 to kmax
#the WSS metric is the measure of the distance of current sample from the cluster centre
def calculate_WSS(points, kmax):
    sse = []    #need an array of all distances
    indices = [i for i in range(1, kmax+1)] #get the indices array
    for k in range(1, kmax+1):
        kmeans = KMeans(n_clusters = k, random_state=0).fit(points) #get the clustering set up
        centroids = kmeans.cluster_centers_
        pred_clusters = kmeans.predict(points)
        curr_sse = 0

    # calculate square of Euclidean distance of each point from its cluster center and add to current WSS
        for i in range(len(points)):
            curr_center = centroids[pred_clusters[i]]
            curr_sse += (points[i, 0] - curr_center[0]) ** 2 + (points[i, 1] - curr_center[1]) ** 2 #calc dist from the centre of the cluster
            
        sse.append(curr_sse)

    print("best k:",indices[np.argmin(sse)])
    plt.title("Variance of different k's")
    plt.xlabel("k")
    plt.ylabel("SSE")
    plt.plot(indices, sse, linewidth=2, color='r')
    plt.show()
    return indices[np.argmin(sse)]  #return best K


#a simple method to get the predicted cluster labels
#for the points given by using KMeans

def return_labels(points, k):
    kmeans = KMeans(n_clusters = k, random_state=0).fit(points)
    labels = kmeans.labels_ #the predicted labels

    dict_labels = {}    #get a distribution of the labels (count of samples in each cluster)

    for i in range(points.shape[0]):
        print("User: ", points[i, :])
        print("Label: ", labels[i])
        if labels[i] not in dict_labels:
            dict_labels[labels[i]] = 1
        else:
            dict_labels[labels[i]] += 1
    print(dict_labels)
    return labels

def write_to_df(labels,userNames,points,filename = "Vectorized Label Users1.csv",names = ["Username","vector"]):
    df = pd.DataFrame(list(zip(userNames,points)),columns = names)
    df["Label"] = labels
    
    
    df.to_csv(filename) 


def read_from_df(filename = "Vectorized Label Users1.csv",names = ["Username","vector","Label"]):
    df = pd.read_csv(filename,sep = ",",header = None,names = names)
    grouped  = df.groupby(by = "Label",axis = 0)
    for df_UV,label in grouped:
        print("Label ",label,":",df_UV)


if __name__ == "__main__":
    points,userNames, gen_skills = returnAllVectors()   #get the vectors from the makeVectors file to start the clustering

    
    np.random.shuffle(points)   #shuffle samples
    k = int(sys.argv[1])    #the max range of number of clusters
    bestK = calculate_WSS(points, k)    #plot the WSS score for clustering from k = 1 from kmax
    labels = return_labels(points, bestK)   #get the labels vectors for the particular 
    write_to_df(labels,userNames,points)
    read_from_df()
    
    

