import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

alpha = 10**-10
T = 10
batch = 100

data = np.load(f"results/stoppingTimes_{alpha}_{T}_{batch}.npy")


print(f"Data for {data.shape[0]} constituencies for {T} runs each with alpha = {alpha}")

avgStoppingTimes = np.clip(np.mean(data, axis = 1), 0, 10000)

avgStoppingTimes.sort()

print(avgStoppingTimes)

plt.hist(avgStoppingTimes, bins = 20)
plt.show()