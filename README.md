# bandit-elections

To run a full experiment, you only need to look at runElectionBatch.py

The script takes two command line arguments

--dataset India2014/India2004/Delhi2015 etc (give the name of a folder in data/)
--algorithm Uniform/DCB/LUCB/TwoLevelOpinionSurvey

Uniform - Baseline which samples constituencies in a round robin manner
TwoLevelOpinionSurvey - Another baseline which chooses a constituency at random and resolves it completely before moving on to another constituency
DCB - The main algorithm that we are proposing
LUCB - An older algorithm which we are not planning to use

Results are stored in the 'results/' directory.


# integer-programming

This computes the minimum number of samples required to decide the winner of the election given the PPR stopping rule. 

Run using the command - python3 real_ip.py --dataset [India2004/India2014/..]