import json
import os
from os import listdir
from os.path import isfile, join

"""
Returns list of all files under the directory storing JSON files.
"""
def return_files_list(json_dir_path):
    onlyfiles = [f for f in listdir(json_dir_path) if isfile(join(json_dir_path, f))]
    return onlyfiles

"""
Function that takes in a path to the LinkedIn profiles in JSON format
and returns a .csv file with all skillsets associated with each user.
"""
def main(file_path, json_dir_path):
    files_list = return_files_list(json_dir_path)
    csv_file = open(file_path, "a")
    for json_file in files_list:
        json_file_path = os.path.join(json_dir_path, json_file)
        json_file = open(json_file_path)
        data = json.load(json_file)
        name = data["profileAlternative"]["name"]
        all_skills = data["skills"]

        if name == "" or len(all_skills) == 0:
            continue

        skills = ""
        for skill in data["skills"]:
            skills = skills + skill["title"] + ", "
        try:
            csv_file.write("\n\" {} \", \" {} \"".format(name.encode('UTF-8').strip(), skills))
        except:
            print("A profile caused an exception")

if __name__ == "__main__":
    main("data/currentScrappedData.csv", "data/crawledProfiles")
