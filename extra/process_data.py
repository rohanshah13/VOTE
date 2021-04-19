import numpy as np
import json

TMP1 = 'tmp1.txt'
TMP2 = 'tmp2.txt'
INFILE1 = 'optimal/India2004/result.txt'
INFILE2 = 'trace/DCB_India2004_1_200_0.01'

def main():
    with open(INFILE1,'r') as f, open(TMP1, 'w') as tmp:
        next(f)
        next(f)
        constituencies = []
        
        for line in f:
            try:
                line = json.loads(line)
            except:
                print(INFILE1)
                print(line)
                exit()
            if line['Position'] == '1':
                constituency = line['Constituency']
                constituencies.append(constituency)
        constituencies.sort()
        for c in constituencies:
            tmp.write(c + '\n')

    with open(INFILE2, 'r') as f, open(TMP2,'w') as tmp:
        consitiuencies = []
        for line in f:
            if line.strip() == 'Election done':
                continue
            try:
                line = json.loads(line)
            except:
                print(INFILE2)
                print(line)
                exit()
            constituency = line['constituency']
            consitiuencies.append(constituency)
        consitiuencies.sort()   
        for c in consitiuencies:
            tmp.write(c + '\n')


if __name__ == '__main__':
    main()