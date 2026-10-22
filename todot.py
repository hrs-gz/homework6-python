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


