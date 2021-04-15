import gc as gc
import sys as sys

import InformedSearch as Search
import invarith as P
import roots as roots
import UninformedSearch as BlindSearch

if len(sys.argv) < 4:
    print('usage: python runCD examplefile solver timelimit [depthlimit]')
    sys.exit()


file = open(sys.argv[1], 'r')
solver = sys.argv[2]
timelimit = int(sys.argv[3])

if solver not in ['BFS', 'DFS', 'DLS', 'IDS', 'UCS', 'GBFS', 'AStar']:
    print('solver', solver, 'not known')
    sys.exit()

if solver == 'DLS' and len(sys.argv) != 5:
    print('missing depthlimit for DLS (last arg)')
    sys.exit()

print(sys.argv)

examples = []
for line in file:
    line = line.rstrip().split(' ')
    line = [int(s) for s in line]
    examples.append((line[0],line[1:]))


print('target', 'size', 'depth', 'success', 'checked', 'time', 'nodes', 'space')

max_time = -1
max_depth = -1
count_unsolved = 0
total_time = 0
ebf = 0

for ex in examples:
    gc.collect()  # clean up any allocated memory now, before we start timing stuff

    if solver == 'BFS':
        problem = P.Problem(ex[0], ex[1])
        s = problem.create_initial_state()
        searcher = BlindSearch.Search(problem,timelimit=timelimit)
        answer = searcher.BreadthFirstSearch(s)

    elif solver == 'DFS':
        problem = P.Problem(ex[0], ex[1])
        s = problem.create_initial_state()
        searcher = BlindSearch.Search(problem,timelimit=timelimit)
        answer = searcher.DepthFirstSearch(s)

    elif solver == 'DLS':
        problem = P.Problem(ex[0], ex[1])
        s = problem.create_initial_state()
        searcher = BlindSearch.Search(problem,timelimit=timelimit)
        answer = searcher.DepthLimitedSearch(s, int(sys.argv[4]))

    elif solver == 'IDS':
        problem = P.Problem(ex[0], ex[1])
        s = problem.create_initial_state()
        searcher = BlindSearch.Search(problem,timelimit=timelimit)
        answer = searcher.IDS(s)

    elif solver == 'UCS':
        problem = P.InformedProblem(ex[0], ex[1])
        s = problem.create_initial_state()
        searcher = Search.InformedSearch(problem,timelimit=timelimit)
        answer = searcher.UCSSearch(s)

    elif solver == 'AStar':
        problem = P.InformedProblem(ex[0], ex[1])
        s = problem.create_initial_state()
        searcher = Search.InformedSearch(problem,timelimit=timelimit)
        answer = searcher.AStarSearch(s)

    elif solver == 'GBFS':
        problem = P.InformedProblem(ex[0], ex[1])
        s = problem.create_initial_state()
        searcher = Search.InformedSearch(problem,timelimit=timelimit)
        answer = searcher.BestFirstSearch(s)

    else:
        answer = None # and this will cause run time error below

    if answer.success:
        checked = eval(answer.result.state.expression()) == ex[0]
        print(ex[0], len(ex[1]), answer.result.depth, answer.success, checked,
              answer.time, answer.nodes, answer.space)

        ebf = ebf + roots.eff_br_fact(answer.nodes, answer.result.depth)
        if answer.time  > max_time:
            max_time = answer.time
        if answer.result.depth > max_depth:
            max_depth = answer.result.depth
    else:
        count_unsolved += 1
        print(ex[0], len(ex[1]), None, answer.success, None, answer.time, answer.nodes, answer.space, '*****')

    total_time += answer.time

print()
print("Attempted:", len(examples))
print("Unsolved:", count_unsolved)
print("Time cutoff:", timelimit)
print("Maximum time:", max_time)
print("Maximum depth:", max_depth)
print("Total time:", total_time)
print("Average effective branching factor:", ebf/(len(examples)-count_unsolved))
