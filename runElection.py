import numpy as np
import pandas as pd
from util import *
from simulate import *

def runElection(alpha, a = 1, b = 1):

    Parties = getPartyList("partyList.json")
    
    constituencies = getAllPlaces()

    C = len(constituencies)
    P = len(Parties)

    stoppingTimes = np.zeros(C)
    winners = (np.ones(C) * -1).astype(int)
    
    N = np.zeros(C+1)
    Nl = np.zeros((P, C + 1))
    Nu = np.ones((P, C + 1)) * C

    N[0] = C

    unseenConstituencies = np.arange(C)
    seenWins = np.zeros(P)

    i = 0
    separated = False
    separated_i = C

    totalVotesCounted = 0

    while N[i] > 0:

        c = np.random.choice(unseenConstituencies)
        
        print("Constituency ", c, ": ", constituencies[c])

        table = pd.read_csv("data/" + constituencies[c] + ".csv")

        data = table['Votes'].to_numpy()
        parties = table['Party'].to_list()


##        stoppingTimes[c], winners[c] = runExperiment(data, alpha, True, True, batch = 100)
        stoppingTimes[c], winners[c] = runOracleSearch(data, alpha / 2, True, True)
        winners[c] = Parties.index(parties[winners[c]])


        totalVotesCounted += stoppingTimes[c]
        seenWins[winners[c]] += 1
        unseenConstituencies = np.delete(unseenConstituencies, np.where(unseenConstituencies == c))

        i = i + 1
        N[i] = N[i-1] - 1

 

        for p in range(P):
            Nl[p, i], Nu[p, i] = binBounds(alpha/(2 * P), C, a, b, i, seenWins[p])

            ## intersection 
            Nl[p, i] = max(Nl[p, i-1], Nl[p, i])
            Nu[p, i] = min(Nu[p, i-1], Nu[p, i])


        winner = np.argmax(Nl[:, i])
        term = Nl[winner, i] - max(Nu[:, i][np.arange(len(Nu[:, i])) != winner])

        if i % (C//100) == 0:
            print(i, term, Parties[winner])

        if term > 0 and not separated:
            separated = True
            separated_i = i
                        
            print("Seperated at ", separated_i)
            print(Parties[winner], ", Seats won = ", seenWins[winner], ", Total votes counted = ", totalVotesCounted)

            return separated_i, winner, totalVotesCounted 

    return separate_i, winner, totalVotesCounted

if __name__ == "__main__":

    alpha = 10**-1

    stoppingC, winner, stoppingVotes = runElection(alpha)

    print(stoppingC, winner, stoppingVotes)
