import sys
import pandas as pd
import numpy as np
import urllib
import pickle
import random

from urllib.parse import urlparse
from operator import itemgetter

from personality_cs_reading import get_closest_personality_matches

PROFILES = "data/IMsample_data/NewUsers.csv"
VECTORFILE = "data/IMsample_data/sampleUserVectors.pkl"
SKILLS  = "data/IMsample_data/NewSkills.csv"
INSIGHTS = "data/userinsights.csv"
UNAME = 0
testUrlstring = "http://localhost:5000/search?skills=Self+Motivated&skills=Deployment+Automation+Tools&skills=Cloud+Applications"
DICT = {"App Dev".lower():0,"Database Management".lower():1,"Software Dev/Security".lower():2,"Cloud Computing".lower():3,"Web Dev".lower():4,"ML/Data Science".lower():5,"Basic Software/OS".lower():6,"Finance".lower():7,"Corporate Experience".lower():8,"Programming Languages".lower():9,"Communication".lower():10,"Hardware/Other".lower():11,"UX Design".lower():12}
f = open(VECTORFILE,"rb")
VECTORS = pickle.load(f)
NUM_FIELDS = 13


def stringURLtoList(urlstring):
    (scheme, location, path, query, identifier) = urllib.parse.urlsplit(urlstring)
    primKey = scheme + "://" + location + path + "?" + "skills"
    secondKey = "skills"
    myDict = urllib.parse.parse_qs(urlstring)
    queries = []
    firstSkill = myDict[primKey]
    secondarySkills = myDict[secondKey]
    queries.append(firstSkill[0])
    for secondarySkill in secondarySkills:
        queries.append(secondarySkill)
    print(queries)
    return queries

#this returns a dictionary of username as keys and the list of all their all tags as a list as values
def getAllskills(dfProfile):
	allSkills = {}
	for i,skill in enumerate(dfProfile["Skills"].tolist()):
		user = dfProfile.iloc[i]["User Name"]
		allSkills[user] = skill.split(', ')

	return allSkills


def findSkill(tag):
	df = pd.read_csv(SKILLS,header = 0,sep = ',')
	GenSkills = df["General Skill"].str.lower().tolist()
	specSkills = df["Specific Skills"].str.lower().tolist()
	df = df.dropna()

	for gen,spec in zip(GenSkills,specSkills):
		spec = spec.split(",")
		if tag in spec:
			return gen

	return None




def getWeightperField(tags):
	
	weights = np.zeros(NUM_FIELDS)
	fieldDict = {}
	numTags = len(tags)
	for tag in tags:
		fieldSkill = findSkill(tag)
		fieldDict[tag] = fieldSkill
		weights[DICT[fieldSkill]] += (1/numTags)

	return weights


def getScoreRank(allMatchingUsers,weights,vectors):
	scores = {}
	for user in allMatchingUsers:
		vector = np.array(vectors[user])
		score = np.multiply(vector,weights).sum()
		scores[user] = score

	scores = sorted(scores.items(), key=itemgetter(1))
	users = [d[0] for d in scores]
	return users

	

#this finds all those user indices who have the common tags with the requested tags
#returns a dictionary of all indices in the data frame with the common set of tags
def findAllUsers(tags,allSkills,reqUser):
	indices = []

	for k in allSkills.keys():
		if k != reqUser:
			v = set(allSkills[k])
			intersect = list(tags & v)
			if intersect != []:
				indices.append({k:intersect})
		
	return indices


#if user in the database, then 
#returns all those users who have matching skills with the users in the database
def iterateTags(user,tags):
	
	dfProfile = pd.read_csv(PROFILES,header = 0).dropna()
	print(dfProfile)
	Users = dfProfile["User Name"].str.strip()
	dfProfile["Skills"] = dfProfile["Skills"].str.lower()
	dfProfile["Skills"] = dfProfile["Skills"].str.strip()
	allSkills = getAllskills(dfProfile)
	Users = Users.tolist()

	# insights_file = open("data/userInsights.csv", "w")
	# for user in Users:
	# 	insights_file.write(str(np.random.randint(10000)))# , user, np.random.rand(22)))
	# 	insights_file.write(",")
	# 	insights_file.write(user)
	# 	insights_file.write(",")
	# 	vector = str(np.random.rand(22)).rstrip("\n")
	# 	print(vector)
	# 	insights_file.write(vector)
	# 	insights_file.write("\n")

	if user in Users:
		rowForUser = np.where(dfProfile["User Name"] == user)[0][0]
		allUserwithTags = findAllUsers(tags,allSkills,rowForUser)
		return allUserwithTags,rowForUser

	return [],-1


def getRecommendations(tags):

	
	requestingUser = "Wallace Lim"
	requestingUserPersonality = np.random.rand(22)
	tags = [tag.lower() for tag in tags]
	tagSet = set(tags)
	allMatchingUsers,_ = iterateTags(requestingUser,tagSet)
	allMatchingUsers = [list(d.keys())[0] for d in allMatchingUsers]
	weights = np.array(getWeightperField(tagSet))
	users = getScoreRank(allMatchingUsers,weights,VECTORS)

	top_25_personality_matches = get_closest_personality_matches(requestingUserPersonality)

	filtered_users = [user for user in users if user in top_25_personality_matches]

	if len(filtered_users) < 5:
		return users
	else:
		return filtered_users


def main():
	print(getRecommendations(["Application Development","Database Administration","AngularJS"]))

if __name__ == '__main__':
	main()



