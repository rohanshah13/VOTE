import numpy as np
import pandas as pd
import pickle
from util import *


## which elections
data = "Delhi2015"

## number of runs 
T = 10

## mistake probability
alpha = 10**-10

## batch size
batch = 500

algorithm = "TwoLevelOpinionSurvey"


a = 1
b = 1


constituencies = getAllPlaces(f"data/{data}/")

C = len(constituencies)

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

    

N0 = [sum(inner) for inner in listVotes]
Nl = [[0] * len(inner) for inner in listVotes]
Nu = [[sum(inner)] * len(inner) for inner in listVotes]



leadingParty = np.zeros(C)
terminated = np.zeros(C)


t = 1
with open(f"results/{data}/{algorithm}_seenVotes_{alpha}_{batch}_{t}.pkl", "rb") as input_file:
    seenVotes = pickle.load(input_file)

totalVotesCounted = 0

for c in range(C):

    K = len(listParties[c])

    for k in range(K):
            
        tempL, tempU = binBounds(alpha/(K*C), N0[c], a, b, sum(seenVotes[c]), seenVotes[c][k])

        Nl[c][k] = max(Nl[c][k], tempL)
        Nu[c][k] = min(Nu[c][k], tempU)

    constiWinner = np.argmax(seenVotes[c])

    constiTerm = Nl[c][constiWinner] - max([x for i,x in enumerate(Nu[c]) if i!=constiWinner])

    leadingParty[c] = Parties.index(listParties[c][constiWinner])

    if constiTerm > 0:
        terminated[c] = 1


    print(c, constituencies[c], Parties[int(leadingParty[c])], terminated[c], sum(seenVotes[c]), seenVotes[c][constiWinner])

    totalVotesCounted += sum(seenVotes[c])

print(totalVotesCounted)
