import numpy as np
import pandas as pd
import argparse
import os
from util import *
import shutil

DATA_DIR = 'data/{}'
OUT_DIR = 'sample_data/{}'
a = 1
b = 1

#this gets the minimum number of samples required to resolve C for the given party with mistake probability alpha
def get_val(alpha, votes, p, C, upper_bound):
    winner_votes = votes[0]
    loser_votes = votes[p]
    total_votes = sum(votes)
    K = len(votes)
    loser_frac = votes[p]/total_votes
    winner_frac = votes[0]/total_votes

    #uses binary search to find the lowest number of samples to separate party p and winner
    l, h = 0, upper_bound
    while True:
        if h - l == 1:
            return h
        mid = (h + l)//2

        loser_sampled = int(loser_frac*mid)
        winner_sampled = int(winner_frac*mid)
        loserL, loserU = binBounds(alpha/(K*C), total_votes, a, b, mid, loser_sampled)
        winnerL, winnerU = binBounds(alpha/(K*C), total_votes, a, b, mid, winner_sampled)

        if loserU < winnerL:
            h = mid
        else:
            l = mid

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset',default='India2014')
    parser.add_argument('--alpha', default=10**-2, type=float)
    parser.add_argument('--batch_size', default=200, type=int)
    args = parser.parse_args()    

    dataset = DATA_DIR.format(args.dataset)
    output_directory = OUT_DIR.format(args.dataset)
    alpha = args.alpha
    batch_size = args.batch_size
    
    C = len(os.listdir(dataset))

    counter = 0

    if not os.path.exists('sample_data'):
        os.mkdir('sample_data')
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    #calculating the reqd values for each file
    for filename in os.listdir(dataset):
        counter += 1
        try:
            df = pd.read_csv(os.path.join(dataset,filename))
        except:
            print(filename)
            exit()
        votes = df["Votes"].tolist()
        votes = [int(str(vote).replace(',','')) for vote in votes]
        
        P = len(votes)
        #Here we store the reqd data
        min_sample = [None for i in range(P)]

        min_sample[0] = sum(votes)
        #min_sample[p] is the minimum number of votes required to separate p from the winner
        #round off to a multiple of 200 because our DCB algorithm uses that batch size
        for p in range(1,P):
            #min_sample[p-1] is the upper bound because we know the values are decreasing
            min_sample[p] = get_val(alpha, votes, p, C, min_sample[p-1])
            if min_sample[p] % 200 != 0:
                min_sample[p] = (min_sample[p]//batch_size + 1)*batch_size

        #number of samples required to show the second placed party is losing = number of samples required to decide winner
        min_sample[0] = min_sample[1]
        #write back to file in the same format
        df.insert(3,"MinSample",min_sample)
        df.to_csv(os.path.join(output_directory, filename), index=False)

        if counter % 10 == 0:
            print(counter)
    
    print('Done!')




if __name__ == '__main__':
    main()