<!-- # Bandit Elections

To run a full experiment, you only need run the command `python3 runElectionBatch.py --dataset [dataset] --algorithm [algorithm]`

The script takes two command line arguments

--dataset India2014/India2004/Delhi2015 etc (give the name of a folder in data/)

--algorithm Uniform/DCB/LUCB/TwoLevelOpinionSurvey

Uniform - Baseline which samples constituencies in a round robin manner

TwoLevelOpinionSurvey - Another baseline which chooses a constituency at random and resolves it completely before moving on to another constituency

DCB - The main algorithm that we are proposing

LUCB - An older algorithm which we are not planning to use

Results are stored in the 'results/' directory.

# Integer Programming

This computes the minimum number of samples required to decide the winner of the election given the PPR stopping rule. 

Run using the command - `python3 real_ip.py --dataset [India2004/India2014/..]`

Results are stored in the 'optimal/' directory -->

# PAC Mode estimation using PPR Martingale Confidence Sequences (Election Experiments)
Contains the implementation of various DCB and RR algorithm variants for estimating the winner of elections. In particular, we provide the implementation of DCB and RR variants of PPR-1VR, PPR-1V1, KLSN-1VR, KLSN-1V1, A1-1VR and A1-1V1.

## Prerequisites
Requires Python 3 for running the code. Install all the dependencies by running the following command:
```
$ pip install -r requirements.txt
```

## Datasets

Data from two Indian Elections was used to run experiments:
1. Indian National Elections 2014 (source - https://www.indiavotes.com/pc/info?eid=16&state=0) - data/India2014
2. Bihar State Elections 2015 (source - https://www.indiavotes.com/ac/info?stateac=58&eid=245) - data/Bihar2015

## Reproducing the results
The main command for running the code
```
$ python runElectionBatch.py --dataset <dataset_name> --algorithm <algorithm_name>
```
The results containing the sample complexity, winning party, number of seats resolved are logged after executing the above command. The experiments are performed for 10 random seeds and the mistake probability is set to 0.01. These statistics for each of the runs are also saved in `.npy` format at `results/<dataset_name>/<algorithm_name>`. Following flags for algorithm can be used

| `<algorithm_name>`| 
| :---        | 
| RRPPR1VR      | 
| RRPPR1V1   |
| RRA11VR   |
| RRA11V1   |
| RRKLSN1VR   |
| RRKLSN1V1   |
| DCBPPR1VR      | 
| DCBPPR1V1   |
| DCBA11VR   |
| DCBA11V1   |
| DCBKLSN1VR   |
| DCBKLSN1V1   |
