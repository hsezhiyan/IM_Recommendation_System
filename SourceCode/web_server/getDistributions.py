import matplotlib.pyplot as plt
import numpy as np


FILENAME = "SimilarityScores.npy"
BINS = 100

def printStats(sorted_scores):
	print(len(sorted_scores)," number of samples")
	print(min(sorted_scores)," is the minimum score within the collection")
	print(max(sorted_scores)," is the maximum score within the collection")
	print(np.mean(sorted_scores)," is the mean score within the collection")

def main():
	scores = np.load(FILENAME)
	sorted_scores = sorted(scores)
	
	printStats(sorted_scores)

	plt.hist(scores, bins=BINS)
	plt.xlabel("Scores")
	plt.ylabel("Frequency")
	plt.title("Distribution of the scores")
	plt.show()




if __name__ == '__main__':
	main()