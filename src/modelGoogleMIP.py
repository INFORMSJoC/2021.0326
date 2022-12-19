from ortools.linear_solver import pywraplp

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


def Flexiblejobshopmodel(instance,mdl):
    Z = [[[mdl.BoolVar(f'Z[{j}][{k}][{i}]') for i in range(instance.g)] for k in range(instance.o[j])] for j in range(instance.n)]
    #X = [[[[mdl.BoolVar(f'X[{j}][{k}][{j1}][{k1}]') for k1 in range(instance.o[j1])] for k in range(instance.o[j])] for j1 in range(instance.n)] for j in range(instance.n)]

    X = [[] for j in range(instance.n)]
    for j in range(instance.n):
        X[j] = [[] for k in range(instance.o[j])]
        for k in range(instance.o[j]):
            X[j][k] = [[] for j1 in range(instance.n)]
            for j1 in range(instance.n):
                X[j][k][j1] = [mdl.BoolVar(f'X[{j}][{k}][{j1}][{k1}]') for k1 in range(instance.o[j1])]
    
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{k}]') for k in range(instance.o[j])] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')

    # constarint 1
    for j in range(instance.n):
        for k in range(instance.o[j]):
            mdl.Add(sum([Z[j][k][i] for i in range(instance.g) if instance.p[j][k][i] > 0]) == 1)

    # constarint 2
    for j in range(instance.n):
        for k in range(instance.o[j]):
            if k == 0:
                mdl.Add(C[j][k] - sum([instance.p[j][k][i] * Z[j][k][i] for i in range(instance.g) if instance.p[j][k][i] > 0]) >= 0)
            else:
                mdl.Add(C[j][k] - C[j][k-1] - sum([instance.p[j][k][i] * Z[j][k][i] for i in range(instance.g) if instance.p[j][k][i] > 0]) >= 0)

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for k in range(instance.o[j]):
                for k1 in range(instance.o[j1]):
                    for i in range(instance.g):
                        if instance.p[j][k][i] > 0 and instance.p[j1][k1][i]>0:
                            mdl.Add(C[j][k] - C[j1][k1] - M * X[j][k][j1][k1] - M * Z[j][k][i] - M * Z[j1][k1][i] >= instance.p[j][k][i]-3*M)

     # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for k in range(instance.o[j]):
                for k1 in range(instance.o[j1]):
                    for i in range(instance.g):
                        if instance.p[j][k][i] > 0 and instance.p[j1][k1][i]>0:
                            mdl.Add(C[j1][k1] - C[j][k] + M * X[j][k][j1][k1] - M * Z[j][k][i] - M * Z[j1][k1][i] >= instance.p[j1][k1][i]-2*M)
                
    # constarint 5
    for j in range(instance.n):
        for k in range(instance.o[j]):
            mdl.Add(C_max - C[j][k] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl


def parallelmachinemodel(instance,mdl):
    Y = [[mdl.BoolVar(f'Y[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')

    # constarint 1
    for j in range(instance.n):
        mdl.Add(sum([Y[j][i] for i in range(instance.g)]) == 1)

    # constarint 2
    for i in range(instance.g):
        mdl.Add(C_max - sum([instance.p[j][i] * Y[j][i] for j in range(instance.n)]) >= 0)

    mdl.Minimize(C_max)
            
    return mdl


def openshopmodel(instance,mdl):
    X = [[[mdl.BoolVar(f'X[{j}][{j1}][{i}]') for i in range(instance.g)] for j1 in range(instance.n)] for j in range(instance.n)]
    Y = [[[mdl.BoolVar(f'Y[{j}][{i1}][{i1}]') for i1 in range(instance.g)] for i in range(instance.g)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')
        
    # constarint 1
    for j in range(instance.n):
        for i in range(instance.g):
            mdl.Add(C[j][i] >= instance.p[j][i])

    # constarint 2
    for j in range(instance.n):
        for i in range(instance.g):
            for i1 in range(i+1,instance.g):
                mdl.Add( C[j][i] - C[j][i1] - M * Y[j][i][i1] >= instance.p[j][i]-M )

    # constarint 3
    for j in range(instance.n):
        for i in range(instance.g):
            for i1 in range(i+1,instance.g):
                mdl.Add( C[j][i1] - C[j][i] + M * Y[j][i][i1] >= instance.p[j][i1] )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add( C[j][i] - C[j1][i] - M * X[j][j1][i] >= instance.p[j][i]-M )
 
    # constarint 5
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add( C[j1][i] - C[j][i] + M * X[j][j1][i] >= instance.p[j1][i] )
                
    # constarint 6
    for j in range(instance.n):
        for i in range(instance.g):
            mdl.Add(C_max - C[j][i] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl


def Distributedflowshopmodel(instance,mdl):
    Y = [[mdl.BoolVar(f'Y[{j}][{k}]') for k in range(instance.f)] for j in range(instance.n)]
    X = [[mdl.BoolVar(f'X[{j}][{j1}]') for j1 in range(instance.n)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')

    # constarint 1
    for j in range(instance.n):
        mdl.Add(sum([Y[j][k] for k in range(instance.f)]) == 1)
       
    # constarint 2
    for j in range(instance.n):
        mdl.Add(C[j][0] >= instance.p[j][0])

    # constarint 2-1
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] >= instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.f):
                    mdl.Add(C[j][i] - C[j1][i]  - M * Y[j][k] - M * Y[j1][k] - M * X[j][j1] >= instance.p[j][i]-3*M )
                    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.f):
                    mdl.Add(C[j1][i] - C[j][i]  - M * Y[j][k] - M * Y[j1][k] + M * X[j][j1] >= instance.p[j1][i]-2*M )
                
    # constarint 5
    for j in range(instance.n):
        mdl.Add(C_max - C[j][instance.g-1] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl


def Hybridflowshopmodel(instance,mdl):
    Y = [[[mdl.BoolVar(f'Y[{j}][{i}][{k}]') for k in range(instance.m[i])] for i in range(instance.g)] for j in range(instance.n)]
    X = [[[mdl.BoolVar(f'X[{j}][{j1}][{i}]') for i in range(instance.g)] for j1 in range(instance.n)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')

    # constarint 1
    for j in range(instance.n):
        for i in range(instance.g):
            mdl.Add(sum([Y[j][i][k] for k in range(instance.m[i])]) == 1)
       
    # constarint 2
    for j in range(instance.n):
        mdl.Add(C[j][0] >= instance.p[j][0])

    # constarint 2-1
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] >= instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.m[i]):
                    mdl.Add(C[j][i] - C[j1][i]  - M * Y[j][i][k] - M * Y[j1][i][k] - M * X[j][j1][i] >= instance.p[j][i]-3*M )
                    
    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                for k in range(instance.m[i]):
                    mdl.Add(C[j1][i] - C[j][i]  - M * Y[j][i][k] - M * Y[j1][i][k] + M * X[j][j1][i] >= instance.p[j1][i]-2*M )
                
    # constarint 5
    for j in range(instance.n):
        mdl.Add(C_max - C[j][instance.g-1] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl


def Nonflowshopmodel(instance,mdl):
    X = [[[mdl.BoolVar(f'X[{j}][{j1}][{i}]') for i in range(instance.g)] for j1 in range(instance.n)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')
        
    # constarint 1
    for j in range(instance.n):
        mdl.Add(C[j][0] >= instance.p[j][0])

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] >= instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1][i] >= instance.p[j][i]-M )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j1][i] - C[j][i] + M * X[j][j1][i] >= instance.p[j1][i] )
                
    # constarint 5
    for j in range(instance.n):
        mdl.Add(C_max - C[j][instance.g-1] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl


def Nowaitflowshopmodel(instance,mdl):
    X = [[mdl.BoolVar(f'X[{j}][{j1}]') for j1 in range(instance.n)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')
        
    # constarint 1
    for j in range(instance.n):
        mdl.Add(C[j][0] >= instance.p[j][0])

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] == instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1] >= instance.p[j][i]-M )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j1][i] - C[j][i] + M * X[j][j1] >= instance.p[j1][i] )
                
    # constarint 5
    for j in range(instance.n):
        mdl.Add(C_max - C[j][instance.g-1] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl




def Setupflowshopmodel(instance,mdl):
    X = [[mdl.BoolVar(f'X[{j}][{j1}]') for j1 in range(instance.n+1)] for j in range(instance.n+1)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n+1)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')

    # constarint 1
    for j in range(1,instance.n+1):
        mdl.Add(sum([X[j][j1] for j1 in range(instance.n+1) if j1 != j]) == 1)
        
    # constarint 2
    for j1 in range(1,instance.n+1):
        mdl.Add(sum([X[j][j1] for j in range(1,instance.n+1) if j1 != j]) <= 1)

    # constarint 2-1
    mdl.Add(sum([X[j][0] for j in range(1,instance.n+1)]) == 1)

    # constarint 3
    for j in range(1,instance.n+1):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] >= instance.p[j-1][i])

    # constarint 4
    for j in range(1,instance.n+1):
        for j1 in range(instance.n+1):
            if j1 != j:
                for i in range(instance.g):
                    if j1 == 0:
                        mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1] >= instance.p[j-1][i]-M )
                    else:
                        mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1] >= instance.p[j-1][i]+instance.s[i][j1-1][j-1]-M )
                        
    # constarint 5
    for j in range(1,instance.n+1):
        mdl.Add(C_max - C[j][instance.g-1] >= 0 )
        
    mdl.Minimize(C_max)
            
    return mdl


