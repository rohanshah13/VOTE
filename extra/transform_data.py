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

def get_val(alpha, votes, p, C, upper_bound):
    winner_votes = votes[0]
    loser_votes = votes[p]
    total_votes = sum(votes)
    K = len(votes)
    loser_frac = votes[p]/total_votes
    winner_frac = votes[0]/total_votes

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

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    for filename in os.listdir(dataset):
        counter += 1
        try:
            df = pd.read_csv(os.path.join(dataset,filename))
        except:
            print(filename)
            exit()
        votes = df["Votes"].tolist()
        votes = [int(str(vote).replace(',','')) for vote in votes]
        winner_votes = votes[0]
        P = len(votes)
        min_sample = [None for i in range(P)]

        min_sample[0] = sum(votes)
        for p in range(1,P):
            min_sample[p] = get_val(alpha, votes, p, C, min_sample[p-1])
            if min_sample[p] % 200 != 0:
                min_sample[p] = (min_sample[p]//batch_size + 1)*batch_size

        min_sample[0] = min_sample[1]
        df.insert(3,"MinSample",min_sample)
        df.to_csv(os.path.join(output_directory, filename), index=False)

        if counter % 10 == 0:
            print(counter)
    
    print('Done!')




if __name__ == '__main__':
    main()