# bandit-elections

To run a full experiment, you only need to look at runElectionBatch.py

There are 4 variables at the start of the main function of this file: data -> which elections you want to run (India2004, India2014, Bihar2015 etc.); T -> number of runs, alpha -> mistake probability, batch -> batch size.

After setting the values of these parameters, simply execute runElectionBatch.py/

This will save all the counted votes for each run at the end of the run.