def Tardinessflowshopmodel(instance,mdl):
    X = [[mdl.BoolVar(f'X[{j}][{j1}]') for j1 in range(instance.n)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    T = [mdl.NumVar(0, mdl.infinity(), f'T[{j}]') for j in range(instance.n)]
        
    # constarint 1
    for j in range(instance.n):
        mdl.Add(C[j][0] >= instance.p[j][0])

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] >= instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1] >= instance.p[j][i]-M )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j1][i] - C[j][i] + M * X[j][j1] >= instance.p[j1][i] )
                
    # constarint 5
    for j in range(instance.n):
        mdl.Add(T[j] - C[j][instance.g-1] >= -1*instance.d[j] )

        
    mdl.Minimize(sum([T[j] for j in range(instance.n)]))
            
    return mdl


def TCTflowshopmodel(instance,mdl):
    X = [[mdl.BoolVar(f'X[{j}][{j1}]') for j1 in range(instance.n)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
        
    # constarint 1
    for j in range(instance.n):
        mdl.Add(C[j][0] >= instance.p[j][0])

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] >= instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1] >= instance.p[j][i]-M )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j1][i] - C[j][i] + M * X[j][j1] >= instance.p[j1][i] )
                
    mdl.Minimize(sum([C[j][instance.g-1] for j in range(instance.n)]))
            
    return mdl


