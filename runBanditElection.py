import numpy as np
import pandas as pd
from util import *


def randChoice(x):
    
    return np.random.choice(x)

## LUCB inspired algorithm
            
def runBanditElectionLUCB(data, alpha, batch = 1, init_batch = 1, a = 1, b = 1):
    
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
    
    unseenVotes = listVotes
    seenVotes = [[0] * len(inner) for inner in listVotes]
        
    N = C
    
    Cl = np.zeros(P)
    Cu = np.ones(P) * C

    for p in range(P):
        
        Cu[p] = sum(row.count(Parties[p]) for row in listParties)

    N0 = [sum(inner) for inner in listVotes]
    Nl = [[0] * len(inner) for inner in listVotes]
    Nu = [[sum(inner)] * len(inner) for inner in listVotes]
    

    seenWins = np.zeros(P)

    undecidedConstituencies = np.arange(C)

    leadingParty = np.zeros(C)

    for c in range(C):

        K = len(listParties[c])
        indexC = np.where(undecidedConstituencies == c)

        for _ in range(init_batch):
            norm = [float(i)/sum(unseenVotes[c]) for i in unseenVotes[c]]
            # print(constituencies[c], unseenVotes[c], norm)
            vote = np.random.multinomial(1, norm)
            
            unseenVotes[c] -= vote
            seenVotes[c] += vote

        for k in range(K):
            
            tempL, tempU = binBounds(alpha/(K*C), N0[c], a, b, sum(seenVotes[c]), seenVotes[c][k])

            Nl[c][k] = max(Nl[c][k], tempL)
            Nu[c][k] = min(Nu[c][k], tempU)

        
        constiWinner = np.argmax(seenVotes[c])

        constiTerm = Nl[c][constiWinner] - max([x for i,x in enumerate(Nu[c]) if i!=constiWinner])

        leadingParty[indexC] = Parties.index(listParties[c][constiWinner])

        if constiTerm > 0:

            N = N - 1
         
            winPartyID = int(leadingParty[indexC])
            
            leadingParty = np.delete(leadingParty, indexC)
            undecidedConstituencies = np.delete(undecidedConstituencies, indexC)

            seenWins[winPartyID] += 1

            for p in range(P):

                Cl[p] = seenWins[p]
                Cu[p] = seenWins[p]

                for ci in undecidedConstituencies:
                    if p in listPartyIDs[ci]:
                        pIndex = listPartyIDs[ci].index(p)
                        if Nu[ci][pIndex] > max(Nl[ci]):
                            Cu[p] += 1

            winner = np.argmax(Cl)

            term = Cl[winner] - max(Cu[np.arange(len(Cu)) != winner])

            
            if N % 5 == 0:

                print(N, constituencies[c], Parties[winPartyID], sum(map(sum, seenVotes)), sum(seenVotes[c]))
                print(Cl[winner], max(Cu[np.arange(len(Cu)) != winner]))
                      
            if term > 0:

                totalVotesCounted = sum(map(sum, seenVotes))
                print("Decided constituencies = ", sum(seenWins))
                print(Parties[winner], ", Seats won = ", seenWins[winner], ", Total votes counted = ", totalVotesCounted)
                
                return sum(seenWins), winner, totalVotesCounted, seenVotes

    while N > 0:

        countWinning = np.array([np.count_nonzero(leadingParty == p) for p in range(P)])

        for p in range(P):

            Cl[p] = seenWins[p]
            Cu[p] = seenWins[p]

            for ci in undecidedConstituencies:
                if p in listPartyIDs[ci]:
                    pIndex = listPartyIDs[ci].index(p)
                    if Nu[ci][pIndex] > max(Nl[ci]):
                        Cu[p] += 1
            

##        pb, pa = np.argsort(countWinning + seenWins)[-2:]

        pa = np.argmax(countWinning + seenWins)

        idx = np.arange(P)
        a1 = np.delete(idx, pa)
        a2 = np.argmax(np.delete(Cu, pa))
        
        pb = a1[a2]
        
        
        aUCB = np.zeros(C)

        for c in undecidedConstituencies:

            if pa in listPartyIDs[c]:

                paIndex = listPartyIDs[c].index(pa)
                
                aUCB[c] = Nu[c][paIndex] / N0[c]


        if max(aUCB) == 0:
            print("Random A")
            c = randChoice(undecidedConstituencies)
        else:
            c = np.argmax(aUCB)
        
        indexC = np.where(undecidedConstituencies == c)

        K = len(listParties[c])

        for _ in range(batch):

            norm = [float(i)/sum(unseenVotes[c]) for i in unseenVotes[c]]
            # print(constituencies[c], unseenVotes[c], norm)
            vote = np.random.multinomial(1, norm)
            
            unseenVotes[c] -= vote
            seenVotes[c] += vote

        for k in range(K):
            
            tempL, tempU = binBounds(alpha/(K*C), N0[c], a, b, sum(seenVotes[c]), seenVotes[c][k])

            Nl[c][k] = max(Nl[c][k], tempL)
            Nu[c][k] = min(Nu[c][k], tempU)

        constiWinner = np.argmax(seenVotes[c])

        constiTerm = Nl[c][constiWinner] - max([x for i,x in enumerate(Nu[c]) if i!=constiWinner])

        

        leadingParty[indexC] = Parties.index(listParties[c][constiWinner])

        if constiTerm > 0:

            N = N - 1
         
            winPartyID = int(leadingParty[indexC])
            
            leadingParty = np.delete(leadingParty, indexC)
            undecidedConstituencies = np.delete(undecidedConstituencies, indexC)

            seenWins[winPartyID] += 1

            for p in range(P):

                Cl[p] = seenWins[p]
                Cu[p] = seenWins[p]

                for ci in undecidedConstituencies:
                    if p in listPartyIDs[ci]:
                        pIndex = listPartyIDs[ci].index(p)
                        if Nu[ci][pIndex] > max(Nl[ci]):
                            Cu[p] += 1

            winner = np.argmax(Cl)

            term = Cl[winner] - max(Cu[np.arange(len(Cu)) != winner])

            
            if N % 5 == 0:

