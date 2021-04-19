import numpy as np
import matplotlib.pyplot as plt
from util import *
import pandas as pd

DATA_DIR = 'data/{}'


def main():
	dataset = 'India2014'
	constituencies = getAllPlaces(f"data/{dataset}/")                              

	C = len(constituencies)

	population = np.zeros(C)

	for c in range(C):
		table = pd.read_csv(f"data/{dataset}/{constituencies[c]}.csv")

		table['Votes'] = table['Votes']

		#List of votes per party for the constituency c
		votes = list(map(int,table['Votes'].to_list()))
		#List of parties for the constituency c
		population[c] = sum(votes)

	print(sorted(population))
if __name__ == '__main__':
	main()