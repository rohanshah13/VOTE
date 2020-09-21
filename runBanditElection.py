import numpy as np
import pandas as pd
from util import *

def choice(x):
    return np.random.choice(x)

def runBanditElection(alpha, batch = 1, a = 1, b = 1):

    Parties = getPartyList("partyList.json")
    
    constituencies = getAllPlaces()

    C = len(constituencies)
    P = len(Parties)

    stoppingTimes = np.zeros(C)
    winners = (np.ones(C) * -1).astype(int)


    listVotes = []
    listParties = []
    for c in range(C):
        table = pd.read_csv("data/" + constituencies[c] + ".csv")

        data = table['Votes'].to_list()
        parties = table['Party'].to_list()

        listVotes.append(data)
        listParties.append(parties)

    unseenVotes = listVotes
    seenVotes = [[0] * len(inner) for inner in listVotes]
        
    N = C

    
    Cl = np.zeros(P)
    Cu = np.ones(P) * C

    N0 = [sum(inner) for inner in listVotes]
    Nl = [[0] * len(inner) for inner in listVotes]
    Nu = [[sum(inner)] * len(inner) for inner in listVotes]
    

    seenWins = np.zeros(P)

    undecidedConstituencies = np.arange(C)

    i = 0
    separated = False
    separated_i = C

    while N > 0:
        
        c = choice(undecidedConstituencies)
        K = len(listParties[c])

        for _ in range(batch):

            norm = [float(i)/sum(unseenVotes[c]) for i in unseenVotes[c]]
            vote = np.random.multinomial(1, norm)
            
            unseenVotes[c] -= vote
            seenVotes[c] += vote

        for k in range(K):
            
            tempL, tempU = binBounds(alpha/(2*K*C), N0[c], a, b, sum(seenVotes[c]), seenVotes[c][k])

            Nl[c][k] = max(Nl[c][k], tempL)
            Nu[c][k] = min(Nu[c][k], tempU)

        constiWinner = np.argmax(Nl[c])

        constiTerm = Nl[c][constiWinner] - max([x for i,x in enumerate(Nu[c]) if i!=constiWinner])

        

        if constiTerm > 0:

            N = N - 1

            winPartyID = Parties.index(listParties[c][constiWinner])

            
            if N % 5 == 0:
                print(N, constituencies[c], Parties[winPartyID], sum(map(sum, seenVotes)), sum(seenVotes[c]))

            undecidedConstituencies = np.delete(undecidedConstituencies, np.where(undecidedConstituencies == c))

            seenWins[winPartyID] += 1

            for p in range(P):

                tempL, tempU = binBounds(alpha/(2 * P), C, a, b, sum(seenWins), seenWins[p])

                Cl[p] = max(Cl[p], tempL)
                Cu[p] = min(Cu[p], tempU)

            winner = np.argmax(Cl)

            term = Cl[winner] - max(Cu[np.arange(len(Cu)) != winner])

            if term > 0:
                totalVotesCounted = sum(map(sum, seenVotes))
                print("Decided constituencies = ", sum(seenWins))
                print(Parties[winner], ", Seats won = ", seenWins[winner], ", Total votes counted = ", totalVotesCounted)
                
                return sum(seenWins), winner, totalVotesCounted


            
if __name__ == "__main__":


    alpha = 10**-1
    batch = 1000

    stoppingC, winner, stoppingVotes = runBanditElection(alpha, batch)

    print(stoppingC, winner, stoppingVotes)
