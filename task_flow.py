from data import datastr

from ortools.graph.python import min_cost_flow
smcf = min_cost_flow.SimpleMinCostFlow()


workers = dict()
tasks = dict()
graph = set()
gra = []
ng = 0

lines = datastr.split('\n')
for ln in lines:
    col = ln.split('\t') 
    worker = col[0]
    task = col[1]
    cost = -int(float(col[2]))
    if not worker in graph:
        graph.add(worker)
        gra.append(worker)
        workers[worker] = ng
        smcf.set_node_supply(ng, 0)
        ng += 1
        
    if not task in graph:
        graph.add(task)    
        gra.append(task)
        tasks[task] = ng
        smcf.set_node_supply(ng, 0)
        ng+=1

    smcf.add_arc_with_capacity_and_unit_cost(workers[worker], tasks[task], 1, cost)


smcf.set_node_supply(ng, len(tasks))
smcf.set_node_supply(ng+1, -len(tasks))
for i in workers.values():
    smcf.add_arc_with_capacity_and_unit_cost(ng, i, 1, 0)

for i in tasks.values():
    smcf.add_arc_with_capacity_and_unit_cost(i, ng+1, 1, 0)

status = smcf.solve()
if status == smcf.OPTIMAL:
    print(f"Total cost = {smcf.optimal_cost()}")
    print()
    for arc in range(smcf.num_arcs()):
        # Can ignore arcs leading out of source or into sink.
        if smcf.tail(arc) < ng and smcf.head(arc) < ng:
            # Arcs in the solution have a flow value of 1. Their start and end nodes
            # give an assignment of worker to task.
            if smcf.flow(arc) > 0:
                print(
                    f"Worker {gra[smcf.tail(arc)]} assigned to task {gra[smcf.head(arc)]}.  Cost = {smcf.unit_cost(arc)}"
                )
else:
    print("There was an issue with the min cost flow input.")
    print(f"Status: {status}")
