import numpy as np
import pandas as pd
from util import *
from simulate import *

def runElection(data, alpha, batch = 1, a = 1, b = 1):

    constituencies = getAllPlaces(f"data/{data}/")

    C = len(constituencies)

    stoppingTimes = np.zeros(C)
    winners = (np.ones(C) * -1).astype(int)

    listVotes = []
    listParties = []
    listPartyIDs = []
    
    for c in range(C):
        table = pd.read_csv(f"data/{data}/{constituencies[c]}.csv")

        votes = table['Votes'].to_list()
        parties = table['Party'].to_list()
        
        listVotes.append(votes)
        listParties.append(parties)    
    
    indexIndi = 0
    for i, row in enumerate(listParties):
        for j, party in enumerate(row):
            if party == 'Independent':
                listParties[i][j] = f"Independent{indexIndi}"
                indexIndi += 1

                

    Parties = list(set([x for y in listParties for x in y]))
    Parties.sort()

    P = len(Parties)
    
    listPartyIDs = [[Parties.index(k) for k in row] for row in listParties]
            

    try:
        listVotes = [[int(inner.replace(',', ''))for inner in outer] for outer in listVotes]
    except:
        pass

    seenVotes = [[0] * len(inner) for inner in listVotes]
    
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
        


        votes = listVotes[c]
        parties = listParties[c]


##        stoppingTimes[c], winners[c] = runExperiment(votes, alpha, True, True, batch = 100)
        stoppingTimes[c], winners[c], seenVotes[c] = runOracleSearch(votes, alpha / (2 * C), batch)
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

        if i % (C//10) == 0:
            print(i, term, Parties[winner])

        if term > 0 and not separated:
            separated = True
            separated_i = i
                        
            print("Decided Constituencies = ", separated_i)
            print(Parties[winner], ", Seats won = ", seenWins[winner], ", Total votes counted = ", totalVotesCounted)

            return separated_i, winner, totalVotesCounted, seenVotes

    return separate_i, winner, totalVotesCounted, seenVotes

if __name__ == "__main__":

    data = "Delhi2015"
    
    alpha = 10**-1

    stoppingC, winner, stoppingVotes, seenVotes = runElection(data, alpha)

    print(stoppingC, winner, stoppingVotes)
