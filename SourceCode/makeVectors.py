import pandas as pd
import numpy as np
import sys
import pickle

#Name of the csv file with classification of skills into categories
skillClassificationFile = "./data/IMsample_data/NewSkills.csv"
#Name of the file username and skills for each person
userDataFile = "./data/IMsample_data/NewUsers.csv"

def returnAllVectors():
    #Create dataframe from the classified skills csv
    df = pd.read_csv(skillClassificationFile,header = 0)
    df = df.dropna()

    #Create lists from dataframe
    major_skills = list(df["General Skill"])
    sp_skills = list(df["Specific Skills"])

    specificSkillList = []
    for specificSkills in sp_skills:
        tempList = [x.strip() for x in specificSkills.split(',')]
        while '' in tempList:
            tempList.remove('')
        specificSkillList.append(tempList)
    
    print(specificSkillList)
    #Get skills of each person
    (userNames, eachPersonSkills) = csvToPeopleLists(userDataFile)
    #Get skillvectors of each person
    (userNames, allSkillVectors) = createVectorList(userNames, eachPersonSkills, major_skills, specificSkillList)

    allSkillVectors =  np.array(allSkillVectors)

    myDict = {}
    for (username,userSkillVector) in zip(userNames,allSkillVectors):
        myDict[username] = userSkillVector
    
    f = open("data/IMSample_data/sampleUserVectors.pkl","wb")
    pickle.dump(myDict,f)
    f.close()

    return (allSkillVectors, userNames, major_skills)

def createVectorList(userNames, eachPersonSkills, majorSkills, specificSkills):
    #Create list with tally of skills in each category
    allSkillVectors = []
    numInMajor = []
    for skillList in specificSkills :
        numInMajor.append(len(skillList))

    #Create tally of skills of each type for each person
    for skillList in eachPersonSkills:
        skillVector = []
        for specificSkillList in specificSkills:
            categoryTally = len(set(skillList).intersection(specificSkillList))
            skillVector.append(categoryTally)
        allSkillVectors.append(skillVector)
    normalizedVectors = []

    #Normalize the list between 0 and 1
    for skillVector in allSkillVectors:
        tempList = [a/b for a,b in zip(skillVector,numInMajor)]
        normalizedVectors.append(tempList)

    return (userNames, normalizedVectors)



# return tuple of lists of format (usernames, [skillsOfPerson1, skillsofPerson2])
def csvToPeopleLists(linkedinFileName):
    #Loading csv into pandas dataframe
    df = pd.read_csv(linkedinFileName,header = 0)
    df = df.dropna()
    
    #create list of usernames and list of skill lists
    userNames = list(np.array(df["User Name"]))
    listOfUserSkills = list(np.array(df["Skills"]))

    #Create list of each person's skills
    listOfEachSkills = []
    for skills_string in listOfUserSkills: 
        tempList = [x.strip() for x in skills_string.split(',')]
        while '' in tempList:
            tempList.remove('')
        listOfEachSkills.append(tempList)
    return (userNames, listOfEachSkills)

def main():
    returnAllVectors()
    # (allSkillVectors, userNames, gen_skills) = returnAllVectors()
    # print(allSkillVectors)
    # print(userNames)
    # print(gen_skills)
    

if __name__ == '__main__':
	main()

