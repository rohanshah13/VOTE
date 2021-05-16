import numpy as np
import argparse
from util import *

N = 10**5
ALPHA = 10**-2
MEAN = 0.6
P = 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_seeds', default=1, type=int)

    args = parser.parse_args()
    num_seeds = args.num_seeds

    uniform = [1, 1]
    true_a = [60, 40]
    true_b = [40, 60]
    a = [40,60]
    b = [60,40]
    
    sample_data = []
    for seed in range(num_seeds):
        print('--------------------------------------')
        print('Starting seed {}'.format(seed))
        print('--------------------------------------')
        np.random.seed(seed)
        
        votes_A = int(MEAN*N)
        votes_B = N - votes_A
        
        unseen_votes = np.asarray([votes_A, votes_B])
        seen_votes = np.zeros(2)
        
        lcb = np.zeros(2)
        ucb = np.ones(2)*N

        term = False
        total_samples = 0

        while not term:
            norm = unseen_votes/np.sum(unseen_votes)

            vote = np.random.multinomial(1,norm)

            unseen_votes -= vote
            seen_votes += vote

            for i in range(P):
                tempL, tempU = binBounds(ALPHA/2, N, a[i], b[i], np.sum(seen_votes), seen_votes[i])
                lcb[i], ucb[i] = max(tempL, lcb[i]), min(tempU, ucb[i])
                # lcb[i], ucb[i] = binBounds(ALPHA/2, N, a[i], b[i], np.sum(seen_votes), seen_votes[i])

            total_samples += 1

            if total_samples % 50 == 0:
                print('LCB:')
                print(lcb)
                print('UCB:')
                print(ucb)

            if lcb[0] > ucb[1]:
                print('A wins!!')
                term = True
            elif lcb[1] > ucb[0]:
                print('B wins!!')
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