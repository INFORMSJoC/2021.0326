from ortools.sat.python import cp_model
import collections
# https://developers.google.com/optimization/reference/python/sat/python/cp_model#bestobjectivebound
#https://developers.google.com/optimization/reference/python/linear_solver/pywraplp#bestbound

###### main ########
def CPmodel_generation(instance,mdl,problemType):

    if problemType == 'Flowshop':
        pass
        mdl = flowshopmodel(instance,mdl)
    if problemType == 'Non-Flowshop':               #done
        mdl = Nonflowshopmodel(instance,mdl)
    if problemType == 'Hybridflowshop':             #done
        mdl = Hybridflowshopmodel(instance,mdl)
    if problemType == 'Distributedflowshop':
        pass
        mdl = Distributedflowshopmodel(instance,mdl)
    if problemType == 'Nowaitflowshop':
        mdl = Nowaitflowshopmodel(instance,mdl)     #done
    if problemType == 'Setupflowshop':
        pass
        mdl = Setupflowshopmodel(instance,mdl)
    if problemType == 'Tardinessflowshop':
        pass
        mdl = Tardinessflowshopmodel(instance,mdl)
    if problemType == 'TCTflowshop':
        pass
        mdl = TCTflowshopmodel(instance,mdl)        
    if problemType == 'Jobshop':                    #done
        mdl = jobshopmodel(instance,mdl)
    if problemType == 'Flexiblejobshop':            #done
        mdl = Flexiblejobshopmodel(instance,mdl)
    if problemType == 'Openshop':                   #done
        mdl = openshopmodel(instance,mdl)
    if problemType == 'Parallelmachine':            #done
        mdl = prallelmachinemodel(instance,mdl)        
    return mdl


def Flexiblejobshopmodel(instance,mdl):

    horizon = 100000
    task_type = collections.namedtuple('task_type', 'start end is_present interval')

    all_tasks = {}    
    machine_to_intervals = collections.defaultdict(list)
    job_operation_to_intervals = [collections.defaultdict(list) for j in range(instance.n)]

    for j in range(instance.n):
        for k in range(instance.o[j]):
            for i in range(instance.g):
                if instance.p[j][k][i]== 0:
                    all_tasks[j, k, i] = []
                else:
                    suffix = '_%i_%i_%i' % (j, k, i)
                    start_var = mdl.NewIntVar(0, horizon, 'start' + suffix)
                    end_var = mdl.NewIntVar(0, horizon, 'end' + suffix)
                    is_present_var = mdl.NewBoolVar('is_present'+ suffix)
                    interval_var = mdl.NewOptionalIntervalVar(start_var, instance.p[j][k][i], end_var, is_present_var, 'interval' + suffix)
                    all_tasks[j, k, i] = task_type(start=start_var, end=end_var, is_present =is_present_var, interval=interval_var)
                    machine_to_intervals[i].append(interval_var)
                    job_operation_to_intervals[j][k].append(interval_var)

    for i in range(instance.g):
        mdl.AddNoOverlap(machine_to_intervals[i])

    for j in range(instance.n):
        for k in range(instance.o[j]):
            mdl.Add( sum([all_tasks[j, k, i].is_present for i in range(instance.g) if instance.p[j][k][i]>0]) == 1)

    for j in range(instance.n):
        for k in range(instance.o[j]-1):
            for i in range(instance.g):
                for i1 in range(instance.g):
                    if instance.p[j][k+1][i] > 0 and instance.p[j][k][i1]>0:
                        mdl.Add(all_tasks[j, k + 1, i].start >= all_tasks[j, k, i1].end )

    # Makespan objective.
    C_max = mdl.NewIntVar(0, horizon, 'C_max')
    mdl.AddMaxEquality(C_max, [all_tasks[j, instance.o[j]-1, i].end for j in range(instance.n) for i in range(instance.g) if instance.p[j][instance.o[j]-1][i]>0])
    mdl.Minimize(C_max)

    return mdl

def Hybridflowshopmodel(instance,mdl):

    horizon = 100000
    task_type = collections.namedtuple('task_type', 'start end is_present interval')

    all_tasks = {}
    
    machine_to_intervals = [ [] for i in range(instance.g)]
    for i in range(instance.g):
        machine_to_intervals[i] = [[] for k in range(instance.m[i])]
    
    #machine_to_intervals = collections.defaultdict(list)
    job_operation_to_intervals = [collections.defaultdict(list) for j in range(instance.n)]

    for j in range(instance.n):
        for i in range(instance.g):
            for k in range(instance.m[i]):
                suffix = '_%i_%i_%i' % (j, i, k)
                start_var = mdl.NewIntVar(0, horizon, 'start' + suffix)
                end_var = mdl.NewIntVar(0, horizon, 'end' + suffix)
                is_present_var = mdl.NewBoolVar('is_present'+ suffix)
                interval_var = mdl.NewOptionalIntervalVar(start_var, instance.p[j][i], end_var, is_present_var, 'interval' + suffix)
                all_tasks[j, i, k] = task_type(start=start_var, end=end_var, is_present =is_present_var, interval=interval_var)
                machine_to_intervals[i][k].append(interval_var)
                job_operation_to_intervals[j][i].append(interval_var)

    for i in range(instance.g):
        for k in range(instance.m[i]):
            mdl.AddNoOverlap(machine_to_intervals[i][k])

    for j in range(instance.n):
        for i in range(instance.g):
            mdl.Add( sum([all_tasks[j, i, k].is_present for k in range(instance.m[i])]) == 1)

    for j in range(instance.n):
        for i in range(instance.g-1):
            for k in range(instance.m[i+1]):
                for k1 in range(instance.m[i]):
                    mdl.Add(all_tasks[j, i + 1, k].start >= all_tasks[j, i, k1].end )

    # Makespan objective.
    C_max = mdl.NewIntVar(0, horizon, 'C_max')
    mdl.AddMaxEquality(C_max, [all_tasks[j, instance.g-1, k].end for j in range(instance.n) for k in range(instance.m[instance.g-1])])
    mdl.Minimize(C_max)

    return mdl


