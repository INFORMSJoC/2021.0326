import datetime as dt
import sys
import os

# problem_name = ['Flowshop','Non-Flowshop','Hybridflowshop','Distributedflowshop','Nowaitflowshop','Setupflowshop','Tardinessflowshop','TCTflowshop','Jobshop','Flexiblejobshop','Openshop','Parallelmachine']
# modelType = ['CP','MIP']
# Solver = ['CPLEX','Groubi','Google','Xpress']

import models

try:
   problem_name = sys.argv[1]
   modelType = sys.argv[2]
   computational_time = sys.argv[3]
   First = sys.argv[4]
   Last = sys.argv[5]

except:
   problem_name = 'Parallelmachine'
   modelType = 'CP'
   computational_time = '10'
   First = '151'
   Last = '151'

try:
   Solver = sys.argv[6]
except:
   Solver = 'Google'
   
try:
   NThreads = int(sys.argv[7])
except:
   NThreads = 4

try:
   address = sys.argv[8]
except:
   address = '..\\Instances\\{}'.format(problem_name) #os.path.dirname(__file__)
   
try:
   output = sys.argv[9]
except:
   output = '..\\Results' #os.path.dirname(__file__)


for benchmark in range(int(First), int(Last)+1):
   if modelType == 'CP':
      if Solver not in ['CPLEX','Google']:
         continue
      if Solver == 'Google' and modelType == 'CP' and problem_name not in ['Non-Flowshop','Hybridflowshop','Nowaitflowshop','Jobshop','Flexiblejobshop','Openshop','Parallelmachine']:
         continue
   try:
      n,g,Time, LB, UB, GAP = models.main(int(computational_time),benchmark,problem_name,modelType,Solver,NThreads,address,output)
      result = open('{}\\result_{}_{}_{}_{}_{}.txt'.format(output,modelType,problem_name,computational_time,NThreads,benchmark),'a')
      result.write('\n{}\t {}\t {}\t {}\t {}\t {}\t {}\t {}\t {}\t {}'.format(problem_name,Solver,modelType,benchmark, n, g, LB, UB, GAP, Time))
      result.close()
   except:
      result = open('{}\\result_{}_{}_{}_{}_{}.txt'.format(output,modelType,problem_name,computational_time,NThreads,benchmark),'a')
      result.write('\n{}\t {}\t {}\t {}\t {} \t {}'.format(problem_name,Solver,modelType,benchmark,sys.exc_info()[0], sys.exc_info()[1]))
      result.close()
      print("Error:", sys.exc_info()[0], sys.exc_info()[1])
   
print("\n\nDone")
