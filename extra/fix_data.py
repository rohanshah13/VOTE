import numpy as np
import json

INFILE = 'trace/LUCB_TriData1_0_200_0.01'
OUTFILE = 'trace/LUCB_TriData1_0_200_0.01_mod'
DATA = 'data/TriData1/{}.csv'


def main():
    with open(INFILE,'r') as input_file, open(OUTFILE,'w') as output_file:
        for line in input_file:
            data = json.loads(line)
            constituency = data['constituency'] 
            votes = [0,0,0]
            with open(DATA.format(constituency), 'r') as f:
                next(f)
                for line in f:
                    line = line.split(',')
                    if line[4].strip() == 'A':
                        votes[0] = line[2]
                    elif line[4].strip() == 'B':
                        votes[1] = line[2]
                    elif line[4].strip() == 'C':
                        votes[2] = line[2]
            data['constituency_votes_A'] = votes[0]
            data['constituency_votes_B'] = votes[1]
            data['constituency_votes_C'] = votes[2]
            output_file.write(json.dumps(data) + '\n')

if __name__ == '__main__':
    main()