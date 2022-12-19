'''
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
'''
problem_name = ['Flowshop','Non-Flowshop','Hybridflowshop','Distributedflowshop','Nowaitflowshop','Setupflowshop','Tardinessflowshop','TCTflowshop','Jobshop','Flexiblejobshop','Openshop','Parallelmachine']

# Flowshop: 360
# Hybridflowshop: 1440
# Non-flowshop: 360
# Distributedflowshop: 600
# Nowaitflowshop: 360
# Setupflowshop: 480
# Tardinessflowshop: 540
# TCTflowshop: 360
# Openshop: 192
# Jobshop: 80 - 162
# Flexiblejobshop: 193 - 96
# Parallelmachine 1400

modelType = ['CPLEX']  #'CP','CPLEX','Gurobi','ORTools_MIP','ORTools_CP'

problem = 'Openshop'
instance = 192
allresults = []
for m in modelType:
    print(m)
    for w in range(1,1+instance):
        try:
            if m in ['ORTools_CP']:
                m1 = 'CP'
            else:
                m1 = 'MIP'
            with open('{}/{}_{}_2_HOURS/result_{}_{}_{}_{}_{}.txt'.format(problem,problem,m,m1,problem,7200,4,w),'r') as data:
                x = data.readline().strip()
                y = 0
                while x == '' and y < 10:
                    x = data.readline().strip()#.split()
                    y += 1
                #print(x)
                allresults.append(x) #
                if y == 10:
                    print(problem,t,m1,w, 'empty')
        except:
            allresults.append(' ')
            print('missing',problem,m1,m,w)

with open('{}_(May2022).txt'.format(problem),'w') as data1:
    for row in allresults:
        data1.write('\n')
        data1.write(row)

