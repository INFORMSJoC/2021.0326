#### Structure for instance data #######
class struct:
    def __init__(self):
        self.n = 0  #jobs
        self.g = 0  #stages
        self.f = 0 #factories

        self.o = [] #operations
        self.p = [] #processing_times
        self.r = [] #routes
        self.m = [] #machine
        self.d = [] #duedates
        self.s = [] #setup
        

####### data entry ########
def dataentry(filename,problemType):
    instance = struct();
    with open(filename,'r') as data:
        instance.n = int(data.readline().strip().split()[0])
        instance.g = int(data.readline().strip().split()[0])

        if problemType != 'Flexiblejobshop':
            if problemType == 'Distributedflowshop':
                instance.f = int(data.readline().strip().split()[0])
            
            if problemType == 'Hybridflowshop':
                instance.m =[int(x) for x in data.readline().strip().split()]

            if problemType == 'Tardinessflowshop':
                instance.d =[int(x) for x in data.readline().strip().split()]

            instance.p =[[int(x) for x in data.readline().strip().split()]]
            for j in range(instance.n-1):
                instance.p.append([int(x) for x in data.readline().strip().split()])

            if problemType == 'Setupflowshop':
                for i in range(instance.g):
                    instance.s.append([])
                    instance.s[i] =[[int(x) for x in data.readline().strip().split()]]
                    for j in range(instance.n-1):
                        instance.s[i].append([int(x) for x in data.readline().strip().split()])        

            if problemType == 'Jobshop':
                instance.r =[[int(x) for x in data.readline().strip().split()]]
                for j in range(instance.n-1):
                    instance.r.append([int(x) for x in data.readline().strip().split()])
        else:
            instance.o =[int(x) for x in data.readline().strip().split()]
            instance.p = [ [] for j in range(instance.n)]
            for j in range(instance.n):
                instance.p[j] = [ [] for k in range(instance.o[j])]
                for k in range(instance.o[j]):
                    x = [int(x) for x in data.readline().strip().split()]
                    for i in range(instance.g):
                        instance.p[j][k].append(x[i])

    print(instance.n)
    print(instance.g)
    #print(instance.p)
    #if problemType == 'Jobshop':
    #    print(instance.r)
    
    return instance
