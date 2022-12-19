import cplex

M = 100000    #Big M
V = 10000000  #upper bound for variables

###### main ########
def MIPmodel_generation(instance,mdl,problemType):

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
        mdl = parallelmachinemodel(instance,mdl)         
    return mdl

def TCTflowshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}".format(j,j1) for j in range(instance.n) for j1 in range(j+1,instance.n)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    for j in range(instance.n):
        for i in range(instance.g-1):
            objective += [0]
        objective += [1]
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,0)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0]) 

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i])
    
    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j1,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i]-M )
    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j1,i)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j1][i] )
    
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl

def Flexiblejobshopmodel(instance,mdl):
    # Variable Z
    names =  ["Z_{}_{}_{}".format(j,k,i) for j in range(instance.n) for k in range(instance.o[j]) for i in range(instance.g)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable X
    names +=  ["X_{}_{}_{}_{}".format(j,k,j1,k1) for j in range(instance.n) for j1 in range(j+1,instance.n) for k in range(instance.o[j]) for k1 in range(instance.o[j1])]
    objective += [0 for j in range(instance.n) for j1 in range(j+1,instance.n) for k in range(instance.o[j]) for k1 in range(instance.o[j1])]
    lower_bounds += [0 for j in range(instance.n) for j1 in range(j+1,instance.n) for k in range(instance.o[j]) for k1 in range(instance.o[j1])]
    upper_bounds += [1 for j in range(instance.n) for j1 in range(j+1,instance.n) for k in range(instance.o[j]) for k1 in range(instance.o[j1])]
    types += ['B' for j in range(instance.n) for j1 in range(j+1,instance.n) for k in range(instance.o[j]) for k1 in range(instance.o[j1])]
    # Variable C
    names += ["C_{}_{}".format(j,k) for j in range(instance.n) for k in range(instance.o[j])]
    objective += [0 for j in range(instance.n) for k in range(instance.o[j])]
    lower_bounds += [0 for j in range(instance.n) for k in range(instance.o[j])]
    upper_bounds += [V for j in range(instance.n) for k in range(instance.o[j])]
    types += ['C'  for j in range(instance.n) for k in range(instance.o[j])]

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(instance.n):
        for k in range(instance.o[j]):
            variables = ["Z_{}_{}_{}".format(j,k,i) for i in range(instance.g) if instance.p[j][k][i] > 0]
            coffiecient = [1 for i in range(instance.g) if instance.p[j][k][i] > 0]
            constraints.append([variables,coffiecient])
            senses.append('E')
            rhs.append(1)
    
    # constarint 2
    for j in range(instance.n):
        for k in range(instance.o[j]):
            variables = ["C_{}_{}".format(j,k)]
            coffiecient = [1]
            if k > 0:
                variables += ["C_{}_{}".format(j,k-1)]
                coffiecient += [-1]
            variables += ["Z_{}_{}_{}".format(j,k,i) for i in range(instance.g) if instance.p[j][k][i] > 0]
            coffiecient += [-instance.p[j][k][i] for i in range(instance.g) if instance.p[j][k][i] > 0]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(0)
    
    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for k in range(instance.o[j]):
                for k1 in range(instance.o[j1]):
                    for i in range(instance.g):
                        if instance.p[j][k][i] > 0 and instance.p[j1][k1][i]>0:
                            variables = ["C_{}_{}".format(j,k)]
                            variables += ["C_{}_{}".format(j1,k1)]
                            variables += ["X_{}_{}_{}_{}".format(j,k,j1,k1)]
                            variables += ["Z_{}_{}_{}".format(j,k,i)]
                            variables += ["Z_{}_{}_{}".format(j1,k1,i)]
                            coffiecient = [1, -1, -M, -M, -M]
                            constraints.append([variables,coffiecient])
                            senses.append('G')
                            rhs.append(instance.p[j][k][i]-3*M )
    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for k in range(instance.o[j]):
                for k1 in range(instance.o[j1]):
                    for i in range(instance.g):
                        if instance.p[j][k][i] > 0 and instance.p[j1][k1][i]>0:
                            variables = ["C_{}_{}".format(j1,k1)]
                            variables += ["C_{}_{}".format(j,k)]
                            variables += ["X_{}_{}_{}_{}".format(j,k,j1,k1)]
                            variables += ["Z_{}_{}_{}".format(j,k,i)]
                            variables += ["Z_{}_{}_{}".format(j1,k1,i)]
                            coffiecient = [1, -1, M, -M, -M]
                            constraints.append([variables,coffiecient])
                            senses.append('G')
                            rhs.append(instance.p[j1][k1][i]-2*M )
    
    # constarint 5
    for j in range(instance.n):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.o[j]-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)
        
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl


def Tardinessflowshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}".format(j,j1) for j in range(instance.n) for j1 in range(j+1,instance.n)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable T
    names += ["T_{}".format(j) for j in range(instance.n)]
    objective += [1] * instance.n
    lower_bounds += [0] * instance.n
    upper_bounds += [V] * instance.n
    types += ['C'] * instance.n

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,0)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0]) 

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j1,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i]-M )
    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j1,i)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j1][i] )
    
    # constarint 5
    for j in range(instance.n):
        variables = ["T_{}".format(j)]
        variables += ["C_{}_{}".format(j,instance.g-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(-1*instance.d[j])
        
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl


def Setupflowshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}".format(j,j1) for j in range(1,instance.n+1) for j1 in range(instance.n+1)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n+1) for i in range(instance.g)]
    objective += [0] * (instance.n +1)* instance.g
    lower_bounds += [0] * (instance.n +1) * instance.g
    upper_bounds += [V] * (instance.n +1) * instance.g
    types += ['C'] * (instance.n +1) * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(1,instance.n+1):
        variables = ["X_{}_{}".format(j,j1) for j1 in range(instance.n+1) if j1 != j]
        coffiecient = [1 for j1 in range(instance.n+1) if j1 != j]
        constraints.append([variables,coffiecient])
        senses.append('E')
        rhs.append(1)

    # constarint 2
    for j1 in range(1,instance.n+1):
        variables = ["X_{}_{}".format(j,j1) for j in range(1,instance.n+1) if j1 != j]
        coffiecient = [1 for j in range(1,instance.n+1) if j1 != j]
        constraints.append([variables,coffiecient])
        senses.append('L')
        rhs.append(1)

    # constarint 2-1
    variables = ["X_{}_{}".format(j,0) for j in range(1,instance.n+1)]
    coffiecient = [1 for j in range(1,instance.n+1)]
    constraints.append([variables,coffiecient])
    senses.append('E')
    rhs.append(1)

    # constarint 3
    for j in range(1,instance.n+1):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j-1][i])

    # constarint 4
    for j in range(1,instance.n+1):
        for j1 in range(instance.n+1):
            if j1 != j:
                for i in range(instance.g):
                    variables = ["C_{}_{}".format(j,i)]
                    variables += ["C_{}_{}".format(j1,i)]
                    variables += ["X_{}_{}".format(j,j1)]
                    coffiecient = [1, -1, -M]
                    constraints.append([variables,coffiecient])
                    senses.append('G')
                    if j1 == 0:
                        rhs.append(instance.p[j-1][i]-M )
                    else:
                        rhs.append(instance.p[j-1][i]+instance.s[i][j1-1][j-1]-M )
       
    # constarint 5
    for j in range(1,instance.n+1):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.g-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)
        
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl


def Nowaitflowshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}".format(j,j1) for j in range(instance.n) for j1 in range(j+1,instance.n)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,0)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0]) 

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('E')
            rhs.append(instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j1,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i]-M )
    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j1,i)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j1][i] )
    
    # constarint 5
    for j in range(instance.n):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.g-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)
        
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl

def Distributedflowshopmodel(instance,mdl):
    # Variable Y
    names =  ["Y_{}_{}".format(j,k) for j in range(instance.n) for k in range(instance.f)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    
    # Variable X
    names += ["X_{}_{}".format(j,j1) for j in range(instance.n) for j1 in range(j+1,instance.n)]
    objective += [0 for j in range(instance.n) for j1 in range(j+1,instance.n)]
    lower_bounds += [0 for j in range(instance.n) for j1 in range(j+1,instance.n)]
    upper_bounds += [1 for j in range(instance.n) for j1 in range(j+1,instance.n)]
    types += ['B' for j in range(instance.n) for j1 in range(j+1,instance.n)]

    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    constraints = []
    senses = []
    rhs = []
    
    # constarint 1
    for j in range(instance.n):
        variables = ["Y_{}_{}".format(j,k) for k in range(instance.f)]
        coffiecient = [1] * instance.f
        constraints.append([variables,coffiecient])
        senses.append('E')
        rhs.append(1)

    # constarint 2-1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,0)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0]) 

    # constarint 2-2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i])
    
    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.f):
                    variables = ["C_{}_{}".format(j,i)]
                    variables += ["C_{}_{}".format(j1,i)]
                    variables += ["X_{}_{}".format(j,j1)]
                    variables += ["Y_{}_{}".format(j,k)]
                    variables += ["Y_{}_{}".format(j1,k)]
                    coffiecient = [1, -1, -M, -M, -M]
                    constraints.append([variables,coffiecient])
                    senses.append('G')
                    rhs.append(instance.p[j][i]-3*M )
    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.f):
                    variables = ["C_{}_{}".format(j1,i)]
                    variables += ["C_{}_{}".format(j,i)]
                    variables += ["X_{}_{}".format(j,j1)]
                    variables += ["Y_{}_{}".format(j,k)]
                    variables += ["Y_{}_{}".format(j1,k)]
                    coffiecient = [1, -1, M, -M, -M]
                    constraints.append([variables,coffiecient])
                    senses.append('G')
                    rhs.append(instance.p[j1][i]-2*M )
    
    for j in range(instance.n):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.g-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)

    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl

