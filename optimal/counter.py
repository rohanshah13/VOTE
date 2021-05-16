import json
import argparse

INFILE = '{}/result.txt'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='India2014')

    args = parser.parse_args()

    dataset = args.dataset
    infile = INFILE.format(dataset)

    counter = 0
    with open(infile,'r') as f:
        next(f)
        next(f)
        for line in f:
            line = json.loads(line)
            position = int(line["Position"])
            if position == 1:
                counter += 1

    print(counter)

if __name__ == '__main__':
    main()