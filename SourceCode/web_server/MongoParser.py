import pymongo
import json
from pymongo import MongoClient
from bson import BSON
from bson import json_util
from bson.json_util import dumps

client = MongoClient('18.191.78.146:27017',
	username='ImS_Im_QA_DEv_UsEr',
	password='a+7swY8Ql103nYJn128nMOodu8a20js',
	authSource='admin',
	authMechanism='SCRAM-SHA-1')
db = client['IMS-R']
skillCollection = db['skillmasters']
userCollection = db['users']
skillCategoriesCollection = db['skillcategorymasters']

def jsonParser(doc):
	return dumps(doc, default=json_util.default)

#return name of the skill based on the hash
def processTags(skillsetObject):
	skillSet = []
	for skill in skillsetObject:
		skillQuery = skillCollection.find_one({"_id" : {"$eq" : skill}}, {"name" : 1})
		skillSet.append(skillQuery["name"])

	return skillSet

#parse the category hash in each skill
def processSkills(categoryObject):
	skillCategories = skillCategoriesCollection.distinct("name")
	specificSkills = skillCollection.find({"$and": [{"category" : {"$eq" : categoryObject['_id']}}, {"name" : {"$exists" : True}}]}, {"name" : 1})

	skillRow = []
	for specificSkill in specificSkills:
		skillRow.append(specificSkill["name"])

	return skillRow

#create csv
def generateSkills():
	skillCategories = skillCategoriesCollection.find({"_id" : {"$exists" : True}}, {"name" : 1})
	categories = []
	categories.append(["General Skill", "Specific Skills"])

	for skillCategory in skillCategories:
		row = []
		row.append(skillCategory["name"])
		row.append(processSkills(skillCategory))
		categories.append(row)

	with open("skills.json", 'w', newline='') as f:
		dict_categories = {}
		for category in categories[1:]:
			dict_categories[category[0]] = category[1]

	return dict_categories

def userCollect():
	skills = skillCollection.distinct("name")
	users = userCollection.find({"$and" : [{"_id" : {"$exists" : True}}, {"skillset" : {"$exists" : True}}]}, {"skillset": 1})
	
	generateSkills()
	
	userAr = []
	for user in users:
		data = {}
		data["_id"] = str(user["_id"])
		data["skillset"] = processTags(user["skillset"])
		userAr.append(data)

	return userAr

if __name__ == '__main__':
	print(generateSkills())