def Hybridflowshopmodel(instance,mdl):
    # Variable Y
    names =  ["Y_{}_{}_{}".format(j,i,k) for j in range(instance.n) for i in range(instance.g) for k in range(instance.m[i])]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    
    # Variable X
    names += ["X_{}_{}_{}".format(j,j1,i) for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]
    objective += [0 for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]
    lower_bounds += [0 for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]
    upper_bounds += [1 for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]
    types += ['B' for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]

    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    constraints = []
    senses = []
    rhs = []
    
    # constarint 1
    for j in range(instance.n):
        for i in range(instance.g):
            variables = ["Y_{}_{}_{}".format(j,i,k) for k in range(instance.m[i])]
            coffiecient = [1] * instance.m[i]
            constraints.append([variables,coffiecient])
            senses.append('E')
            rhs.append(1)

    # constarint 2-1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,0)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0]) 

    # constarint 2-2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i])
    
    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.m[i]):
                    variables = ["C_{}_{}".format(j,i)]
                    variables += ["C_{}_{}".format(j1,i)]
                    variables += ["X_{}_{}_{}".format(j,j1,i)]
                    variables += ["Y_{}_{}_{}".format(j,i,k)]
                    variables += ["Y_{}_{}_{}".format(j1,i,k)]
                    coffiecient = [1, -1, -M, -M, -M]
                    constraints.append([variables,coffiecient])
                    senses.append('G')
                    rhs.append(instance.p[j][i]-3*M )
    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.m[i]):
                    variables = ["C_{}_{}".format(j1,i)]
                    variables += ["C_{}_{}".format(j,i)]
                    variables += ["X_{}_{}_{}".format(j,j1,i)]
                    variables += ["Y_{}_{}_{}".format(j,i,k)]
                    variables += ["Y_{}_{}_{}".format(j1,i,k)]
                    coffiecient = [1, -1, M, -M, -M]
                    constraints.append([variables,coffiecient])
                    senses.append('G')
                    rhs.append(instance.p[j1][i]-2*M )
    
    for j in range(instance.n):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.g-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)
           
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl

def flowshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}".format(j,j1) for j in range(instance.n) for j1 in range(j+1,instance.n)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,0)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0]) 

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j1,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i]-M )
    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j1,i)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["X_{}_{}".format(j,j1)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j1][i] )
    
    # constarint 5
    for j in range(instance.n):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.g-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)
        
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl

def Nonflowshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}_{}".format(j,j1,i) for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)

    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []
    
    # constarint 1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,0)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0]) 

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,i)]
            variables += ["C_{}_{}".format(j,i-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i])
   
    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j1,i)]
                variables += ["X_{}_{}_{}".format(j,j1,i)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i]-M )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j1,i)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["X_{}_{}_{}".format(j,j1,i)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j1][i] )
    
    # constarint 5
    for j in range(instance.n):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.g-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)

    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl


def jobshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}_{}".format(j,j1,i) for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(instance.n):
        variables = ["C_{}_{}".format(j,instance.r[j][0]-1)]
        coffiecient = [1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(instance.p[j][0])
    
    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            variables = ["C_{}_{}".format(j,instance.r[j][i]-1)]
            variables += ["C_{}_{}".format(j,instance.r[j][i-1]-1)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j1,i)]
                variables += ["X_{}_{}_{}".format(j,j1,i)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                #print(j,i,instance.r[j],instance.r[j].index(i+1),instance.p[j][instance.r[j].index(i+1)])
                rhs.append(instance.p[j][instance.r[j].index(i+1)]-M )
                
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j1,i)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["X_{}_{}_{}".format(j,j1,i)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j1][instance.r[j1].index(i+1)] )
    
    # constarint 5
    for j in range(instance.n):
        variables = ["C_max"]
        variables += ["C_{}_{}".format(j,instance.r[j][instance.g-1]-1)]
        coffiecient = [1, -1]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)
    
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    
    return mdl


