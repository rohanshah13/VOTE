import numpy as np
from util import *
import argparse

N = 10**4
ALPHA = 10**-2
a = 1
b = 1
MF = 0.55
M_MEAN = 0.80
W_MEAN = 0.20


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_seeds', default=1, type=int)
    parser.add_argument('--algo', default='usual')

    args = parser.parse_args()
    num_seeds = args.num_seeds
    algo = args.algo
    
    sample_data = []
    for seed in range(num_seeds):
        print('--------------------------------------')
        print('Starting seed {}'.format(seed))
        print('--------------------------------------')
        np.random.seed(seed)
        unseen_votes = np.zeros((2,2))
    
        male_votes = int(MF*N)
        female_votes = N - male_votes
        votes = [male_votes, female_votes]
        unseen_votes[0,0] = male_votes_A = int(M_MEAN*male_votes)
        unseen_votes[0,1] = male_votes_B = male_votes - male_votes_A
        unseen_votes[1,0] = female_votes_A = int(W_MEAN*female_votes)
        unseen_votes[1,1] = female_votes_B = female_votes - female_votes_A
    
        seen_votes = np.zeros((2,2))
    
        unseen_votes_joint = np.sum(unseen_votes.copy(),axis=0)
        seen_votes_joint = np.zeros(2)

        assert(unseen_votes_joint[0] == unseen_votes[0,0] + unseen_votes[1,0])
        assert(unseen_votes_joint[1] == unseen_votes[0,1] + unseen_votes[1,1])


        lcb = np.zeros((2,2))
        ucb = np.ones((2,2))
        ucb[0,:] *= male_votes
        ucb[1,:] *= female_votes
        combined_lcb = np.sum(lcb.copy(), axis=0)
        combined_ucb = np.sum(ucb.copy(), axis=0)

        lcb_joint = np.zeros(2)
        ucb_joint = N*np.ones(2)
    
        term = False
    
        total_samples = 0
    
        if not algo == 'usual':
            print('Split Sampling')
            while not term:
                combined_votes_seen = np.sum(seen_votes.copy(), axis=0)
                
                winner = np.argmax(combined_votes_seen)
                loser = 1 - winner
                
                if ucb[0,winner] - lcb[0,winner] > ucb[1,winner] - lcb[1,winner]:
                    norm = unseen_votes[0,:]/np.sum(unseen_votes[0,:])

                    vote = np.random.multinomial(1,norm)

                    unseen_votes[0,:] -= vote
                    seen_votes[0,:] += vote

                else:
                    norm = unseen_votes[1,:]/np.sum(unseen_votes[1,:])

                    vote = np.random.multinomial(1,norm)

                    unseen_votes[1,:] -= vote
                    seen_votes[1,:] += vote

                for i in range(2):
                    for j in range(2):
                        lcb[i,j], ucb[i,j] = binBounds(ALPHA/4, votes[i], a, b, np.sum(seen_votes[i]), seen_votes[i,j])


                combined_lcb = np.sum(lcb.copy(), axis=0)
                assert(combined_lcb[0] == lcb[0,0] + lcb[1,0])
                assert(combined_lcb[1] == lcb[0,1] + lcb[1,1])
                combined_ucb = np.sum(ucb.copy(), axis=0)
                assert(combined_ucb[0] == ucb[0,0] + ucb[1,0])
                assert(combined_ucb[1] == ucb[0,1] + ucb[1,1])

                total_samples += 1

                if total_samples % 100 == 0:
                    print(total_samples)
                    print('LCB')
                    print(combined_lcb)
                    print('UCB')
                    print(combined_ucb)
                    # print('Uncombined LCB')
                    # print(lcb)
                    # print('Uncombined UCB')
                    # print(ucb)
                    # print('Seen Votes')
                    # print(seen_votes)
                if combined_lcb[0] > combined_ucb[1]:
                    print('A wins!!')
                    term = True
                elif combined_lcb[1] > combined_ucb[0]:
                    print('B wins!!')
                    term = True
        else:
            print('usual sampling')
            while not term and not np.sum(unseen_votes_joint) == 0:
                norm = unseen_votes_joint/np.sum(unseen_votes_joint)
                vote = np.random.multinomial(1, norm)

                unseen_votes_joint -= vote
                seen_votes_joint += vote

                total_samples += 1

                for i in range(2):
                    lcb_joint[i], ucb_joint[i] = binBounds(ALPHA/2, N, a, b, np.sum(seen_votes_joint), seen_votes_joint[i])

                if total_samples % 100 == 0:
                    print(seen_votes_joint)    
                    print('LCB:')
                    print(lcb_joint)
                    print('UCB:')
                    print(ucb_joint)

                if lcb_joint[0] > ucb_joint[1]:
                    print('A wins!!')
                    term = True
                elif lcb_joint[1] > ucb_joint[0]:
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