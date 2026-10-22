# Ryan Shen
# rs280
# COMP 182 Spring 2021 - Homework 5, Problem 4

# You can import any standard library, as well as Numpy and Matplotlib.
# You can use helper functions from provided.py, and autograder.py,
# but they have to be copied over here.

from collections import defaultdict

### Functions for use in Problem 4
# AUTOGRADER STUFF
from typing import Tuple
from collections import *
from copy import *


# Ryan Shen
# rs280
# COMP 182 Spring 2026 - Homework 6, Problem 2, 3

# You may NOT import anything apart from already imported libraries.
# You can use helper functions from provided.py, but they have
# to be copied over here.

# TEST CONFIG {
# # test_sequence1.txt:
# # 01000000000000000000000000000000000001011
# # 10000000000000000000000001000000011110000

# sample_trace1.txt:
# 1 2 3 4 5 6 7
# 0.5 0 0 0 0 0 0
# 0 1.5 0 0 0 0 0
# 0 0 2.5 0 0 0 0
# 0 0 0 3.5 0 0 0
# 0 0 0 0 4.5 0 0
# 0 0 0 0 0 5.5 0
# 0 0 0 0 0 0 6.5

# test_sequence2.txt:
# # 01000000000000100000000000000000000001011
# # 10000000000000100000000001000000011110000

# sample_trace_min_2.txt
# 1 2 3 4 5 6 7
# 0.5 0 0 0 0 0 0
# 0 1.5 0 0 0 0 0
# 0 0 2.5 0 0 0 0
# 0 0 0 3.5 0 0 0
# 0 0 0 0 4.5 0 0
# 0 0 0 0 0 5.5 0
# 0 0 0 0 0 0 6.5


# VIZ
from pathlib import Path

from graphviz import Digraph, Graph


def build_graphviz(g, directed=True, name="G"):
    """Build a Graphviz graph from an adjacency mapping.

    Supports dict-of-dict adjacency for weighted edges, e.g.:
    {0: {2: 4}, 2: {3: 7}}
    """
    dot = Digraph(name=name) if directed else Graph(name=name)

    for u, nbrs in g.items():
        dot.node(str(u))

        if isinstance(nbrs, dict):
            for v, w in nbrs.items():
                dot.node(str(v))
                edge_attrs = {"label": str(w)} if w is not None else {}
                dot.edge(str(u), str(v), **edge_attrs)
        else:
            for v in nbrs:
                dot.node(str(v))
                dot.edge(str(u), str(v))

    return dot


def render_graph(g, filename="graph", output_dir="visualizations", directed=True, fmt="png"):
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dot = build_graphviz(g, directed=directed)
    output_path = dot.render(filename=filename, directory=str(out_dir), format=fmt, cleanup=False)
    return output_path, dot.source

# AUTOGRADER
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

# PROVIDED FXNS
def infer_transmap(gen_data, epi_data, patient_id):
    """
        Infers a transmission map based on genetic
        and epidemiological data rooted at patient_id
        
        Arguments:
        gen_data -- filename with genetic data for each patient
        epi_data -- filename with epidemiological data for each patient
        patient_id -- the id of the 'patient 0'
        
        Returns:
        The most likely transmission map for the given scenario as the RDMST 
        of a weighted, directed, complete digraph
        """
    
    complete_digraph = construct_complete_weighted_digraph(gen_data, epi_data)
    return compute_rdmst(complete_digraph, patient_id)


def read_patient_sequences(filename):
    """
        Turns the bacterial DNA sequences (obtained from patients) into a list containing tuples of
        (patient ID, sequence).
        
        Arguments:
        filename -- the input file containing the sequences
        
        Returns:
        A list of (patient ID, sequence) tuples.
        """
    sequences = []
    with open(filename) as f:
        line_num = 0
        for line in f:
            if len(line) > 5:
                patient_num, sequence = line.split("\t")
                sequences.append( (int(patient_num), ''.join(e for e in sequence if e.isalnum())) )
    return sequences

