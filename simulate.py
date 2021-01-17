import numpy as np
from scipy.stats import betabinom
from util import *

def runExperiment(data, alpha, batch = 1, termWhenSep = True, verbose = False, a = 1, b = 1):
    
    N0 = np.sum(data)
    K = len(data)

    N = np.zeros(N0+1)

    Nl = np.zeros((K, N0 + 1))
    Nu = np.ones((K, N0 + 1)) * N0

    N[0] = N0

    unseenVotes = np.copy(data)
    seenVotes = np.zeros(K)

    i = 0
    separated = False
    separated_i = N0

    while N[i] > 0:

        vote = np.random.multinomial(1, unseenVotes/np.sum(unseenVotes))

        seenVotes += vote
        unseenVotes -= vote

        i = i + 1
        N[i] = N[i-1] - 1

        
        for k in range(K):
            if i % batch == 0:
                Nl[k, i], Nu[k, i] = binBounds(alpha/K, N0, a, b, i, seenVotes[k])

            ## intersection 
            Nl[k, i] = max(Nl[k, i-1], Nl[k, i])
            Nu[k, i] = min(Nu[k, i-1], Nu[k, i])
        
        if i % batch == 0:
            winner = np.argmax(Nl[:, i])
            term = Nl[winner, i] - max(Nu[:, i][np.arange(len(Nu[:, i])) != winner])

            if verbose and i % (N0//10) == 0:
                print(i, term, winner, seenVotes)

            if term > 0 and not separated:
                separated = True
                separated_i = i
                
                if verbose:
                    print("Seperated at ", separated_i)

                if termWhenSep:
                    return separated_i, winner

        # Don't run for too long
        if i >= 10000:
            print("Terimated at ", i)
            return i, winner

    return separated_i, int(winner)

def runOracleSearch(data, alpha, batch = 1, a = 1, b = 1):

    N0 = np.sum(data)
    K = len(data)

    Nl = np.zeros(K)
    Nu = np.ones(K) * N0
    
    voteList = np.concatenate([np.ones(data[i]) * i for i in range(len(data))])

    votePerm = np.random.choice(voteList, len(voteList), replace = False)

    ## np.array([np.sum(y == i) for i in range(int(max(y) + 1))])

    def check(c):

        seenVotes = np.array([np.sum(votePerm[:c] == i) for i in range(int(max(votePerm) + 1))])
        
        for k in range(K):
            Nl[k], Nu[k] = binBounds(alpha/K, N0, a, b, np.sum(seenVotes), seenVotes[k])

        winner = np.argmax(Nl)
        term = Nl[winner] - max(Nu[np.arange(len(Nu)) != winner])            
                
        return term > 0

    def search(l, h):
        
        c = (l + h)//2
        
        if check(c):
            if check(c - 1):
                return search(l, c)
            else:
                return c
        else:
            if not check(c + 1):
                return search(c, h)
            else:
                return c + 1            

    stoppingTime = search(0, N0)

    stoppingTime = min(stoppingTime + batch - stoppingTime % batch, N0)

    seenVotes = [np.sum(votePerm[:stoppingTime] == i) for i in range(int(max(votePerm) + 1))]

    winner = np.argmax(seenVotes)
    
    return stoppingTime, int(winner), seenVotes
