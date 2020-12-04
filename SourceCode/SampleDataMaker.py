import TagParser as tagParser

allSkills = tagParser.read_files("./data/IMsample_data/NewSkills.csv", secondName="Specific Skills")
#Save vectors into numpy file
print(allSkills)

#change makeVectors to return dictionary that is keyed based on name of user and value - vector


