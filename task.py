from data import datastr
from ortools.sat.python import cp_model
model = cp_model.CpModel()



workers = set()
tasks = set()
costs = dict()
x = dict()
objective = []


lines = datastr.split('\n')
for ln in lines:
    col = ln.split('\t') 
    worker = col[0]
    task = col[1]
    cost = int(float(col[2]))
    x[worker, task] = model.NewBoolVar(f"x[{worker},{task}]")
    workers.add(worker)
    tasks.add(task)
    costs[worker, task] = cost
    objective.append(cost * x[worker, task])


for worker in workers:
    model.AddAtMostOne(x[worker, task] for task in tasks)

# Each task is assigned to exactly one worker.
for task in tasks:
    model.AddExactlyOne(x[worker, task] for worker in workers)

'''
model.Maximize(sum(objective))
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Total max cost = {solver.ObjectiveValue()}\n")
else:
    print("No solution found.")

model.Minimize(sum(objective))
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Total max cost = {solver.ObjectiveValue()}\n")
else:
    print("No solution found.")    
'''
#model.Minimize(sum(objective))
model.Maximize(sum(objective))
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Total cost = {solver.ObjectiveValue()}, time = {solver.WallTime()}\n")
    
    for worker in workers:
        for task in tasks:
            if solver.BooleanValue(x[worker, task]):
                print(
                    f"Worker {worker} assigned to task {task}."
                    + f" Cost = {costs[worker, task]}"
                )
else:
    print("No solution found.")
