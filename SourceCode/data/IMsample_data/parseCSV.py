import pandas as pd
import sys


def parse_file(filename):
	df = pd.read_csv(filename,sep = ',',header = 0,names = ["id","skill","numberInt","type","isActive"])
	Skills = set(df["skill"].astype("U").to_numpy())

	for skill in Skills:
		print(skill)



def main():
	FILENAME = sys.argv[1]
	parse_file(FILENAME)


if __name__ == '__main__':
	main()