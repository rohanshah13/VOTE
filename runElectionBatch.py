import numpy as np
from util import *
from runElection import *
from runBanditElection import *

def runDrawElectionBatch(T, alpha):

    stoppingTimes = np.zeros(T)
    winners = np.zeros(T)
    totalVotesCounted = np.zeros(T)

    for t in range(T):

        print("Election  ", t)
        stoppingTimes[t], winners[t], totalVotesCounted[t] = runElection(alpha)
        
    return stoppingTimes, winners.astype(int), totalVotesCounted

def runBanditElectionBatch(T, alpha, batch):

    stoppingTimes = np.zeros(T)
    winners = np.zeros(T)
    totalVotesCounted = np.zeros(T)

    for t in range(T):

        print("Election  ", t)
        stoppingTimes[t], winners[t], totalVotesCounted[t] = runBanditElection(alpha, batch)
        
    return stoppingTimes, winners.astype(int), totalVotesCounted

def main():
 
    T = 10
    alpha = 10**-1
    batch = 100

    ## BJP
    W = 85
    
    constituenciesPolled, winners, totalVotesCounted = runBanditElectionBatch(T, alpha, batch)

    # np.save(f"results/metaOS_constituenciesPolled_{alpha}_{T}.npy", constituenciesPolled)

    # np.save(f"results/metaOS_winnerIDs_{alpha}_{T}.npy", winners)

    # np.save(f"results/metaOS_totalVotesCounted _{alpha}_{T}.npy", totalVotesCounted)

    np.save(f"results/randBandit_{batch}_constituenciesPolled_{alpha}_{T}.npy", constituenciesPolled)

    np.save(f"results/randBandit_{batch}_winnerIDs_{alpha}_{T}.npy", winners)

    np.save(f"results/randBandit_{batch}_totalVotesCounted _{alpha}_{T}.npy", totalVotesCounted)

    print("For alpha = ", alpha, ", Constituencies polled = ", np.mean(constituenciesPolled), " +- ", np.std(constituenciesPolled)/np.sqrt(T))
    print("Votes counted = ", np.mean(totalVotesCounted), " +- ", np.std(totalVotesCounted)/np.sqrt(T))
    print("Accuracy = ", 100 * np.sum(winners == W) / T, "%")
    
if __name__ == "__main__":

    main()
