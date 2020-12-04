import csv
import pandas as pd
import numpy as np 

INSIGHTS = "data/userinsights.csv"

class IMUser():
	def __init__(self, UserName, InsightsVector, PersonalityDistanceToRequestor):
		self.UserName = UserName
		self.InsightsVector = InsightsVector
		self.PersonalityDistanceToRequestor = PersonalityDistanceToRequestor


def read_csv_file(requesting_user_vector):
	all_users = []
	with open(INSIGHTS) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    first_row = True
	    for row in csv_reader:
	    	if first_row:
	    		first_row = False
	    		continue
	    	UserName = row[1]
	    	InsightsVector = row[2].strip("]")
	    	InsightsVector = InsightsVector.strip("[")
	    	InsightsVector = InsightsVector.split(" ")

	    	while("" in InsightsVector): 
    			InsightsVector.remove("") 

	    	FinalInsightsVector = [float(i) for i in InsightsVector]
	    	distance = np.linalg.norm(requesting_user_vector - FinalInsightsVector)

	    	newUser = IMUser(UserName, FinalInsightsVector, distance)

	    	all_users.append(newUser)

	return all_users 

def get_closest_personality_matches(requesting_user_vector):
	personalityProfiles = pd.read_csv(INSIGHTS,header = 0).dropna()

	all_users = read_csv_file(requesting_user_vector)
	all_users.sort(key=lambda x: x.PersonalityDistanceToRequestor)

	# top 25% best matches
	top_25_best_matches = [user.UserName for user in all_users[0:int(len(all_users) / 4)]]
	# print(len(top_25_best_matches))
	# print(len(all_users))

	# print(top_25_best_matches)
	return top_25_best_matches

if __name__ == "__main__":
	#print(read_csv_file())
	get_closest_personality_matches(np.random.rand(22))




