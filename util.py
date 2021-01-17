import os
import json
import numpy as np
from math import factorial
from scipy.stats import betabinom


def normalize(p):

    return p/np.sum(p)

def sampleBetaBin(n, a, b):
    
    p = np.random.beta(a, b)
    r = np.random.binomial(n, p)

    return r

##def sampleDirMulti(n, alphas):
##    
##    p = np.random.dirichlet(alphas)
##    r = np.random.multinomial(n, p)
##
##    return r
##
##def pmfDirMulti(v, n, alphas):
##
##    if min(v) < 0:
##        return 0
##
##    x = factorial(n) * factorial(np.sum(alphas) - 1) / factorial(n + np.sum(alphas) - 1)
##
##    for i in range(len(alphas)):
##
##        #was unable to handle large calculations so I did this not sure if correct discuss with shivaram
##
##        try:
##            x = x * factorial(v[i] + alphas[i] - 1) / ( factorial(v[i]) * factorial(alphas[i] - 1) )
##
##        except:
##            temp = 1 / factorial(v[i])
##
##            for j in range(1, v[i] + 1):
##                temp = temp * (j + alphas[i] - 1)
##
##            x = x * temp
##    return x

def scoreCandidate(candidateStats):

    s = 0
    for k in range(len(candidateStats)):
        s += (k+1) * candidateStats[k]

    return s

def scoreCandidateLB(lb, ub, N0):

    x = np.copy(lb)
    
    for k in range(len(lb)):

        N = np.sum(x)
        if N == N0:
            break
        x[k] += min(ub[k]-x[k], N0 - N)

    return scoreCandidate(x)

def scoreCandidateUB(lb, ub, N0):

    x = np.copy(ub)

    for k in range(len(ub)):

        N = np.sum(x)
        if N == N0:
            break
        x[k] -= min(x[k]-lb[k], N-N0)
        
    return scoreCandidate(x)
        

def ppr(k, N0, a, b, t, kt):

    return betabinom.pmf(k, N0, a, b) / betabinom.pmf(k - kt, N0 - t, a + kt, b + t - kt)

##def pprDirMulti(v, N0, alphas, cData):
##
##    return pmfDirMulti(v, N0, alphas) / pmfDirMulti(v - cData, N0 - np.sum(cData), alphas + cData)
##
##
##def CI(alpha, N0, alphas, cData):
##
##    t = N0 - np.sum(cData)
##    
##    for i in range(t + 1):
##        for j in range(t + 1 - i):
##            for k in range(t + i + j - 1


## brute force search
##def bounds(alpha, N0, a, b, t, kb):
##
##    i = 0
##    while ppr(i, N0, a, b, t, kb) > 1/alpha:
##        i+=1
##
##    j = N0
##    while ppr(j, N0, a, b, t, kb) > 1/alpha:
##        j-=1
##
##    return i, j



# binary search
def binBounds(alpha, N0, a, b, t, kb):

    def f(c):

        return ppr(c, N0, a, b, t, kb) - 1/alpha
    
    def check(c):
        
        if f(c) < 0:
            return c
        else:
            return -1

    def binSearch(l, h, increasing):

        if increasing:
            
            if h - l == 1:
                return l
            
            c = (l+h)//2

            if f(c) < 0:
                l = c
            else:
                h = c

            return binSearch(l, h, True)

        else:
            if h - l == 1:
                return h

            c = (l+h)//2

            if f(c) < 0:
                h = c
            else:
                l = c

            return binSearch(l, h, False)

            

    #find a point inside the confidence interval    
    
    def pointInsideCI(l, h):

        p = 1
        while True:
            for i in np.arange(1, 2**p + 1, 2):
                k = check(l + (h-l) * i // 2**p)

                if k != -1:
                    return k
            p+=1

    k = pointInsideCI(0, N0)

    if f(0) < 0:
        i = 0
    else:
        i = binSearch(0, k, False) 

    if f(N0) < 0:
        j = N0
    else:
        j = binSearch(k, N0, True)
    
    return i, j


def trueWinner(data):

    scores = np.load(data)

    return np.argmax(np.sum(scores, axis = 0))

def getAllPlaces(directory = "data/"):
    
    allPlaces = [x.replace(".csv", "").strip() for x in os.listdir(directory) if x[-4:] == ".csv"]
    allPlaces = [x for x in allPlaces]
    #allPlaces = sorted(allPlaces)
    allPlaces.sort()
    return allPlaces

def getPartyList(file):

    with open(file, 'r') as f:
        return json.load(f)
    

    
