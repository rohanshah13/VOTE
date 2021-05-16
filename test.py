import numpy as np
from scipy.stats import beta, betabinom

def main():
    for i in range(1000):
        val = beta.logpdf(0.5, 1, 1) - beta.logpdf(0.5, 1 + 50, 1 + 100 - 50)

    # for i in range(10000):
        # val = betabinom.pmf(50, 100, 1, 1) / betabinom.pmf(50 - 30, 100 - 50, 1 + 30, 1 + 50 - 30)

if __name__  == '__main__':
    main()