import random
from typing import List


class Graph:
    """
    Jednostavan neusmeren graf predstavljen listom suseda.
    Čvorovi su označeni brojevima 0, 1, 2, ..., n-1.
    """

    def __init__(self, n: int):

        self.n = n
        self.adj: List[List[int]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int):
        """
        Dodaje neusmerenu ivicu između čvorova u i v.
        Podrazumevamo da su u i v u opsegu [0, n-1].
        """
        if u < 0 or u >= self.n or v < 0 or v >= self.n:
            raise ValueError(f"Neispravni čvorovi: {u}, {v}")

        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)

    def neighbors(self, u: int) -> List[int]:
        """
        Vraća listu suseda čvora u.
        """
        if u < 0 or u >= self.n:
            raise ValueError(f"Neispravan čvor: {u}")
        return self.adj[u]

    def __repr__(self) -> str:
        """
        Lep ispis grafa za male primere.
        """
        lines = [f"Graph with {self.n} nodes:"]
        for u in range(self.n):
            lines.append(f"{u}: {self.adj[u]}")
        return "\n".join(lines)


def generate_random_graph(n: int, p: float) -> Graph:

    if not (0.0 <= p <= 1.0):
        raise ValueError("p mora biti između 0 i 1")

    g = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                g.add_edge(u, v)

    return g


if __name__ == "__main__":
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(3, 4)

    print("Ručni graf:")
    print(g)

    print("\nRandom graf (n=5, p=0.4):")
    rg = generate_random_graph(5, 0.4)
    print(rg)
