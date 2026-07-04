from collections import deque
from typing import List

from graph import Graph


def bfs(graph: Graph, start: int) -> List[int]:
    """
    Klasičan BFS (Breadth-First Search) nad neusmerenim grafom.
    Vraća listu distanci od start čvora do svih ostalih čvorova.

    Ako do nekog čvora ne može da se dođe iz start,
    njegova distanca će biti -1.
    """
    n = graph.n

    if start < 0 or start >= n:
        raise ValueError(f"Neispravan start čvor: {start}")

    # distance[i] = rastojanje od start do i
    # -1 znači da čvor nije posećen / nedostupan
    distance: List[int] = [-1] * n

    # queue za BFS (fifo)
    q = deque()

    # startni čvor: rastojanje 0
    distance[start] = 0
    q.append(start)

    # Klasična BFS petlja
    while q:
        u = q.popleft()  

        for v in graph.neighbors(u):
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                q.append(v)

    return distance

def bfs_reachable_nodes(graph: Graph, start: int, visited: List[bool]) -> List[int]:
    """
    BFS koji pronalazi sve čvorove dostupne iz start čvora
    (tj. jednu povezanu komponentu).

    visited je zajednički niz za ceo algoritam komponenti.
    """
    if visited[start]:
        return []

    q = deque()
    q.append(start)

    visited[start] = True
    component = [start]

    while q:
        u = q.popleft()
        for v in graph.neighbors(u):
            if not visited[v]:
                visited[v] = True
                q.append(v)
                component.append(v)

    return component

if __name__ == "__main__":
    from graph import Graph

    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(3, 4)

    print("Graf:")
    print(g)

    print("\nBFS od čvora 0:")
    dist = bfs(g, 0)
    print("distance =", dist)

    print("\nBFS od čvora 3:")
    dist2 = bfs(g, 3)
    print("distance =", dist2)
