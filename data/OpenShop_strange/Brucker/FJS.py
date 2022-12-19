# http://nbviewer.jupyter.org/gist/manujeevanprakash/996d18985be612072ee0

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pylab as pl
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
from statsmodels.formula.api import ols
import statsmodels
from statsmodels.graphics.factorplots import interaction_plot
import statsmodels.stats.anova
import datetime as dt
from collections import Counter

sns.set(style="ticks")

jobs = [3,4,5,6,7,8]

q = 140
for n in jobs:
    print(n)
    with open('B{}.txt'.format(n),'r') as data:
        if n == 3 or n == 8:
            w = 8
        else:
            w = 9
        for k in range(w):
            print(k)
            z = data.readline().strip().split()
            z = data.readline().strip().split()
            p = []
            for j in range(n):
                p.append(data.readline().strip().split())

            q += 1
            with open('{}.txt'.format(q),'w') as data1:
                data1.write('{}\n{}'.format(n,n))
                for j in range(n):
                    data1.write('\n')
                    for i in range(n):
                        data1.write(p[j][i])
                        data1.write('\t')


                    