def read_patient_traces(filename):
    """
        Reads the epidemiological data file and computes the pairwise epidemiological distances between patients
        
        Arguments:
        filename -- the input file containing the sequences
        
        Returns:
        A dictionary of dictionaries where dict[i][j] is the
        epidemiological distance between i and j.
    """
    trace_data = []
    patient_ids = []
    first_line = True
    with open(filename) as f:
        for line in f:
            if first_line:
                patient_ids = line.split()
                patient_ids = list(map(int, patient_ids))
                first_line = False
            elif len(line) > 5:
                trace_data.append(line.rstrip('\n'))
    return compute_pairwise_epi_distances(trace_data, patient_ids)

def compute_pairwise_gen_distances(sequences, distance_function):
    """
        Computes the pairwise genetic distances between patients (patients' isolate genomes)
        
        Arguments:
        sequences -- a list of sequences that correspond with patient id's
        distance_function -- the distance function to apply to compute the weight of the 
        edges in the returned graph
        
        Returns:
        A dictionary of dictionaries where gdist[i][j] is the
        genetic distance between i and j.
        """
    gdist = {}
    cultures = {}
    
    # Count the number of differences of each sequence
    for i in range(len(sequences)):
        patient_id = sequences[i][0]
        seq = sequences[i][1]
        if patient_id in cultures:
            cultures[patient_id].append(seq)
        else:
            cultures[patient_id] = [seq]
            gdist[patient_id] = {}
    # Add the minimum sequence score to the graph
    for pat1 in range(1, max(cultures.keys()) + 1):
        for pat2 in range(pat1 + 1, max(cultures.keys()) + 1):
            min_score = float("inf")
            for seq1 in cultures[pat1]:
                for seq2 in cultures[pat2]:
                    score = distance_function(seq1, seq2)
                    if score < min_score:
                        min_score = score
            gdist[pat1][pat2] = min_score
            gdist[pat2][pat1] = min_score
    return gdist

### HELPER FUNCTIONS. ###

def find_first_positives(trace_data):
    """
        Finds the first positive test date of each patient
        in the trace data.
        Arguments:
        trace_data -- a list of data pertaining to location
        and first positive test date
        Returns:
        A dictionary with patient id's as keys and first positive
        test date as values. The date numbering starts from 0 and
        the patient numbering starts from 1.
        """
    first_pos = {}
    for pat in range(len(trace_data[0])):
        first_pos[pat + 1] = None
        for date in range(len(trace_data)):
            if trace_data[date][pat].endswith(".5"):
                first_pos[pat + 1] = date
                break
    return first_pos



def compute_epi_distance(pid1, pid2, trace_data, first_pos1, first_pos2, patient_ids):
    """
        Computes the epidemiological distance between two patients.
        
        Arguments:
        pid1 -- the assumed donor's index in trace data
        pid2 -- the assumed recipient's index in trace data
        trace_data -- data for days of overlap and first positive cultures
        first_pos1 -- the first positive test day for pid1
        first_pos2 -- the first positive test day for pid2
        patient_ids -- an ordered list of the patient IDs given in the text file
        
        Returns:
        Finds the epidemiological distance from patient 1 to
        patient 2.
        """
    first_overlap = -1
    assumed_trans_date = -1
    pid1 = patient_ids.index(pid1)
    pid2 = patient_ids.index(pid2)
    # Find the first overlap of the two patients
    for day in range(len(trace_data)):
        if (trace_data[day][pid1] == trace_data[day][pid2]) & \
            (trace_data[day][pid1] != "0"):
            first_overlap = day
            break
    if (first_pos2 < first_overlap) | (first_overlap < 0):
        return len(trace_data) * 2 + 1
    # Find the assumed transmission date from patient 1 to patient 2
    for day in range(first_pos2, -1, -1):
        if (trace_data[day][pid1] == trace_data[day][pid2]) & \
            (trace_data[day][pid1] != "0"):
            assumed_trans_date = day
            break
    sc_recip = first_pos2 - assumed_trans_date

    if first_pos1 < assumed_trans_date:
        sc_donor = 0
    else:
        sc_donor = first_pos1 - assumed_trans_date
    return sc_donor + sc_recip



