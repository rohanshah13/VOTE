import numpy as np
import pandas as pd
import os
import argparse
import json
from ortools.linear_solver import pywraplp

DATA_DIR = 'sample_data/{}'
OUTFILE = 'optimal/{}/result.txt'
OUT_PATH = 'optimal'
BJP = 'Bharatiya Janta Party'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--dataset', default='India2014')
	args = parser.parse_args()

	if not os.path.exists(OUT_PATH):
		os.mkdir(OUT_PATH)
	if not os.path.exists(os.path.join(OUT_PATH, args.dataset)):
		os.mkdir(os.path.join(OUT_PATH, args.dataset))

	dataset = DATA_DIR.format(args.dataset)

	#List of All Constituency Names
	listConstituencies = [x[:-4] for x in os.listdir(dataset)]
	N = len(listConstituencies)
	listParties = []
	listCosts = []
		
	#Loads the constituency level lists with the standings reversed, i.e. lowest votes first
	for filename in os.listdir(dataset):
		df = pd.read_csv(os.path.join(dataset,filename))
		parties = df["Party"].to_list()
		costs = df["MinSample"].to_list()
		parties.reverse()
		costs.reverse()
		listParties.append(parties)
		listCosts.append(costs)
	
	indexIndi = 0

	#Gives a unique name to each independent party
	for i, row in enumerate(listParties):
		for j, party in enumerate(row):
			if party == 'Independent':
				listParties[i][j] = f"Independent{indexIndi}"
				indexIndi += 1

	Parties = list(set([x for y in listParties for x in y]))
	Parties.sort()
	P = len(Parties)

	# print('Number of Constituencies = {}'.format(N))
	# print('Number of Parties = {}'.format(P))

	#count wins - number of constituencies each party has one
	countWins = [0 for i in range(P)]

	for standings in listParties:
		index = Parties.index(standings[-1])
		countWins[index] += 1
		for party in standings:
			party_index = Parties.index(party)

	#id of the winner of the election 
	winner_index = np.argmax(countWins)
	#party name of the winner of the election
	winner = Parties[winner_index]
	#ids of the constituency where the overall winner has won
	winner_constituencies = []

	for index, standings in enumerate(listParties):
		if standings[-1] == winner:
			winner_constituencies.append(index)

	solver = pywraplp.Solver.CreateSolver('SCIP')
	#x[i][j] is 1 if we choose to resolve the constituency i upto j parties. This implies that we know that the last j parties in i lost. If j = #parties in i, then we also know who won.
	#x[i][-1] is a dummy variable with cost 0 to handle all the parties who did not contest the constituency
	#this is for convenience of writing constraints
	x = {}
	for i,standings in enumerate(listParties):
		tmp = {}
		tmp[-1] = solver.IntVar(0, 1, 'x{},{}'.format(i, -1))
		for j, party in enumerate(standings):
			tmp[j] = solver.IntVar(0, 1, 'x{},{}'.format(i,j))
		x[i] = tmp

	#for each i, this ensures that there is exactly 1 j such that x[i][j] = 1
	for i,standings in enumerate(listParties):
		constraint = solver.RowConstraint(0,1,'')
		constraint.SetCoefficient(x[i][-1], 1)

		for j, party in enumerate(standings):
			constraint.SetCoefficient(x[i][j], 1)
	
	print('Number of constraints = {}'.format(solver.NumConstraints()))

	#for each party X (excpet the winner A) this does the following -
	#it enforces the constraint that UCB of X must be less than LCB of A
	#  i.e N - #losses_X < #wins_A -> #losses_X + #wins_A > N
	infinity = solver.infinity()
	for party_index, party in enumerate(Parties):
		if party == winner:
			continue
		constraint = solver.RowConstraint(N+1, infinity, '{}'.format(party))
		for i, standings in enumerate(listParties):
			if party not in standings:
				start = -1
			else:
				start = standings.index(party)
			end = len(standings)
			#if party X is winning a constituency, it does not help our objective
			if start == end - 1:
				continue
			for j in range(start,end):
				constraint.SetCoefficient(x[i][j], 1)
		#this coeffiecient is 2, since it implies both - A wins and X loses
		for c in winner_constituencies:
			num_parties = len(listParties[c])
			constraint.SetCoefficient(x[c][num_parties-1], 2)
	print('Number of constraints = {}'.format(solver.NumConstraints()))

	# the cost of x[i][j] is the number of samples required to resolve to that extent
	objective = solver.Objective()
	for i, costs in enumerate(listCosts):
		objective.SetCoefficient(x[i][-1], 0)
		for j, cost in enumerate(costs):
			objective.SetCoefficient(x[i][j], np.int(cost))
	objective.SetMinimization()

	status = solver.Solve()

	outfile = OUTFILE.format(args.dataset)
	f = open(outfile, 'w')

	#just printing results
	if status == pywraplp.Solver.OPTIMAL:
		print('Objective Value = ', solver.Objective().Value())
		print('Winner of the election is {}'.format(winner))
		f.write('Minimum required number of samples is {}\n'.format(solver.Objective().Value()))
		f.write('Winner of the election is {}\n'.format(winner))
		for i, standings in enumerate(listParties):
			num_parties = len(standings)
			found = False
			print_data = {}
			print_data['Constituency'] = listConstituencies[i]
			for j, party in enumerate(standings):
				if x[i][j].solution_value() == 1:
					print_data['Party'] = party
					position = num_parties - j
					print_data['Position'] = str(position)
					found = True
					break
					print('Resolve {} up to the party {} at position {}'.format(listConstituencies[i], party, position))
			if not found:
				print_data['Party'] = 'None'
				print_data['Position'] = str(-1)
			f.write(json.dumps(print_data) + '\n')
	else:
		print(status)
	
	f.close()


 

if __name__ == '__main__':
	main()