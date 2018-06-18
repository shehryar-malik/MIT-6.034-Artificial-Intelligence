# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
from graphs import GRAPH1,GRAPH2,GRAPH3,GRAPH4,GRAPH5,SAQG,NEWGRAPH1,NEWGRAPH2,NEWGRAPH3,NEWGRAPH4
import Queue
## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    path = []
    q = Queue.Queue()
    q.put([start])

    while q.qsize()!=0:
        path = q.get()
        if path[len(path)-1] == goal:
            break
        all_nodes = graph.get_connected_nodes(path[len(path)-1])
        for node in all_nodes:
            lst = list(path)
            lst += node
            d = 0
            for i in range(0,len(lst)):
                for j in range(i+1,len(lst)):
                    if lst[j] == lst[i]:
                        d = 1
                        break
                if d == 1:
                    break
            if d == 0:
                if graph.is_valid_path(lst):
                    q.put(lst)

    if path[len(path)-1] != goal:
        path = []
    return path

## Once you have completed the breadth-first search,
## this part should be very simple to complete.


def dfs(graph, start, goal):
    path = []
    q = Queue.Queue()
    q.put([start])

    while q.qsize()!=0:
        path = q.get()
        if path[len(path) - 1] == goal:
            break
        all_nodes = graph.get_connected_nodes(path[len(path) - 1])
        for node in all_nodes:
            lst = list(path)
            lst += node
            d = 0
            for i in range(0, len(lst)):
                for j in range(i + 1, len(lst)):
                    if lst[j] == lst[i]:
                        d = 1
                        break
                if d == 1:
                    break
            if d == 0:
                if graph.is_valid_path(lst):
                    q_extra = Queue.Queue()
                    while q.qsize()!=0:
                        q_extra.put(q.get())
                    q.put(lst)
                    while q_extra.qsize()!=0:
                        q.put(q_extra.get())

    if path[len(path) - 1] != goal:
        path = []
    return path
#print dfs(GRAPH5,'S','G')
## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.


def hill_climbing(graph, start, goal):
    path = []
    q = Queue.Queue()
    q.put([start])

    while q.qsize()!=0:
        path = q.get()

        if path[len(path) - 1] == goal:
            return path

        all_nodes = graph.get_connected_nodes(path[len(path) - 1])

        lst_paths = []
        for node in all_nodes:
            lst = list(path)
            lst += node
            d = 0

            for i in range(0, len(lst)):
                for j in range(i + 1, len(lst)):
                    if lst[j] == lst[i]:
                        d = 1
                        break
                if d == 1:
                    break

            if d == 0:
                if graph.is_valid_path(lst):
                    lst_paths += [list(lst)]

        lst_paths = sorted(lst_paths, key=lambda path: graph.get_heuristic(path[len(path) - 1], goal))

        q_extra = Queue.Queue()

        while q.qsize() != 0:
            q_extra.put(q.get())

        for var in lst_paths:
            q.put(var)

        while q_extra.qsize() != 0:
            q.put(q_extra.get())

    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    path = []
    q = Queue.Queue()
    q.put([start])

    while q.qsize()!=0:

        all_nodes = []
        lst_paths = []

        while q.qsize() != 0:
            path = q.get()

            if path[len(path) - 1] == goal:
                return path

            all_nodes += graph.get_connected_nodes(path[len(path) - 1])

            for node in all_nodes:
                lst = list(path)
                lst += node

                d = 0
                for i in range(0, len(lst)):
                    for j in range(i + 1, len(lst)):
                        if lst[j] == lst[i]:
                            d = 1
                            break
                    if d == 1:
                        break

                if d == 0:
                    if graph.is_valid_path(lst):
                        lst_paths += [list(lst)]

        lst_paths_sorted = sorted(lst_paths, key=lambda var: graph.get_heuristic(var[len(var) - 1],goal))
        lst_paths_sorted = lst_paths_sorted[0:beam_width]

        for var1 in lst_paths:
            for var2 in lst_paths_sorted:
                if var1 == var2:
                    q.put(var1)

    return []

#print beam_search(NEWGRAPH2,'S','G',2)
## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.

def path_length(graph, node_names):
    length = 0
    for i in range(0,len(node_names)-1):
        for var in graph.edges:
            if graph.get_edge(node_names[i],node_names[i+1]) == var or graph.get_edge(node_names[i+1],node_names[i]) == var:
                length += var.length
    return length

def branch_and_bound(graph, start, goal):
    path = []
    q = Queue.Queue()
    q.put([start])

    while q.qsize()!=0:

        all_nodes = []
        lst_paths = []

        while q.qsize() != 0:
            path = q.get()

            if path[len(path) - 1] == goal:
                return path

            all_nodes += graph.get_connected_nodes(path[len(path) - 1])

            for node in all_nodes:
                lst = list(path)
                lst += node

                d = 0
                for i in range(0, len(lst)):
                    for j in range(i + 1, len(lst)):
                        if lst[j] == lst[i]:
                            d = 1
                            break
                    if d == 1:
                        break

                if d == 0:
                    if graph.is_valid_path(lst):
                        lst_paths += [list(lst)]

        while q.qsize() != 0:
            lst_paths += q.get()

        lst_paths_sorted = sorted(lst_paths, key=lambda var: graph.get_heuristic(var[len(var)-1],goal)+path_length(graph,var))

        for var in lst_paths_sorted:
            q.put(var)

    return []

def a_star(graph, start, goal):
    path = []
    extended_list = [start]
    q = Queue.Queue()
    q.put([start])

    while q.qsize() != 0:

        all_nodes = []
        lst_paths = []

        while q.qsize() != 0:
            path = q.get()

            if path[len(path) - 1] == goal:
                return path

            all_nodes += graph.get_connected_nodes(path[len(path) - 1])

            for node in all_nodes:
                c = 0
                for var in extended_list:
                    if var == node:
                        c = 1
                        break
                if c != 1:
                    extended_list += node

                    lst = list(path)
                    lst += node

                    d = 0
                    for i in range(0, len(lst)):
                        for j in range(i + 1, len(lst)):
                            if lst[j] == lst[i]:
                                d = 1
                                break
                        if d == 1:
                            break

                    if d == 0:
                        if graph.is_valid_path(lst):
                            lst_paths += [list(lst)]

        while q.qsize() != 0:
            lst_paths += q.get()

        lst_paths_sorted = sorted(lst_paths,
                                  key=lambda var: graph.get_heuristic(var[len(var) - 1], goal) + path_length(graph,
                                                                                                             var))
        for var in lst_paths_sorted:
            q.put(var)

    return []

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
            Hxg = graph.get_heuristic(node,goal)
            Dxg = path_length(graph,a_star(graph,node,goal))
            if Dxg < Hxg:
                return False
    return True

def is_consistent(graph, goal):
    for i in range(0, len(graph.nodes)):
        Hig = graph.get_heuristic(graph.nodes[i], goal)
        for j in range(i+1, len(graph.nodes)):
            Hjg = graph.get_heuristic(graph.nodes[j], goal)
            Dij = path_length(graph,a_star(graph,graph.nodes[i],graph.nodes[j]))
            if  Dij < abs(Hig - Hjg):
                return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '20'
WHAT_I_FOUND_INTERESTING = 'None'
WHAT_I_FOUND_BORING = 'None'