def openshopmodel(instance,mdl):

    horizon = sum([sum(instance.p[j]) for j in range(instance.n)])
    
    task_type = collections.namedtuple('task_type', 'start end interval')
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)
    job_to_intervals = collections.defaultdict(list)

    for j in range(instance.n):
        for i in range(instance.g):            
            suffix = '_%i_%i' % (j, i)
            start_var = mdl.NewIntVar(0, horizon, 'start' + suffix)
            end_var = mdl.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = mdl.NewIntervalVar(start_var, instance.p[j][i], end_var,'interval' + suffix)
            all_tasks[j, i] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[i].append(interval_var)
            job_to_intervals[j].append(interval_var)
            
    for i in range(instance.g):
        mdl.AddNoOverlap(machine_to_intervals[i])

    for j in range(instance.n):
        mdl.AddNoOverlap(job_to_intervals[j])

    # Makespan objective.
    C_max = mdl.NewIntVar(0, horizon, 'C_max')
    mdl.AddMaxEquality(C_max, [all_tasks[j, i].end for j in range(instance.n) for i in range(instance.g) ])
    mdl.Minimize(C_max)

    return mdl

def prallelmachinemodel(instance,mdl):
    Y = [[mdl.NewBoolVar(f'Y[{j}][{i}]') for i in range(instance.g)] for j in range(instance.n)]
    C_max = mdl.NewIntVar(0, sum([max(instance.p[j]) for j in range(instance.n)]) , 'C_max')

    for j in range(instance.n):
        mdl.AddExactlyOne(Y[j][i] for i in range(instance.g))
    mdl.AddMaxEquality(C_max, [sum([instance.p[j][i] * Y[j][i] for j in range(instance.n)]) for i in range(instance.g)])    
    mdl.Minimize(C_max)
    
    return mdl

def Nowaitflowshopmodel(instance,mdl):

    horizon = sum([sum(instance.p[j]) for j in range(instance.n)])
    
    task_type = collections.namedtuple('task_type', 'start end interval')
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for j in range(instance.n):
        for i in range(instance.g):
            suffix = '_%i_%i' % (j, i)
            start_var = mdl.NewIntVar(0, horizon, 'start' + suffix)
            end_var = mdl.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = mdl.NewIntervalVar(start_var, instance.p[j][i], end_var,'interval' + suffix)
            all_tasks[j, i] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[i].append(interval_var)

    for i in range(instance.g):
        mdl.AddNoOverlap(machine_to_intervals[i])

    for j in range(instance.n):
        for i in range(instance.g-1):
            mdl.Add(all_tasks[j, i + 1].start == all_tasks[j, i].end)

    C_max = mdl.NewIntVar(0, horizon, 'C_max')
    mdl.AddMaxEquality(C_max, [all_tasks[j, instance.g-1].end for j in range(instance.n)])
    mdl.Minimize(C_max)

    return mdl

def Nonflowshopmodel(instance,mdl):

    horizon = sum([sum(instance.p[j]) for j in range(instance.n)])

    task_type = collections.namedtuple('task_type', 'start end interval')
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for j in range(instance.n):
        for i in range(instance.g):
            suffix = '_%i_%i' % (j, i)
            start_var = mdl.NewIntVar(0, horizon, 'start' + suffix)
            end_var = mdl.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = mdl.NewIntervalVar(start_var, instance.p[j][i], end_var,'interval' + suffix)
            all_tasks[j, i] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[i].append(interval_var)

    for i in range(instance.g):
        mdl.AddNoOverlap(machine_to_intervals[i])

    for j in range(instance.n):
        for i in range(instance.g-1):
            mdl.Add(all_tasks[j, i + 1].start >= all_tasks[j, i].end)

    C_max = mdl.NewIntVar(0, horizon, 'C_max')
    mdl.AddMaxEquality(C_max, [all_tasks[j, instance.g-1].end for j in range(instance.n)])
    mdl.Minimize(C_max)

    return mdl

def jobshopmodel(instance,mdl):

    jobs_data = [ [] for j in range(instance.n)]
    for j in range(instance.n):
        jobs_data[j] = [(instance.r[j][i]-1, instance.p[j][i]) for i in range(instance.g)]   

    horizon = sum(task[1] for job in jobs_data for task in job)
    task_type = collections.namedtuple('task_type', 'start end interval')

    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = mdl.NewIntVar(0, horizon, 'start' + suffix)
            end_var = mdl.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = mdl.NewIntervalVar(start_var, duration, end_var,'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[machine].append(interval_var)
    
    for i in range(instance.g):
        mdl.AddNoOverlap(machine_to_intervals[i])

    for j in range(instance.n):
        for i in range(instance.g-1):
            mdl.Add(all_tasks[j, i + 1].start >= all_tasks[j, i].end)

    C_max = mdl.NewIntVar(0, horizon, 'C_max')
    mdl.AddMaxEquality(C_max, [all_tasks[j, len(job) - 1].end for j, job in enumerate(jobs_data)])
    mdl.Minimize(C_max)
    
    return mdl
