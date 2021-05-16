import numpy as np 
import pandas as pd
import argparse
import json
from util import *

INFILE = 'optimal/{}/result.txt'
DATA_DIR = 'data/{}'

CONGRESS = "Indian National Congress"
BJP = "Bharatiya Janta Party"

def main():
	parser = argparse.ArgumentParser()
	
	parser.add_argument('--dataset', default='India2004')

	args = parser.parse_args()
	dataset = args.dataset

	infile = INFILE.format(dataset)
	data_dir = DATA_DIR.format(dataset)

	results = {}
	with open(infile) as f:
		next(f)
		next(f)
		for line in f:
			line = json.loads(line)
			results[line["Constituency"]] = int(line["Position"])

	constituencies = getAllPlaces(data_dir)
	C = len(constituencies)

	listParties = []
	listVotes = []
	for c in range(C):
		table = pd.read_csv('data/{}/{}.csv'.format(dataset, constituencies[c]))

		#List of votes per party for the constituency c
		try:
			table['Votes'] = table['Votes'].str.replace(',','')
		except:
			pass
		votes = list(map(int,table['Votes'].to_list()))
		#List of parties for the constituency c
		parties = table['Party'].to_list()
		
		listVotes.append(votes)
		listParties.append(parties)    

	indexIndi = 0
	for i, row in enumerate(listParties):
		for j, party in enumerate(row):
			if party == 'Independent':
				listParties[i][j] = f"Independent{indexIndi}"
				indexIndi += 1

				
	#A sorted list(no duplicates) of parties
	Parties = list(set([x for y in listParties for x in y]))
	Parties.sort()

	indexCongress = Parties.index(CONGRESS)
	indexBJP = Parties.index(BJP)
	#Number of parties
	P = len(Parties)

	LCB = np.zeros(P)
	UCB = np.ones(P)*C

	for p in range(P):
		UCB[p] = sum(row.count(Parties[p]) for row in listParties)
	
	for constituency, position in results.items():
		indexC = constituencies.index(constituency)
		position -= 1
		consti_parties = listParties[indexC]
		if position < 0:
			continue
		print(constituency,position)
		for consti_position, party in enumerate(consti_parties[position:]):
			consti_position += position
			indexP = Parties.index(party)
			if consti_position == 0:
				LCB[indexP] += 1
			else:
				UCB[indexP] -= 1
		

	
	print(np.sort(UCB)[-5:])
	print(np.sort(LCB)[-5:])
	print(indexCongress)
	print(indexBJP)
	print(UCB[indexCongress])
	print(UCB[indexBJP])
	print(LCB[indexCongress])
	print(LCB[indexBJP])

	

	




if __name__ == '__main__':
	main()