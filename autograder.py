# Ryan Shen
# rs280
# COMP 182 Spring 2026 - Homework 6, Problem 2, 3

# You may NOT import anything apart from already imported libraries.
# You can use helper functions from provided.py, but they have
# to be copied over here.

from typing import Tuple
from collections import *
from copy import *


def bfs(graph, startnode):
    """
        Perform a breadth-first search on digraph graph starting at node startnode.
        
        Arguments:
        graph -- directed graph
        startnode - node in graph to start the search from
        
        Returns:
        The distances from startnode to each node
    """
    dist = {}
    
    # Initialize distances
    for node in graph:
        dist[node] = float('inf')
    dist[startnode] = 0
    
    # Initialize search queue
    queue = deque([startnode])
    
    # Loop until all connected nodes have been explored
    while queue:
        node = queue.popleft()
        for nbr in graph[node]:
            if dist[nbr] == float('inf'):
                dist[nbr] = dist[node] + 1
                queue.append(nbr)
    return dist

# check typesssss
def _check_int(value, name: str) -> None:
    if not isinstance(value, int):
        raise TypeError(
            f"{name} must be an int; got value={value!r} (type={type(value).__name__})"
        )


def _check_tuple_of_ints(value, name: str) -> None:
    if not isinstance(value, tuple):
        raise TypeError(
            f"{name} must be a tuple; got value={value!r} (type={type(value).__name__})"
        )
    for item in value:
        if not isinstance(item, int):
            raise TypeError(
                f"{name} must contain only ints; got item={item!r} "
                f"(type={type(item).__name__}) in {value!r}"
            )


def _check_weighted_digraph(graph: dict, name: str) -> None:
    if not isinstance(graph, dict):
        raise TypeError(
            f"{name} must be a dict; got value={graph!r} (type={type(graph).__name__})"
        )

    for source, edges in graph.items():
        if not isinstance(source, int):
            raise TypeError(
                f"{name} keys must be ints; got key={source!r} "
                f"(type={type(source).__name__})"
            )
        if not isinstance(edges, dict):
            raise TypeError(
                f"{name}[{source!r}] must be a dict; got value={edges!r} "
                f"(type={type(edges).__name__})"
            )

        for dest, weight in edges.items():
            if not isinstance(dest, int):
                raise TypeError(
                    f"{name}[{source!r}] keys must be ints; got key={dest!r} "
                    f"(type={type(dest).__name__})"
                )
            if not isinstance(weight, (int, float)):
                raise TypeError(
                    f"{name}[{source!r}][{dest!r}] must be numeric; "
                    f"got value={weight!r} (type={type(weight).__name__})"
                )

def reverse_digraph_representation(graph: dict) -> dict:
    """
    This function takes in a digraph representation and returns its reversal

    inputs--
    graph: a digraph represented as a dict of dicts, where outer key is source node  
            and inner dict contains destination: weight entries

    outputs--
    reverse: a digraph represented as a dict of dicts, where outer key is destination 
            and inner dict contains source: weight entries
    """
    _check_weighted_digraph(graph, "graph")

    reverse = defaultdict(dict)
    for source, edges in graph.items():
        for dest, weight in edges.items():
            reverse[dest][source] = weight
        if source not in reverse.keys():
            reverse[source]

    
    return dict(reverse)

def modify_edge_weights(rgraph: dict, root: int) -> None:
    """
    This function takes in a reverse digraph representation
      and modifies the edge weights according to Lemma 2 
      (subtract min incoming edge weight from all incoming edges for a node)

    inputs--
    rgraph: a reverse digraph represented as a dict of dicts, where outer key is destination
             and inner dict contains edges as source: weight entries
    root: the root vertex of the graph

    outputs--
    mod_rgraph: a reverse digraph represented as a dict of dicts, where outer key is destination
             and inner dict contains edges as source: modified weight entries

    """
    _check_weighted_digraph(rgraph, "rgraph")
    _check_int(root, "root")

    # root must have no incoming edges; non-root nodes must have ≥1

    for end_node in rgraph:
        if end_node == root:
            continue
        try:
            min_weight = min(rgraph[end_node].values())
        except ValueError:
            min_weight = 0
        for start_node in rgraph[end_node]:
            rgraph[end_node][start_node] -= min_weight

