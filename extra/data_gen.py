import numpy as np
import os
import shutil
import argparse

DATA_DIR = 'data/Hard-Easy/'
P1 = 'A'
P2 = 'B'
# P3 = 'C'
C = 500
POPULATION = 10**6
PARTIES = ['X','Y']

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--seed',default=0)
	args = parser.parse_args()
	seed = args.seed
	np.random.seed(seed)
	if os.path.exists(DATA_DIR):
		shutil.rmtree(DATA_DIR)
	os.mkdir(DATA_DIR)
	wins = np.zeros(2)
	p = np.zeros((C,2))
	for c in range(C):
		if c < 260:
			p[c,0] = np.random.uniform(0.51,0.9)
			p[c,1] = 1 - p[c,0]
		else:
			p[c,1] = np.random.uniform(0.51,0.9)
			p[c,0] = 1 - p[c,1]

	np.random.shuffle(p)
	for c in range(C):
		OUTFILE = '{}{}.csv'.format(DATA_DIR,c)
		with open(OUTFILE,'w+') as f:
			f.write('"Position","Candidate Name","Votes","Votes %","Party"\n')
			votesA = int(p[c,0]*POPULATION)
			votesB = POPULATION - votesA
			votes = [votesA, votesB]
			order = np.flip(np.argsort(p[c,:]))
			position = 1
			wins[order[0]] += 1
			for index in order:
				f.write('{},{},{},{}%,{}\n'.format(str(position),'NA',votes[index],p[c,index]*100,PARTIES[index]))
				position += 1				
	print(wins)
if __name__ == '__main__':
	main()