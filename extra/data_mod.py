import numpy as np
import pandas as pd
import os

BJP = 'Bharatiya Janta Party'
CONG = 'Indian National Congress'
DATA_DIR = 'data/RealData1/'

def main():
	count = 0
	count_bjp = 0
	count_cong = 0
	for filename in os.listdir(DATA_DIR):
		filepath = DATA_DIR + filename
		table = pd.read_csv(filepath)
		parties = table['Party'].to_list()
		if BJP in parties and CONG in parties and parties[0] in [BJP,CONG]:
			count += 1
			if parties[0] == BJP:
				count_bjp += 1
			else:
				count_cong += 1
			#table = table.loc[(table['Party'] == BJP) | (table['Party'] == CONG),:]
			#table.to_csv(filepath,index=False)
		else:
			pass
			#os.remove(filepath)
	print(count, count_bjp, count_cong)
		
if __name__ == '__main__':
	main()