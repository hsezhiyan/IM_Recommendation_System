import pandas as pd
import numpy as np
import sys

#function to read the file
##Provide name of second column as secondName
def read_files(filename, secondName="Skills"):
	df = pd.read_csv(filename,header = 0)	#the file name should be passed in as the command line argument
	df = df.dropna()	#remove all the NA samples
	print(df.shape)		#get the size of the dataframe
	skills = np.array(df[secondName])	#extract skills
	ALL_skills = []
	for skill in skills:
		skill = skill.replace(", ",",")	#remove extra space after comma as skills are comma seperated values
		skill.strip()	#remove extra spaces
		
			
		set_skills = [sk for sk in skill.split(',') if sk != '']

		ALL_skills.extend(set_skills)


	ALL_skills = set(ALL_skills)
	print("number of different skills: ",len(ALL_skills))
	return ALL_skills

def main():
	All_skills = read_files(sys.argv[1])



if __name__ == '__main__':
	main()
