from docplex.cp.model import *


###### main ########
def CPmodel_generation(instance,mdl,problemType):

    if problemType == 'Flowshop':
        mdl = flowshopmodel(instance,mdl)
    if problemType == 'Non-Flowshop':
        mdl = Nonflowshopmodel(instance,mdl)
    if problemType == 'Hybridflowshop':
        mdl = Hybridflowshopmodel(instance,mdl)
    if problemType == 'Distributedflowshop':
        mdl = Distributedflowshopmodel(instance,mdl)
    if problemType == 'Nowaitflowshop':
        mdl = Nowaitflowshopmodel(instance,mdl)
    if problemType == 'Setupflowshop':
        mdl = Setupflowshopmodel(instance,mdl)
    if problemType == 'Tardinessflowshop':
        mdl = Tardinessflowshopmodel(instance,mdl)
    if problemType == 'TCTflowshop':
        mdl = TCTflowshopmodel(instance,mdl)        
    if problemType == 'Jobshop':
        mdl = jobshopmodel(instance,mdl)
    if problemType == 'Flexiblejobshop':
        mdl = Flexiblejobshopmodel(instance,mdl)
    if problemType == 'Openshop':
        mdl = openshopmodel(instance,mdl)
    if problemType == 'Parallelmachine':
        mdl = prallelmachinemodel(instance,mdl)        
    return mdl


def TCTflowshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
         
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(tasks[j][i-1],tasks[j][i]))     #no overlap jobs

    Sequence_variable = [[]] * instance.g
    for i in range(instance.g):
        Sequence_variable[i] = mdl.sequence_var([tasks[j][i] for j in range(instance.n)])

    for i in range(instance.g):
        mdl.add(mdl.no_overlap( Sequence_variable[i] ))     #no overlap machines

    for i in range(instance.g-1):
        mdl.add(mdl.same_sequence(Sequence_variable[i],Sequence_variable[i+1]))
  
    mdl.add(mdl.minimize( mdl.sum([mdl.end_of(tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is total tardiness
    
    return mdl


def Distributedflowshopmodel(instance,mdl):
    
    tasks = [[] for j in range(instance.n)]
    for j in range(instance.n):
        tasks[j] = [[] for i in range(instance.g)]
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = [mdl.interval_var(name="A_{}_{}_{}".format(j,i,k), optional=True, size=instance.p[j][i]) for k in range(instance.f)]  #interval variable

    _tasks = [[] for j in range(instance.n)]
    for j in range(instance.n):
        _tasks[j] = [mdl.interval_var(name="T_{}_{}".format(j,i)) for i in range(instance.g)]
    for j in range(instance.n):
        for i in range(instance.g):
            #if i == 0:
            mdl.add(mdl.alternative(_tasks[j][i], [tasks[j][i][k] for k in range(instance.f)]))

    for j in range(instance.n):
        for i in range(1,instance.g):
            for k in range(instance.f):
                mdl.add( mdl.presence_of(tasks[j][i][k]) >= mdl.presence_of(tasks[j][0][k]) )
      
    Sequence_variable = [[]] * instance.g
    for i in range(instance.g):
        Sequence_variable[i] = [[]] * instance.f
        for k in range(instance.f):
            Sequence_variable[i][k] = mdl.sequence_var([tasks[j][i][k] for j in range(instance.n)])

    for i in range(instance.g):
        for k in range(instance.f):
            mdl.add(mdl.no_overlap( Sequence_variable[i][k] ))     #no overlap machines

    for i in range(instance.g-1):
        for k in range(instance.f):
            mdl.add(mdl.same_sequence(Sequence_variable[i][k],Sequence_variable[i+1][k]))

    #for i in range(instance.g):
    #    for k in range(instance.f):
    #        mdl.add(mdl.no_overlap( [tasks[j][i][k] for j in range(instance.n)] ))     #no overlap machines
    
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(_tasks[j][i-1],_tasks[j][i]))     #no overlap jobs

    #for j in range(instance.n):
    #    for i in range(1,instance.g):
    #        for k in range(instance.f):
    #            mdl.add(mdl.end_before_start(tasks[j][i-1][k],tasks[j][i][k]))     #no overlap jobs
            
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(_tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl


def Setupflowshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g    
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
         
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(tasks[j][i-1],tasks[j][i]))     #no overlap jobs

    Sequence_variable = [[]] * instance.g
    for i in range(instance.g):
        Sequence_variable[i] = mdl.sequence_var([tasks[j][i] for j in range(instance.n)])

    for i in range(instance.g-1):
        mdl.add(mdl.same_sequence(Sequence_variable[i],Sequence_variable[i+1]))
  
    for i in range(instance.g):
        mdl.add(mdl.no_overlap(Sequence_variable[i],instance.s[i]))     #no overlap

    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl
        


def Flexiblejobshopmodel(instance,mdl):

    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.o[j]
        
    for j in range(instance.n):
        for k in range(instance.o[j]):
            tasks[j][k] = [mdl.interval_var(name="A_{}_{}_{}".format(j,k,i), optional=True, size=instance.p[j][k][i]) for i in range(instance.g)]  #interval variable

    _tasks = [[]] * instance.n
    for j in range(instance.n):
        _tasks[j] = [mdl.interval_var(name="T_{}_{}".format(j,k)) for k in range(instance.o[j])]
    for j in range(instance.n):
        for k in range(instance.o[j]):
            mdl.add(mdl.alternative(_tasks[j][k], [tasks[j][k][i] for i in range(instance.g) if instance.p[j][k][i]>0]))
   
    for i in range(instance.g):
        go = 0
        for j in range(instance.n):
            for k in range(instance.o[j]):
                if instance.p[j][k][i]>0:
                    go = 1
        if go == 1:
            mdl.add(mdl.no_overlap( [tasks[j][k][i] for j in range(instance.n) for k in range(instance.o[j]) if instance.p[j][k][i]>0]))     #no overlap machines
       
    for j in range(instance.n):
        for k in range(1,instance.o[j]):
            mdl.add(mdl.end_before_start(_tasks[j][k-1],_tasks[j][k]))     #no overlap jobs
  
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(_tasks[j][instance.o[j]-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl


def Tardinessflowshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
   
    #for i in range(instance.g):
    #    mdl.add(mdl.no_overlap( [tasks[j][i] for j in range(instance.n)]))     #no overlap machines
       
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(tasks[j][i-1],tasks[j][i]))     #no overlap jobs

    Sequence_variable = [[]] * instance.g
    for i in range(instance.g):
        Sequence_variable[i] = mdl.sequence_var([tasks[j][i] for j in range(instance.n)])

    for i in range(instance.g):
        mdl.add(mdl.no_overlap( Sequence_variable[i] ))     #no overlap machines

    for i in range(instance.g-1):
        mdl.add(mdl.same_sequence(Sequence_variable[i],Sequence_variable[i+1]))
  
    mdl.add(mdl.minimize( mdl.sum([ mdl.max([mdl.end_of(tasks[j][instance.g-1])-instance.d[j],0]) for j in range(instance.n) ]) ))   #this is total tardiness
    
    return mdl


def Nowaitflowshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
   
    for i in range(instance.g):
        mdl.add(mdl.no_overlap( [tasks[j][i] for j in range(instance.n)]))     #no overlap machines
       
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_at_start(tasks[j][i-1],tasks[j][i]))     #no overlap jobs

    Sequence_variable = [[]] * instance.g
    for i in range(instance.g):
        Sequence_variable[i] = mdl.sequence_var([tasks[j][i] for j in range(instance.n)])

    for i in range(instance.g-1):
        mdl.add(mdl.same_sequence(Sequence_variable[i],Sequence_variable[i+1]))
  
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl


def Hybridflowshopmodel(instance,mdl):
  
    '''
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = [mdl.interval_var(name="A_{}_{}_{}".format(j,i,k), optional=True, size=instance.p[j][i]) for k in range(instance.m[i])]  #interval variable

    _tasks = [[]] * instance.n
    for j in range(instance.n):
        _tasks[j] = [mdl.interval_var(name="T_{}_{}".format(j,i)) for i in range(instance.g)]
    for j in range(instance.n):
        for i in range(instance.g):
            mdl.add(mdl.alternative(_tasks[j][i], [tasks[j][i][k] for k in range(instance.m[i])]))
  
    for i in range(instance.g):
        for k in range(instance.m[i]):
            mdl.add(mdl.no_overlap( [tasks[j][i][k] for j in range(instance.n)]))     #no overlap machines
       
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(_tasks[j][i-1],_tasks[j][i]))     #no overlap jobs
  
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(_tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is makespan

    return mdl
    '''

    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
   
    for i in range(instance.g):
        mdl.add(mdl.sum([mdl.pulse(tasks[j][i],1) for j in range(instance.n)]) <= instance.m[i] )     #no overlap machines
       
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(tasks[j][i-1],tasks[j][i]))     #no overlap jobs
 
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl

def flowshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
         
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(tasks[j][i-1],tasks[j][i]))     #no overlap jobs

    Sequence_variable = [[]] * instance.g
    for i in range(instance.g):
        Sequence_variable[i] = mdl.sequence_var([tasks[j][i] for j in range(instance.n)])

    for i in range(instance.g):
        mdl.add(mdl.no_overlap( Sequence_variable[i] ))     #no overlap machines

    for i in range(instance.g-1):
        mdl.add(mdl.same_sequence(Sequence_variable[i],Sequence_variable[i+1]))
  
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl

def Nonflowshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
   
    for i in range(instance.g):
        mdl.add(mdl.no_overlap( [tasks[j][i] for j in range(instance.n)]))     #no overlap machines
       
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(tasks[j][i-1],tasks[j][i]))     #no overlap jobs
 
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(tasks[j][instance.g-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl


def jobshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][instance.r[j].index(i+1)])  #interval variable
   
    for i in range(instance.g):
        mdl.add(mdl.no_overlap( [tasks[j][i] for j in range(instance.n)]))     #no overlap machines
       
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.add(mdl.end_before_start(tasks[j][instance.r[j][i-1]-1],tasks[j][instance.r[j][i]-1]))     #no overlap jobs
  
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(tasks[j][instance.r[j][instance.g-1]-1]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl


def openshopmodel(instance,mdl):
    
    tasks = [[]] * instance.n
    for j in range(instance.n):
        tasks[j] = [[]] * instance.g
        
    for j in range(instance.n):
        for i in range(instance.g):
            tasks[j][i] = mdl.interval_var(name="T_{}_{}".format(j,i), size=instance.p[j][i])  #interval variable
   
    for i in range(instance.g):
        mdl.add(mdl.no_overlap( [tasks[j][i] for j in range(instance.n)]))     #no overlap machines
       
    for j in range(instance.n):
        mdl.add(mdl.no_overlap( [tasks[j][i] for i in range(instance.g)]))     #no overlap jobs

    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(tasks[j][i]) for j in range(instance.n) for i in range(instance.g)]) ))   #this is makespan
    
    return mdl


