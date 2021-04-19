import numpy as np
import os
import shutil
import argparse

DATA_DIR = 'data/TriData3/'
P1 = 'A'
P2 = 'B'
P3 = 'C'
C = 200
POPULATION = 100000
PARTIES = ['A','B','C']

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--seed',default=0)
	args = parser.parse_args()
	seed = args.seed
	np.random.seed(seed)
	if os.path.exists(DATA_DIR):
		shutil.rmtree(DATA_DIR)
	os.mkdir(DATA_DIR)
	wins = np.zeros(3)
	p = np.zeros((C,3))
	for c in range(C):
		if c < 20:
			p[c,0] = np.random.uniform(0.40,0.60)
			p[c,1] = np.random.uniform(0.20,0.40)
			p[c,2] = np.random.uniform(0.25,0.35)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 40:
			p[c,0] = np.random.uniform(0.40,0.60)
			p[c,1] = np.random.uniform(0.15,0.25)
			p[c,2] = np.random.uniform(0.25,0.33)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 60:
			p[c,0] = np.random.uniform(0.35,0.45)
			p[c,1] = np.random.uniform(0.2,0.4)
			p[c,2] = np.random.uniform(0.2,0.4)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 80:
			p[c,0] = np.random.uniform(0.35,0.45)
			p[c,1] = np.random.uniform(0.2,0.4)
			p[c,2] = np.random.uniform(0.2,0.4)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 96:
			p[c,1] = np.random.uniform(0.35,0.45)
			p[c,0] = np.random.uniform(0.3,0.4)
			p[c,2] = np.random.uniform(0.2,0.3)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 112:
			p[c,1] = np.random.uniform(0.35,0.45)
			p[c,0] = np.random.uniform(0.2,0.4)
			p[c,2] = np.random.uniform(0.3,0.4)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 126:
			p[c,1] = np.random.uniform(0.40,0.60)
			p[c,0] = np.random.uniform(0.2,0.4)
			p[c,2] = np.random.uniform(0.25,0.35)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 140:
			p[c,1] = np.random.uniform(0.40,0.60)
			p[c,0] = np.random.uniform(0.25,0.35)
			p[c,2] = np.random.uniform(0.2,0.4)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 156:
			p[c,2] = np.random.uniform(0.35,0.45)
			p[c,1] = np.random.uniform(0.3,0.4)
			p[c,0] = np.random.uniform(0.2,0.3)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 172:
			p[c,2] = np.random.uniform(0.35,0.45)
			p[c,1] = np.random.uniform(0.2,0.4)
			p[c,0] = np.random.uniform(0.3,0.4)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 186:
			p[c,2] = np.random.uniform(0.40,0.60)
			p[c,1] = np.random.uniform(0.2,0.4)
			p[c,0] = np.random.uniform(0.25,0.35)
			p[c,:] = p[c,:]/np.sum(p[c,:])
		elif c < 200:
			p[c,2] = np.random.uniform(0.40,0.60)
			p[c,1] = np.random.uniform(0.25,0.35)
			p[c,0] = np.random.uniform(0.2,0.4)
			p[c,:] = p[c,:]/np.sum(p[c,:])

	np.random.shuffle(p)
	for c in range(C):
		OUTFILE = '{}{}.csv'.format(DATA_DIR,c)
		with open(OUTFILE,'w+') as f:
			f.write('"Position","Candidate Name","Votes","Votes %","Party"\n')
			votesA = int(p[c,0]*POPULATION)
			votesB = int(p[c,1]*POPULATION)
			votesC = POPULATION - votesA - votesB
			votes = [votesA, votesB, votesC]
			order = np.flip(np.argsort(p[c,:]))
			position = 1
			wins[order[0]] += 1
			for index in order:
				f.write('{},{},{},{}%,{}\n'.format(str(position),'X',votes[index],p[c,index]*100,PARTIES[index]))
				position += 1				
	print(wins)
if __name__ == '__main__':
	main()