def flowshopmodel(instance,mdl):
    X = [[mdl.BoolVar(f'X[{j}][{j1}]') for j1 in range(instance.n)] for j in range(instance.n)]
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')
        
    # constarint 1
    for j in range(instance.n):
        mdl.Add(C[j][0] >= instance.p[j][0])

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][i] - C[j][i-1] >= instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1] >= instance.p[j][i]-M )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j1][i] - C[j][i] + M * X[j][j1] >= instance.p[j1][i] )
                
    # constarint 5
    for j in range(instance.n):
        mdl.Add(C_max - C[j][instance.g-1] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl


def jobshopmodel(instance,mdl):
    X = [[[mdl.BoolVar(f'X[{j}][{j1}][{i}]') for i in range(instance.g)] for j1 in range(instance.n)] for j in range(instance.n)]
    #X = [mdl.BoolVar(f'x[{i}]')) for i in range(n)] IntVar
    C = [[mdl.NumVar(0, mdl.infinity(), f'C[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NumVar(0, mdl.infinity(), 'C_max')
        
    # constarint 1
    for j in range(instance.n):
        mdl.Add(C[j][instance.r[j][0]-1] >= instance.p[j][0])

    # constarint 2
    for j in range(instance.n):
        for i in range(1,instance.g):
            mdl.Add(C[j][instance.r[j][i]-1] - C[j][instance.r[j][i-1]-1] >= instance.p[j][i])

    # constarint 3
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j][i] - C[j1][i] - M * X[j][j1][i] >= instance.p[j][instance.r[j].index(i+1)]-M )

    # constarint 4
    for j in range(instance.n-1):
        for j1 in range(j+1,instance.n):
            for i in range(instance.g):
                mdl.Add(C[j1][i] - C[j][i] + M * X[j][j1][i] >= instance.p[j1][instance.r[j1].index(i+1)] )
                
    # constarint 5
    for j in range(instance.n):
        mdl.Add(C_max - C[j][instance.r[j][instance.g-1]-1] >= 0 )

    mdl.Minimize(C_max)
            
    return mdl


