def compute_rdst_candidate(rgraph: dict, root: int) -> dict:

    _check_weighted_digraph(rgraph, "rgraph")
    _check_int(root, "root")

    # print(rgraph)
    
    rdst_candidate = defaultdict(dict)
    for dest, redges in rgraph.items():
        # print(dest, redges)
        for source, weight in sorted(redges.items(), key=lambda item: item[1]):
            # print(source, weight)
            if dest not in rdst_candidate.keys():
                if dest == root:
                    rdst_candidate[dest]
                else:
                    rdst_candidate[dest][source] = weight

    # reversed representation
    rdst_candidate[root] = {}

    return dict(rdst_candidate)

def compute_cycle(rdst_candidate: dict) -> tuple:
    """
    This function checks for cycles in candidate (reversed) and returns them
    as a tuple of vertices in the cycle, in order of traversal. 

    assumes the candidate has already been processed by modify_edge_weights

    inputs--
        rdst_candidate: a reverse digraph represented as a dict of dicts, where outer
    outputs--
        cycle: a tuple of vertices in the cycle, in order of traversal (empty if no cycles)
    """
    _check_weighted_digraph(rdst_candidate, "rdst_candidate")

    state = {}
    for node in rdst_candidate:
        state[node] = 0
    
    for start in rdst_candidate:
        if state[start] != 0:
            continue

        path = []
        idx = {}

        curr = start

        while True:
            if curr is None:
                break
            if state[curr] == 2:
                break
            if state[curr] == 1:
                cycle_start_idx = idx[curr]
                return tuple(path[cycle_start_idx:])
            
            state[curr] = 1
            path.append(curr)
            idx[curr] = len(path) -1 #check for -1

            # print(f"current node is {curr}, path is {path}, state is {state}")
            if len(rdst_candidate[curr]) == 0:
                curr = None
            else:
                curr = next(iter(rdst_candidate[curr]))

        for node in path:
            state[node] = 2

    return()
 

def contract_cycle(graph: dict, cycle: tuple) -> Tuple[dict, int]:
    """"
    This function contracts a cycle in a graph into a single vertex c*.

    inputs--
        graph: a digraph represented as a dict of dicts, where outer key is source node  
            and inner dict contains destination: weight entries
        cycle: a tuple of vertices in the cycle, in order of traversal
    outputs--
        shrunk: a digraph represented as a dict of dicts

    
    """

    # print(f"{cycle} is seen")
    cycle = tuple(cycle)
    _check_weighted_digraph(graph, "graph")
    _check_tuple_of_ints(cycle, "cycle")

    shrunk = defaultdict(dict)
    rgraph = reverse_digraph_representation(graph)
    nodes = graph.keys()|rgraph.keys()
    c = max(nodes) +1

    for source, edge in graph.items():
        # check for isolated nodes
        if not edge:
            shrunk[source]

        for dest, weight in edge.items():

            # adds only nodes not adjacent to cycle elements 
            if dest not in cycle and source not in cycle:
                shrunk[source][dest] = weight

    # print(f"first pass: {dict(shrunk)}")
    for cyc_elem in cycle:
        # finds all nodes going into the cycle via rgraph repr
        rewires_in = rgraph[cyc_elem]
        # print(f"rewires_in = {rewires_in}")
        for source, weight in rewires_in.items():
            # routes them into c now
            if source not in cycle: 
                if c not in shrunk[source] or weight < shrunk[source][c]:
                    shrunk[source][c] = weight
                else:
                    shrunk[source]

        # print(f"after rewiring nodes into c* instead of cycle {dict(shrunk)}")
        # finds all nodes coming out of the cycle via standard rep
        rewires_out = graph[cyc_elem]
        # print(f"rewires_out = {rewires_out}")

        for destination, weight in rewires_out.items():
            # routes them all out through c now
            if destination not in cycle:
                if destination not in shrunk[c] or weight < shrunk[c][destination]:
                    shrunk[c][destination] = weight
            else:
                shrunk[c]
        # print(f"after rewiring nodes out of c* instead of cycle {dict(shrunk)}")

    return dict(shrunk), c


