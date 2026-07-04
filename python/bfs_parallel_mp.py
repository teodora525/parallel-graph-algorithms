from __future__ import annotations

from collections import deque
from multiprocessing import Pool, cpu_count
from typing import List, Tuple, Set

from graph import Graph


def _process_frontier(args: Tuple[List[int], List[List[int]]]) -> List[int]:
    """
    Worker funkcija: dobije chunk frontier-a i adjacency list (read-only),
    vrati sve susede tih čvorova (kandidate za sledeći nivo).
    """
    chunk, adj = args
    out = []
    for u in chunk:
        out.extend(adj[u])
    return out


def bfs_parallel_mp(graph: Graph, start: int, workers: int | None = None) -> List[int]:
    """
    Level-synchronous BFS preko multiprocessing.
    Vraća distance listu kao i sekvencijalni BFS.

    Napomena: Ovo je "edukativna" paralelizacija – radi, ali nije maksimalno brza,
    jer multiprocessing ima overhead. Ipak je super za NTP poređenja.
    """
    n = graph.n
    if start < 0 or start >= n:
        raise ValueError("Invalid start node")

    if workers is None:
        workers = max(1, cpu_count() - 1)

    dist = [-1] * n
    dist[start] = 0

    frontier = [start]
    level = 0

    # adjacency list prosleđujemo workerima kao plain listu
    adj = graph.adj  # read-only

    with Pool(processes=workers) as pool:
        while frontier:
            # podeli frontier u chunkove
            k = max(1, len(frontier) // (workers * 4))
            chunks = [frontier[i:i + k] for i in range(0, len(frontier), k)]

            # svaki worker vrati listu kandidata (suseda)
            candidates_lists = pool.map(_process_frontier, [(c, adj) for c in chunks])

            # spojimo u jedan veliki niz kandidata
            candidates = []
            for lst in candidates_lists:
                candidates.extend(lst)

            # filtriramo i pravimo next_frontier (bez duplikata)
            next_frontier: List[int] = []
            next_set: Set[int] = set()

            for v in candidates:
                if dist[v] == -1:  # nije posećen
                    dist[v] = level + 1
                    if v not in next_set:
                        next_set.add(v)
                        next_frontier.append(v)

            frontier = next_frontier
            level += 1

    return dist


if __name__ == "__main__":
    # Mali test
    g = Graph(6)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(3, 4)

    print("Parallel BFS distances from 0:")
    print(bfs_parallel_mp(g, 0, workers=2))
