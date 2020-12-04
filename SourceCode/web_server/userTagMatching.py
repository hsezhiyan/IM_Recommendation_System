import sys
import pandas as pd
import numpy as np
import urllib
import pickle
from urllib.parse import urlparse
from operator import itemgetter
import random
import pickle


PROFILES = "data/NewUsers.csv"
VECTORFILE = "data/sampleUserVectors.pkl"
SKILLS  = "data/NewSkills.csv"
UNAME = 0
testUrlstring = "http://localhost:5000/search?skills=Self+Motivated&skills=Deployment+Automation+Tools&skills=Cloud+Applications"
DICT = {"App Dev".lower():0,"Database Management".lower():1,"Software Dev/Security".lower():2,"Cloud Computing".lower():3,"Web Dev".lower():4,"ML/Data Science".lower():5,"Basic Software/OS".lower():6,"Finance".lower():7,"Corporate Experience".lower():8,"Programming Languages".lower():9,"Communication".lower():10,"Hardware/Other".lower():11,"UX Design".lower():12}
f = open(VECTORFILE,"rb")
SKILLTAGS = [['AngularJS', 'Application Development', 'Mobile Applications'], ['Data Imports', 'Optimize Database', 'Database', 'Database Administration', 'Information Architecture', 'IT Optimization', 'Storage', 'Configure Database Software', 'Architecture', 'Data Storage', 'Servers', 'Big Data'], ['Deployment Automation Tools', 'IT Security', 'APIs', 'Design Specifications', 'Software Developer', 'Interaction Flows', 'IT Solutions', 'Software Development', 'Systems Software', 'Security', 'Information Systems', 'Open Source Technology Integration', 'Process Flows', 'Software Engineering'], ['Cloud Applications', 'Cloud Management Tools', 'Cloud-Based Visualizations', 'AWS', 'Amazon Web Services (AWS)', 'Cloud Systems Administration', 'Cloud Platforms', 'Deployment of Cloud Services', 'Cloud Services', 'Cloud Scalability', 'Cloud Maintenance Tasks', 'Utilizing Cloud Automation Tools', 'Cloud Hosting Services'], ['NodeJS', 'CSS', 'Web Development', 'Play Framework', 'Javascript', 'Web Technologies', 'Optimizing Website Performance', 'Wireframes', 'Twitter Bootstrap', 'Web Applications', 'EmberJS', 'ExpressJS', 'Web Design'], ['Data Intelligence', 'Data Science', 'Information Design', 'Data Analysis', 'Data Mining', 'Data Modeling', 'Data Visualizations', 'Analytics', 'Data Visualization Tools'], ['Linux', 'Metrics', 'Continuous Integration', 'Testing', 'Installation', 'Operations', 'User Testing', 'Design Principles', 'Troubleshooting', 'Operating Systems', 'Virtualization', 'Microsoft Office', 'Tech Skills', 'QA', 'File Systems', 'Agile Project Methodology', 'Integrated Technologies', 'Documentation', 'Configuration Management'], ['Business Intelligence', 'Analytical', 'Business Process Modeling', 'Data Strategy'], ['Messaging', 'User Research', 'Customer Support', 'Product Support', 'IT Support', 'Technical Support', 'Desktop Support', 'Google Analytics', 'Search Engine Optimization (SEO)', 'Web Analytics', 'Management', 'Team Building', 'Network Operations', 'Optimizing User Experiences', 'Identify User Needs', 'Team Oriented', 'Continuous Deployment', 'Content Management', 'Product Management', 'Project Management', 'Presentation', 'Product Design', 'Content Strategy', 'Review Existing Solutions', 'Product Training', 'Help Desk', 'Networking', 'Product Development', 'Business Analytics'], ['Java', 'C#', 'Languages', 'Python'], ['Critical Thinking', 'Communication', 'Reporting', 'Technical Writing'], ['Self Motivated', 'Motivation', 'Organization', 'Work Independently', 'Tools', 'Logical Thinking', 'Implementation', 'Configuration', 'Computer', 'Technology', 'Flexibility', 'IT Soft Skills', 'Hardware', 'Tablets', 'Prototyping Methods', 'Research Emerging Technology', 'Problem Solving', 'Self Starting', 'Leadership', 'Time Management', 'Teamwork', 'Training', 'Coding', 'Programming', 'Emerging Technologies'], ['Visual Design', 'Usability', 'Design Thinking', 'UI', 'User Interaction Diagrams', 'Interaction Design', 'Responsive Design', 'User Experience', 'User Flows', 'Front End Design', 'Design', 'Design Tools', 'User Interface', 'Design Prototypes', 'User-Centered Design', 'Touch Input Navigation']]
VECTORS = pickle.load(f)
NUM_FIELDS = 13



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