#remember candidate returns in the reversed repr
def expand_graph(graph: dict, rdst_candidate: dict, cycle: tuple, cstar: int) -> dict:
    """
    This function expands an rdst candidate computed on the contracted version of a graph
    inputs--
        graph: the original graph, in standard representation
        rdst_candidate: the rdst candidate computed on the contracted graph, in standard representation
        cycle: the cycle that was contracted, as a tuple of vertices in order of traversal
        cstar: the vertex in the contracted graph that represents the contracted cycle
    outputs--
        expanded: the expanded rdst candidate, in standard representation
    
    """
    cycle = tuple(cycle)

    expanded = defaultdict(dict)
    # expand contracted version of the graph
    
    # u, vstar : start out end in 

    for source, edge in rdst_candidate.items():
        for dest, weight in edge.items():
            if source != cstar and dest != cstar:
                expanded[source][dest] = weight
            # coutvout
            elif source == cstar and dest != cstar:
                # Find the minimum weight outgoing edge from cycle to dest
                candidates = [(cyc_elem, graph.get(cyc_elem, {}).get(dest)) 
                              for cyc_elem in cycle 
                              if dest in graph.get(cyc_elem, {})]
                if candidates:
                    c_out, c_out_weight = min(candidates, key=lambda x: x[1])
                    expanded[c_out][dest] = c_out_weight
            # uvstar
            elif source != cstar and dest == cstar:
                # Find the minimum weight incoming edge from source to cycle
                candidates = [(cyc_elem, graph.get(source, {}).get(cyc_elem))
                              for cyc_elem in cycle
                              if cyc_elem in graph.get(source, {})]
                if candidates:
                    vstar, vstar_weight = min(candidates, key=lambda x: x[1])
                    expanded[source][vstar] = vstar_weight


    # internal edges (cycle to cycle) are the same as in the original graph
    cycle = tuple(reversed(cycle))
    cidx = cycle.index(vstar)
    cycle = cycle[cidx:]+cycle[:cidx]

    cycle_shift = cycle[1:]+cycle[:1]

    print(f"Cycle: {cycle}, cycle_shift: {cycle_shift}, vstar: {vstar}")

    for node, next_node in zip(cycle, cycle_shift):
        if next_node != vstar:
            expanded[node][next_node] = graph[node][next_node]

    return dict(expanded)

def compute_rdmst(graph, root):
    """
        This function checks if:
        (1) root is a node in digraph graph, and
        (2) every node, other than root, is reachable from root
        If both conditions are satisfied, it calls compute_rdmst_helper
        on (graph, root).
        
        Since compute_rdmst_helper modifies the edge weights as it computes,
        this function reassigns the original weights to the RDMST.
        
        Arguments:
        graph -- a weighted digraph in standard dictionary representation.
        root -- a node id.
        
        Returns:
        An RDMST of graph rooted at r and its weight, if one exists;
        otherwise, nothing.
    """
    
    if root not in graph:
        print ("The root node does not exist")
        return
    
    distances = bfs(graph, root)
    for node in graph:
        if distances[node] == float('inf'):
            print ("The root does not reach every other node in the graph")
            return

    rdmst = compute_rdmst_helper(graph, root)
    
    # reassign the original edge weights to the RDMST and computes the total
    # weight of the RDMST
    rdmst_weight = 0
    for node in rdmst:
        for nbr in rdmst[node]:
            rdmst[node][nbr] = graph[node][nbr]
            rdmst_weight += rdmst[node][nbr]

    return (rdmst,rdmst_weight)

def compute_rdmst_helper(graph,root):
    """
        Computes the RDMST of a weighted digraph rooted at node root.
        It is assumed that:
        (1) root is a node in graph, and
        (2) every other node in graph is reachable from root.
        
        Arguments:
        graph -- a weighted digraph in standard dictionary representation.
        root -- a node in graph.
        
        Returns:
        An RDMST of graph rooted at root. The weights of the RDMST
        do not have to be the original weights.
        """
    
    # reverse the representation of graph
    rgraph = reverse_digraph_representation(graph)
    
    # Step 1 of the algorithm
    modify_edge_weights(rgraph, root)
    
    # Step 2 of the algorithm
    rdst_candidate = compute_rdst_candidate(rgraph, root)
    
    # compute a cycle in rdst_candidate
    cycle = compute_cycle(rdst_candidate)
    
    # Step 3 of the algorithm
    if not cycle:
        return reverse_digraph_representation(rdst_candidate)
    else:
        # Step 4 of the algorithm
        
        g_copy = deepcopy(rgraph)
        g_copy = reverse_digraph_representation(g_copy)
        
        # Step 4(a) of the algorithm
        (contracted_g, cstar) = contract_cycle(g_copy, cycle)
        #cstar = max(contracted_g.keys())
        
        # Step 4(b) of the algorithm
        new_rdst_candidate = compute_rdmst_helper(contracted_g, root)
        
        # Step 4(c) of the algorithm
        rdmst = expand_graph(reverse_digraph_representation(rgraph), new_rdst_candidate, cycle, cstar)

        return rdmst
