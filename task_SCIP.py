from data import datastr
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver("SCIP")



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
    cost = float(col[2])
    x[worker, task] = solver.IntVar(0, 1, "")
    workers.add(worker)
    tasks.add(task)
    costs[worker, task] = cost
    objective.append(cost * x[worker, task])


# Each worker is assigned to at most 1 task.
for i in workers:
    solver.Add(solver.Sum([x[i, j] for j in tasks]) <= 1)

# Each task is assigned to exactly one worker.
for j in tasks:
    solver.Add(solver.Sum([x[i, j] for i in workers]) == 1)


solver.Maximize(sum(objective))
status = solver.Solve()
print(f"Total max cost = {solver.Objective().Value()}\n")

solver.Minimize(sum(objective))
status = solver.Solve()
print(f"Total min cost = {solver.Objective().Value()}\n")

'''
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value()}\n")
    for i in workers:
        for j in tasks:
            # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
            if x[i, j].solution_value() > 0.5:
                print(f"Worker {i} assigned to task {j}." + f" Cost: {costs[i, j]}")
else:
    print("No solution found.")
'''    