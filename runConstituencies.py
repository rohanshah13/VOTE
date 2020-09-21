import numpy as np
import pandas as pd
from util import *
from runBatch import *


resume = True

def main():

    alpha = 10**-10
    T = 10
    batch = 100

    Parties = getPartyList("partyList.json")
    
    constituencies = getAllPlaces()

    C = len(constituencies)

    stoppingTimes = np.zeros((C, T))
    winnerIDs = np.zeros((C, T))

    start = 0

    if resume == True:
        try:
            oldST = np.load(f"results/stoppingTimes_{alpha}_{T}_{batch}.npy")
            oldWID = np.load(f"results/winnerIDs_{alpha}_{T}_{batch}.npy")

            start = oldST.shape[0]
            print(f"Resuming from constiuency {start}: {constituencies[start]}")

            stoppingTimes[:start, :] = oldST
            winnerIDs[:start, :] = oldWID
        
        except: 
            print("No file to resume from")
            exit()
    
    for c in range(start, C):

        print("Constituency ", c, ": ", constituencies[c])

        table = pd.read_csv("data/" + constituencies[c] + ".csv")

        data = table['Votes'].to_numpy()
        parties = table['Party'].to_list()

        # partiesID = np.zeros(len(parties))

        # for i in range(len(parties)):
        #     partiesID[i] = Parties.index(parties[i])


        stoppingTimes[c], winners = runBatch(data, T, alpha, batch)

        winnerIDs[c] = [Parties.index(parties[w]) for w in winners]

        np.save(f"results/stoppingTimes_{alpha}_{T}_{batch}.npy", stoppingTimes[:c+1])

        np.save(f"results/winnerIDs_{alpha}_{T}_{batch}.npy", winnerIDs[:c+1])

if __name__ == "__main__":

    main()