##                print("*")
##                print(np.argsort(seenWins + countWinning)[-4:], sum(seenWins) + len(leadingParty))
##                print("**")
##                print(Cu[np.argsort(seenWins + countWinning)[-4:]], Cl[np.argsort(seenWins + countWinning)[-4:]])
##                print("***")
##                print(seenWins[np.argsort(seenWins + countWinning)[-4:]], countWinning[np.argsort(seenWins + countWinning)[-4:]])
##

                print(pa, pb)
                print(N, constituencies[c], Parties[winPartyID], sum(map(sum, seenVotes)), sum(seenVotes[c]))
                print(Cl[winner], max(Cu[np.arange(len(Cu)) != winner]))
                      
            if term > 0:

                totalVotesCounted = sum(map(sum, seenVotes))
                print("Decided constituencies = ", sum(seenWins))
                print(Parties[winner], ", Seats won = ", seenWins[winner], ", Total votes counted = ", totalVotesCounted)
                
                return sum(seenWins), winner, totalVotesCounted, seenVotes


##        countWinning = np.array([np.count_nonzero(np.array(leadingParty) == p) for p in range(P)])

        bLCB = np.ones(C)

        for c in undecidedConstituencies:

            if pb in listPartyIDs[c]:
                pbIndex = listPartyIDs[c].index(pb)
                if Nu[c][pbIndex] > max(Nl[c]):
                    bLCB[c] = Nl[c][pbIndex] / N0[c]

        if min(bLCB) == 1:
            print("Random B")
            c = randChoice(undecidedConstituencies)
            
        else:
            c = np.argmin(bLCB)

        indexC = np.where(undecidedConstituencies == c)

        K = len(listParties[c])

        for _ in range(batch):

            norm = [float(i)/sum(unseenVotes[c]) for i in unseenVotes[c]]
            # print(constituencies[c], unseenVotes[c], norm)
            vote = np.random.multinomial(1, norm)
            
            unseenVotes[c] -= vote
            seenVotes[c] += vote

        for k in range(K):
            
            tempL, tempU = binBounds(alpha/(K*C), N0[c], a, b, sum(seenVotes[c]), seenVotes[c][k])

            Nl[c][k] = max(Nl[c][k], tempL)
            Nu[c][k] = min(Nu[c][k], tempU)

        constiWinner = np.argmax(seenVotes[c])

        constiTerm = Nl[c][constiWinner] - max([x for i,x in enumerate(Nu[c]) if i!=constiWinner])

        leadingParty[indexC] = Parties.index(listParties[c][constiWinner])

        if constiTerm > 0:

            N = N - 1
            
            winPartyID = int(leadingParty[indexC])
            
            leadingParty = np.delete(leadingParty, indexC)
            undecidedConstituencies = np.delete(undecidedConstituencies, indexC)

            seenWins[winPartyID] += 1

            for p in range(P):

                Cl[p] = seenWins[p]
                Cu[p] = seenWins[p]

                for ci in undecidedConstituencies:
                    if p in listPartyIDs[ci]:
                        pIndex = listPartyIDs[ci].index(p)
                        if Nu[ci][pIndex] > max(Nl[ci]):
                            Cu[p] += 1

            winner = np.argmax(Cl)

            term = Cl[winner] - max(Cu[np.arange(len(Cu)) != winner])


            if N % 5 == 0:

##                print("*")
##                print(np.argsort(seenWins + countWinning)[-4:], sum(seenWins) + len(leadingParty))
##                print("**")
##                print(Cu[np.argsort(seenWins + countWinning)[-4:]], Cl[np.argsort(seenWins + countWinning)[-4:]])
##                print("***")
##                print(seenWins[np.argsort(seenWins + countWinning)[-4:]], countWinning[np.argsort(seenWins + countWinning)[-4:]])

                print(pa, pb)
                print(N, constituencies[c], Parties[winPartyID], sum(map(sum, seenVotes)), sum(seenVotes[c]))
                print(Cl[winner], max(Cu[np.arange(len(Cu)) != winner]))
                      
            if term > 0:

                totalVotesCounted = sum(map(sum, seenVotes))
                print("Decided constituencies = ", sum(seenWins))
                print(Parties[winner], ", Seats won = ", seenWins[winner], ", Total votes counted = ", totalVotesCounted)
                
                return sum(seenWins), winner, totalVotesCounted, seenVotes

if __name__ == "__main__":


    alpha = 10**-1
    batch = 500
    init_batch = batch
    data = "India2014"
    
    stoppingC, winner, stoppingVotes, seenVotes = runBanditElectionLUCB(data, alpha, batch, init_batch)

    print(stoppingC, winner, stoppingVotes)
