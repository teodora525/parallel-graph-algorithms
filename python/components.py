from typing import List

from graph import Graph
from bfs import bfs_reachable_nodes


def connected_components(graph: Graph) -> List[List[int]]:
    """
    Pronalazi sve povezane komponente u neusmerenom grafu.

    Vraća listu komponenti, gde je svaka komponenta lista čvorova.
    """
    n = graph.n
    visited = [False] * n
    components: List[List[int]] = []

    for start in range(n):
        if not visited[start]:
            comp = bfs_reachable_nodes(graph, start, visited)
            # comp je lista čvorova u jednoj komponenti
            components.append(comp)

    return components


if __name__ == "__main__":
    # Mali test
    g = Graph(6)
    # komponenta 1: 0-1-2
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    # komponenta 2: 3-4
    g.add_edge(3, 4)
    # čvor 5 je izolovan (treća komponenta)

    print("Graf:")
    print(g)

    comps = connected_components(g)
    print("\nPovezane komponente:")
    print(comps)