# --------------------------------------------------

# test cases //

# if __name__ == "__main__":
#     g4 = {1: {2: 2.1, 3: 1.0, 4: 9.1, 5: 1.1, 6: 10.1, 7: 10.1, 8: 6.1, 9: 11.0, 10: 10.1}, 2: {1: 2.1, 3: 1.0, 4: 17.0, 5: 1.0, 6: 18.1, 7: 18.1, 8: 14.1, 9: 19.1, 10: 18.0}, 3: {1: 1.0, 2: 1.0, 4: 16.0, 5: 0.0, 6: 17.0, 7: 17.0, 8: 13.1, 9: 18.1, 10: 17.0}, 4: {1: 9.1, 2: 17.1, 3: 16.0, 5: 16.0, 6: 5.1, 7: 5.1, 8: 15.1, 9: 6.1, 10: 5.0}, 5: {1: 1.1, 2: 1.0, 3: 0.0, 4: 16.0, 6: 17.1, 7: 17.1, 8: 13.1, 9: 18.1, 10: 17.0}, 6: {1: 10.1, 2: 18.1, 3: 17.0, 4: 5.1, 5: 17.1, 7: 0.0, 8: 16.1, 9: 7.1, 10: 0.0}, 7: {1: 10.1, 2: 18.1, 3: 17.0, 4: 5.1, 5: 17.1, 6: 0.0, 8: 16.0, 9: 7.1, 10: 0.0}, 8: {1: 6.1, 2: 14.1, 3: 13.1, 4: 15.1, 5: 13.1, 6: 16.1, 7: 16.0, 9: 17.1, 10: 16.1}, 9: {1: 11.1, 2: 19.1, 3: 18.1, 4: 6.1, 5: 18.1, 6: 7.1, 7: 7.1, 8: 17.1, 10: 7.0}, 10: {1: 10.1, 2: 18.1, 3: 17.1, 4: 5.1, 5: 17.0, 6: 0.0, 7: 0.0, 8: 16.1, 9: 7.0}}
#     # Results for compute_rdmst(g4, 1):
#     soln = ({1: {8: 6.1, 3: 1.0, 4: 9.1}, 2: {}, 3: {2: 1.0, 5: 0.0}, 4: {9: 6.1, 10: 5.0}, 5: {}, 6: {7: 0.0}, 7: {}, 8: {}, 9: {}, 10: {6: 0.0}}, 28.3)

#     # original
#     # render_graph(g4, filename="original", output_dir="visualizations")
#     # soln
#     render_graph(soln[0], filename=f"soln_", output_dir="visualizations")
#     print(f"final: {compute_rdmst(g4, 1)}")
#     render_graph(compute_rdmst(g4, 1)[0], filename=f"rdmst", output_dir="visualizations")

    # g3 = {1: {2: 2.1, 3: 1.0, 4: 9.1, 5: 1.1}, 2: {1: 2.1, 3: 1.0, 4: 17.0, 5: 1.0}, 3: {1: 1.0, 2: 1.0, 4: 16.0, 5: 0.0}, 4: {1: 9.1, 2: 17.1, 3: 16.0, 5: 16.0}, 5: {1: 1.1, 2: 1.0, 3: 0.0, 4: 16.0}}
    # # Results for compute_rdmst(g3, 1):
    # soln = ({1: {3: 1.0, 4: 9.1}, 2: {}, 3: {2: 1.0, 5: 0.0}, 4: {}, 5: {}}, 11.1)
    #     # original
#     render_graph(g3, filename="original", output_dir="visualizations")
#     soln
#     render_graph(soln[0], filename=f"soln_", output_dir="visualizations")
#     print(f"final: {compute_rdmst(g3, 1)}")
#     render_graph(compute_rdmst(g3, 1)[0], filename=f"rdmst", output_dir="visualizations")


