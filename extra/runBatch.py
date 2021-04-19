import numpy as np
from util import *
from simulate import *

def runBatch(data, T, alpha, batch):

    stoppingTimes = np.zeros(T)
    winners = np.zeros(T)

    for t in range(T):

        print("iteration ", t)
        stoppingTimes[t], winners[t] = runExperiment(data, alpha, True, True, batch)

        ## early termination
        if stoppingTimes[t] == 10000:
            return np.ones(T) * 10000, (np.ones(T) * winners[t]).astype(int)


    return stoppingTimes, winners.astype(int)

def main():

    #### biden trump
    ##data = np.array([650, 350])

    ## adilabad
    data = np.array([377374, 318814, 314238, 8007, 6837, 5523, 5241, 4548, 4388, 3019, 2705])

##    ## ajmer
##    data = np.array([815076, 398652, 13618, 13041, 4824, 4652, 2773])
    
    T = 10
    alpha = 10**-1
    batch = 100

    W = np.argmax(data)
    
    stoppingTimes, winners = runBatch(data, T, alpha, batch)

    print("For alpha = ", alpha, ", Stopping time = ", np.mean(stoppingTimes), " +- ", np.std(stoppingTimes)/np.sqrt(T))
    print("Accuracy = ", 100 * np.sum(winners == W) / T, "%")
    
if __name__ == "__main__":

    main()
