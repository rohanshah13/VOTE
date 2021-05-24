import numpy as np
from util import *
from runElection import *
from runBanditElection import *
from runUniformElection import *
from runDCBElection import *
from runDCBElectionPrior import *
from runDCBElection_PPR1 import *
from runDCBElection_PPR2 import *
from runDCBElection_SE import *
from runDCBElection_GLR import *
from runUniformElection_SE import *
from runUniformElection_GLR import *
from runUniformElection1 import *
from runUniformElection_PPR2 import *
import pickle
import sys
import argparse
import os

TRACEFILE = 'results/{}/{}/trace/{}_{}_{}'
##def runDrawElectionBatch(T, alpha):
##
##    stoppingTimes = np.zeros(T)
##    winners = np.zeros(T)
##    totalVotesCounted = np.zeros(T)
##
##    for t in range(T):
##
##        print("Election  ", t)
##        stoppingTimes[t], winners[t], totalVotesCounted[t] = runElection(alpha)
##        
##    return stoppingTimes, winners.astype(int), totalVotesCounted
##
##def runBanditElectionBatch(T, alpha, batch):
##
##    stoppingTimes = np.zeros(T)
##    winners = np.zeros(T)
##    totalVotesCounted = np.zeros(T)
##
##    for t in range(T):
##
##        print("Election  ", t)
##        stoppingTimes[t], winners[t], totalVotesCounted[t] = runBanditElection(alpha, batch)
##        
##    return stoppingTimes, winners.astype(int), totalVotesCounted

def main():

	parser = argparse.ArgumentParser()

	parser.add_argument('--dataset',default='India2014')
	parser.add_argument('--algorithm', default='LUCB')

	args = parser.parse_args()
	## which elections
	data = args.dataset

	## number of runs 
	T = 10

	## mistake probability
	alpha = 10**-2

	## batch size
	batch = 200

	## batch size for initial pulls of each constituency
	init_batch = batch

	algorithm = args.algorithm

	constituenciesDecided = np.zeros(T)
	winners = np.zeros(T)
	totalVotesCounted = np.zeros(T)
	totalLabelledVotesCounted = np.zeros(T)
	seenVotes = [None for i in range(T)]
	listVotes = [None for i in range(T)]

	if not os.path.exists('results'):
		os.mkdir('results')
	if not os.path.exists('results/{}'.format(data)):
		os.mkdir('results/{}'.format(data))
	if not os.path.exists('results/{}/{}'.format(data,algorithm)):
		os.mkdir('results/{}/{}'.format(data,algorithm))
	if not os.path.exists('results/{}/{}/trace'.format(data,algorithm)):
		os.mkdir('results/{}/{}/trace'.format(data,algorithm))

	for t in range(0,T):
		np.random.seed(t)
		print("Election  ", t)
		tracefile = TRACEFILE.format(data,algorithm,alpha,batch,t)
		tracefile = 'temp.txt'
		if algorithm == "LUCB":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t] = runBanditElectionLUCB(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "Uniform":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t] = runUniformElection(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "U1":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runUniformElection1(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "U2":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runUniformElection_PPR2(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "USE":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runUniformElection_SE(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "UGLR":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runUniformElection_GLR(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "TwoLevelOpinionSurvey":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t] = runElection(data, alpha, tracefile, batch)
		elif algorithm == "DCB":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t] = runDCBElection(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "DCB_Prior":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t] = runDCBElectionPrior(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "DCB1":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runDCBElection_PPR1(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "DCB2":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runDCBElection_PPR2(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "DCBSE":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runDCBElection_SE(data, alpha, tracefile, batch, init_batch)
		elif algorithm == "DCBGLR":
			constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes[t], totalLabelledVotesCounted[t] = runDCBElection_GLR(data, alpha, tracefile, batch, init_batch)	
		# exit()

	C = len(seenVotes[0])
	constiVotes = np.zeros((T,C))
	for t in range(T):
		constiVotes[t,:] = np.asarray([sum(x) for x in seenVotes[t]])

	np.save('results/{}/{}/constituenciesPolled_{}_{}_{}'.format(data,algorithm,alpha,batch,T), constituenciesDecided)

	np.save('results/{}/{}/winnerIDs_{}_{}_{}'.format(data,algorithm,alpha,batch,T), winners)

	np.save('results/{}/{}/totalVotesCounted_{}_{}_{}'.format(data,algorithm,alpha,batch,T), totalVotesCounted)

	np.save('results/{}/{}/votesSeen_{}_{}_{}.npy'.format(data,algorithm,alpha,batch,T), constiVotes)

	print(f"Algorithm = {algorithm}, alpha = {alpha}, batch = {batch}, T = {T}")
	print("Constituencies decided = ", np.mean(constituenciesDecided), " +- ", np.std(constituenciesDecided)/np.sqrt(T))
	print("Votes counted (unlabelled)= ", np.mean(totalVotesCounted), " +- ", np.std(totalVotesCounted)/np.sqrt(T))
	if algorithm in ['U1', 'U2', 'USE', 'UGLR', 'DCB1', 'DCB2', 'DCBSE', 'DCBGLR']:
		print("Votes counted (labelled)= ", np.mean(totalLabelledVotesCounted), " +- ", np.std(totalLabelledVotesCounted)/np.sqrt(T))
	
if __name__ == "__main__":

	main()