def openshopmodel(instance,mdl):
    # Variable X
    names =  ["X_{}_{}_{}".format(j,j1,i) for j in range(instance.n) for j1 in range(j+1,instance.n) for i in range(instance.g)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    # Variable Y
    names +=  ["Y_{}_{}_{}".format(j,i,i1) for j in range(instance.n) for i in range(instance.g) for i1 in range(i+1,instance.g)]
    objective += [0 for j in range(instance.n) for i in range(instance.g) for i1 in range(i+1,instance.g)]
    lower_bounds += [0 for j in range(instance.n) for i in range(instance.g) for i1 in range(i+1,instance.g)]
    upper_bounds += [1 for j in range(instance.n) for i in range(instance.g) for i1 in range(i+1,instance.g)]
    types += ['B' for j in range(instance.n) for i in range(instance.g) for i1 in range(i+1,instance.g)]
    # Variable C
    names += ["C_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective += [0] * instance.n * instance.g
    lower_bounds += [0] * instance.n * instance.g
    upper_bounds += [V] * instance.n * instance.g
    types += ['C'] * instance.n * instance.g

    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    ###### Constarints ########
    constraints = []
    senses = []
    rhs = []

    # constarint 1
    for j in range(instance.n):
        for i in range(instance.g):
            variables = ["C_{}_{}".format(j,i)]
            coffiecient = [1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(instance.p[j][i]) 

    # constarint 2
    for j in range(instance.n):
        for i in range(instance.g):
            for i1 in range(i+1,instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j,i1)]
                variables += ["Y_{}_{}_{}".format(j,i,i1)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i]-M )
    
    # constarint 3
    for j in range(instance.n):
        for i in range(instance.g):
            for i1 in range(i+1,instance.g):
                variables = ["C_{}_{}".format(j,i1)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["Y_{}_{}_{}".format(j,i,i1)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i1] )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j,i)]
                variables += ["C_{}_{}".format(j1,i)]
                variables += ["X_{}_{}_{}".format(j,j1,i)]
                coffiecient = [1, -1, -M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j][i]-M )
    
    # constarint 5
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                variables = ["C_{}_{}".format(j1,i)]
                variables += ["C_{}_{}".format(j,i)]
                variables += ["X_{}_{}_{}".format(j,j1,i)]
                coffiecient = [1, -1, M]
                constraints.append([variables,coffiecient])
                senses.append('G')
                rhs.append(instance.p[j1][i] )
    
    # constarint 6
    for j in range(instance.n):
        for i in range(instance.g):
            variables = ["C_max"]
            variables += ["C_{}_{}".format(j,i)]
            coffiecient = [1, -1]
            constraints.append([variables,coffiecient])
            senses.append('G')
            rhs.append(0)
        
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl


def parallelmachinemodel(instance,mdl):
    
    # Variable Y
    names =  ["Y_{}_{}".format(j,i) for j in range(instance.n) for i in range(instance.g)]
    objective = [0] * len(names)
    lower_bounds = [0] * len(names)
    upper_bounds = [1] * len(names)
    types = ['B'] * len(names)
    
    # Variable Cmax
    names += ["C_max"]
    objective += [1]
    lower_bounds += [0]
    upper_bounds += [V]
    types += ['C']

    constraints = []
    senses = []
    rhs = []
    
    # constarint 1
    for j in range(instance.n):
        variables = ["Y_{}_{}".format(j,i) for i in range(instance.g)]
        coffiecient = [1] * instance.g
        constraints.append([variables,coffiecient])
        senses.append('E')
        rhs.append(1)
    
    # constarint 2
    for i in range(instance.g):
        variables = ["C_max"]
        coffiecient = [1]
        variables += ["Y_{}_{}".format(j,i) for j in range(instance.n)]
        coffiecient += [-1*instance.p[j][i] for j in range(instance.n)]
        constraints.append([variables,coffiecient])
        senses.append('G')
        rhs.append(0)
    
    mdl.variables.add(obj = objective,lb = lower_bounds,ub = upper_bounds,names = names, types = types)
    mdl.linear_constraints.add(lin_expr = constraints,senses = senses,rhs = rhs)
    mdl.objective.set_sense(mdl.objective.sense.minimize)
    return mdl
