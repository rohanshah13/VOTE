import numpy as np
import argparse
from util import *
import pandas as pd

DATA = 'data/Bihar2015/87_Jale_Bihar2015.csv'
ALPHA = 10**-2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_seeds', default=1, type=int)
    parser.add_argument('--batch_size', default=1, type=int)

    args = parser.parse_args()
    num_seeds = args.num_seeds
    batch_size = args.batch_size

    table = pd.read_csv(DATA)
        
    table['Votes'] = table['Votes'].str.replace(',','')

    votes = list(map(int, table['Votes'].to_list()))
    parties = table['Party'].to_list()

    N = sum(votes)
    P = len(votes)

    sample_data = []
    for seed in range(num_seeds):
        print('--------------------------------------')
        print('Starting seed {}'.format(seed))
        print('--------------------------------------')
        np.random.seed(seed)
    
        unseen_votes = np.asarray(votes.copy())
        seen_votes = np.zeros(P)
    
        lcb = np.zeros(P)
        ucb = np.ones(P)*N
    
        term = False
        total_samples = 0
    
        a = 1000*unseen_votes/N
        b = 1000 - a
    
        a[0], a[1] = a[1], a[0]
        b[0], b[1] = b[1], b[0]
        # a = np.ones(P)
        # b = np.ones(P)
    
        while not term:
            for _ in range(batch_size):
                norm = unseen_votes/np.sum(unseen_votes)

                vote = np.random.multinomial(1,norm)

                unseen_votes -= vote
                seen_votes += vote

            for i in range(P):
                tempL, tempU = binBounds(ALPHA/P, N, a[i], b[i], np.sum(seen_votes), seen_votes[i])
                lcb[i], ucb[i] = max(lcb[i],tempL), min(ucb[i],tempU)

            total_samples += batch_size

            if total_samples % 1000 == 0:
                print('LCB:')
                print(lcb)
                print('UCB:')
                print(ucb)

            winner = np.argmax(seen_votes)
            best_loser = np.argsort(ucb)[-2]

            if lcb[winner] > ucb[best_loser]:
                print('{} wins!!'.format(parties[winner]))
                term = True
        sample_data.append(total_samples)
        print(total_samples)
        print('------------------------------')
        print('Completed seed {}'.format(seed))
        print('------------------------------')
    print(sample_data)
    print(np.mean(sample_data))
    print(np.std(sample_data))

        
        


if __name__ == '__main__':
    main()