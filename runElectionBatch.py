import numpy as np
from util import *
from runElection import *
from runBanditElection import *
import pickle

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

    ## which elections
    data = "India2004"

    ## number of runs 
    T = 10

    ## mistake probability
    alpha = 10**-1

    ## batch size
    batch = 500

    ## batch size for initial pulls of each constituency
    init_batch = batch

    algorithm = "LUCB"    

    constituenciesDecided = np.zeros(T)
    winners = np.zeros(T)
    totalVotesCounted = np.zeros(T)

    for t in range(T):

        print("Election  ", t)
        if algorithm == "LUCB":
            constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes = runBanditElectionLUCB(data, alpha, batch, init_batch)
        elif algorithm == "TwoLevelOpinionSurvey":
            constituenciesDecided[t], winners[t], totalVotesCounted[t], seenVotes = runElection(data, alpha, batch)
            
        with open(f"results/{data}/{algorithm}_seenVotes_{alpha}_{batch}_{t}.pkl", "wb") as output:
            pickle.dump(seenVotes, output)
    

    np.save(f"results/{algorithm}_{data}_constituenciesPolled_{alpha}_{batch}_{T}.npy", constituenciesDecided)

    np.save(f"results/{algorithm}_{data}_winnerIDs_{alpha}_{batch}_{T}.npy", winners)

    np.save(f"results/{algorithm}_{data}_totalVotesCounted _{alpha}_{batch}_{T}.npy", totalVotesCounted)

    print(f"Algorithm = {algorithm}, alpha = {alpha}, batch = {batch}, T = {T}")
    print("Constituencies decided = ", np.mean(constituenciesDecided), " +- ", np.std(constituenciesDecided)/np.sqrt(T))
    print("Votes counted = ", np.mean(totalVotesCounted), " +- ", np.std(totalVotesCounted)/np.sqrt(T))
    
if __name__ == "__main__":

    main()