def prallelmachinemodel(instance,mdl):
  
    '''
    tasks = [[]] * instance.n       
    for j in range(instance.n):
        tasks[j] = [mdl.interval_var(name="A_{}_{}".format(j,i), optional=True, size=instance.p[j][i]) for i in range(instance.g)]  #interval variable

    _tasks = [[]] * instance.n
    for j in range(instance.n):
        _tasks[j] = mdl.interval_var(name="T_{}".format(j))
    for j in range(instance.n):
            mdl.add(mdl.alternative(_tasks[j], [tasks[j][i] for i in range(instance.g)]))
  
    for i in range(instance.g):
        mdl.add(mdl.no_overlap( [tasks[j][i] for j in range(instance.n)]))     #no overlap machines
  
    mdl.add(mdl.minimize( mdl.max([ mdl.end_of(_tasks[j]) for j in range(instance.n) ]) ))   #this is makespan
    
    return mdl
    '''

    machine  = [ mdl.integer_var(min=0, max=instance.g-1)    for j in range(instance.n) ]
    duration = [ mdl.element(instance.p[j],machine[j])  for j in range(instance.n) ] # duration[i] = matrix[i][machine[i]]
    makespan = max([ sum([ instance.p[j][i]*(machine[j]==i) for j in range(instance.n) ]) for i in range(instance.g) ])
    mdl.add( sum([ duration[j] for j in range(instance.n) ]) <= instance.g*makespan ) # Mostly for strengthening lower bound
    mdl.add( minimize(makespan) )
    
    return mdl