#Used to test similarity score distribution
def getScoreList(allMatchingUsers,weights,vectors):
	scores = {}
	similarityScores = []
	for user in allMatchingUsers:
		vector = np.array(vectors[user])
		score = np.multiply(vector,weights).sum()
		similarityScores.append(score) #Add to similarity score array
		scores[user] = score
	scores = sorted(scores.items(), key=itemgetter(1))
	users = [d[0] for d in scores]
	return (users, similarityScores)
#this finds all those user indices who have the common tags with the requested tags
#returns a dictionary of all indices in the data frame with the common set of tags
def findAllUsers(tags,allSkills,reqUser):
	indices = []
	##Changed during meeting 
	for k in allSkills.keys():
		#if k != reqUser:
		v = set(allSkills[k])
		intersect = list(tags & v)
		if intersect != []:
			indices.append({k:intersect})
		
	return indices


#if user in the database, then 
#returns all those users who have matching skills with the users in the database
def iterateTags(user,tags):
	
	dfProfile = pd.read_csv(PROFILES,header = 0).dropna()
	Users = dfProfile["User Name"].str.strip()
	dfProfile["Skills"] = dfProfile["Skills"].str.lower()
	dfProfile["Skills"] = dfProfile["Skills"].str.strip()
	allSkills = getAllskills(dfProfile)
	Users = Users.tolist()
	
	if user in Users:
		rowForUser = np.where(dfProfile["User Name"] == user)[0][0]
		allUserwithTags = findAllUsers(tags,allSkills,rowForUser)
		return allUserwithTags,rowForUser

	return [],-1

#Used to test similarity score distribution
def getSimilarityScores(tags):
	requestingUser = "Wallace Lim"
	tags = [tag.lower() for tag in tags]
	tagSet = set(tags)
	allMatchingUsers,_ = iterateTags(requestingUser,tagSet)
	allMatchingUsers = [list(d.keys())[0] for d in allMatchingUsers]
	weights = np.array(getWeightperField(tagSet))
	scores = getScoreList(allMatchingUsers,weights,VECTORS)
	return scores[1]
	
def testRandomTags():
	totalSimilarities = []
	for i in range(0,10000):
		currentTagList = []
		currentNumList = []
		while len(currentTagList) < 5 :
			randomIndex = random.randint(0,12)
			while randomIndex in currentNumList :
				randomIndex = random.randint(0,12)
			currentNumList.append(randomIndex)
			randomSkill = random.choice(SKILLTAGS[randomIndex])
			currentTagList.append(randomSkill)
			#if( in fieldsInTagList):
		print(i)
		print(currentTagList)
		totalSimilarities.extend(getSimilarityScores(currentTagList))

	print(totalSimilarities)
	return totalSimilarities
		#Create random tags
		#call getSimilarity Scores
	


def getRecommendations(tags):

	
	requestingUser = "Wallace Lim"
	tags = [tag.lower() for tag in tags]
	tagSet = set(tags)
	allMatchingUsers,_ = iterateTags(requestingUser,tagSet)
	allMatchingUsers = [list(d.keys())[0] for d in allMatchingUsers]
	weights = np.array(getWeightperField(tagSet))
	users = getScoreRank(allMatchingUsers,weights,VECTORS)
	return users


def main():
	print(getRecommendations(["Application Development","Database Administration","AngularJS"]))
	print(getRecommendations(["python"]))
	print(getSimilarityScores(["python"]))
	print(findSkill("python"))
	testList = testRandomTags()
	tempNumpyArray = np.asarray(testList)
	np.save("SimilarityScores.npy", tempNumpyArray)


if __name__ == '__main__':
	main()