def compute_pairwise_epi_distances(trace_data, patient_ids):
    """
        Turns the patient trace data into a dictionary of pairwise 
        epidemiological distances.
        
        Arguments:
        trace_data -- a list of strings with patient trace data
        patient_ids -- ordered list of patient IDs to expect
        
        Returns:
        A dictionary of dictionaries where edist[i][j] is the
        epidemiological distance between i and j.
        """
    edist = {}
    proc_data = []
    # Reformat the trace data
    for i in range(len(trace_data)):
        temp = trace_data[i].split()[::-1]
        proc_data.append(temp)
    # Find first positive test days and remove the indication from the data
    first_pos = find_first_positives(proc_data)
    for pid in first_pos:
        day = first_pos[pid]
        proc_data[day][pid - 1] = proc_data[day][pid - 1].replace(".5", "")
    # Find the epidemiological distance between the two patients and add it
    # to the graph
    for pid1 in patient_ids:
        edist[pid1] = {}
        for pid2 in patient_ids:
            if pid1 != pid2:
                epi_dist = compute_epi_distance(pid1, pid2, proc_data,
                                                first_pos[pid1], first_pos[pid2], patient_ids)
                edist[pid1][pid2] = epi_dist
    return edist

# ---------------
# ANALYSIS FXNS
def compute_genetic_distance(seq1, seq2):

    """
    Computes the genetic distance between two sequences as the number of
    differences between the two sequences.
    
    inputs--
        seq1: the first sequence
        seq2: the second sequence
    
    outputs--
        distance: hamming distance between the two sequences
    """
    distance = 0
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            distance += 1
    return distance

# testing compute_genetic_distance
# seq1 = "01000000000000000000000000000000000001011"
# seq2 = "10000000000000000000000001000000000110000"
# print(compute_genetic_distance(seq1, seq2)) # should be 8

# seq3 = "01000000000000100000000000000000000001011"
# seq4 = "10000000000000100000000001000000011110000"
# print(f"Genetic distance between seq3 and seq4: {compute_genetic_distance(seq3, seq4)}") # should = 10

def construct_complete_weighted_digraph(gen_data, epi_data):
    """
    The function constructs a complete weighted digraph where the vertices are the patients
    and the weight of an edge from patient A to patient B is the genetic distance between A and B
    plus a small fraction of the epidemiological distance between A and B. 

    inputs--
        gen_data: filename with genetic data for each patient
        epi_data: filename with epidemiological data for each patient

    outputs--
        wdgraph: a complete weighted digraph represented as a dict of dicts, 
        where outer key is source node and inner dict contains destination: weight entries    
    """
    wdgraph = defaultdict(dict)

    epi_dist = read_patient_traces(epi_data)
    # returns dict of dicts where epi_dist[pa][pb] is the epidemiological distance between pa and pb

    gen_dist = compute_pairwise_gen_distances(read_patient_sequences(gen_data), compute_genetic_distance)
    # returns dict of dicts where gen_dist[pa][pb] is the genetic distance between pa and pb

    max_e = 0
    for pa in epi_dist:
        for pb in epi_dist[pa]:
            if pa != pb and epi_dist[pa][pb] > max_e:
                max_e = epi_dist[pa][pb]


    for pa in epi_dist:
        for pb in epi_dist[pa]:
            if pa != pb:
                wdgraph[pa][pb] = gen_dist[pa][pb] + ((999 * epi_dist[pa][pb]/ max_e)/(10**5))

    print(f"complete weighted digraph is {dict(wdgraph)}")
    return wdgraph

# testing construct_complete_weighted_digraph
# gen_data = "test_sequence1.txt"
# epi_data = "sample_trace1.txt"
# print(construct_complete_weighted_digraph(gen_data, epi_data))

# gen_data = "test_sequence2.txt"
# epi_data = "sample_trace2.txt"
# print(construct_complete_weighted_digraph(gen_data, epi_data))

ans = infer_transmap("patient_sequences.txt", "patient_traces.txt", 1)
print(ans)
render_graph(ans[0], "transmission_map.png")
