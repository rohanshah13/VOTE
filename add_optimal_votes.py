import pandas as pd
import numpy as np
import json
import argparse
from util import *


DATA_DIR = 'sample_data/{}'
MY_FILE = 'optimal/{}/result.txt'
DATASETS = ['India2004', 'India2014', 'Delhi2015', 'Bihar2015', 'Easy-Easy', 'Easy-Hard', 'Hard-Easy', 'Hard-Hard']

def main():
    for dataset in DATASETS:
        data_dir = DATA_DIR.format(dataset)
        myfile = MY_FILE.format(dataset)

        constituencies = getAllPlaces(data_dir)
        C = len(constiuencies)

        print(constituencies)

        for c in constituencies:
            df = pd.read_csv('sample_data/{}/{}.csv'.format(dataset,c))

            min_sample = df['MinSample'].to_list()


    