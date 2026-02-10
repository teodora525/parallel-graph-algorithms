import time
import csv

from graph import generate_random_graph
from bfs import bfs
from components import connected_components


def benchmark_bfs(graph, start=0):
    t0 = time.perf_counter()
    bfs(graph, start)
    t1 = time.perf_counter()
    return t1 - t0


def benchmark_components(graph):
    t0 = time.perf_counter()
    connected_components(graph)
    t1 = time.perf_counter()
    return t1 - t0


def run_benchmarks():
    # Različite veličine grafova
    sizes = [1_000, 2_000, 5_000, 10_000]
    p = 0.001  # gustina ivica

    results = []

    for n in sizes:
        print(f"\n--- n = {n} ---")
        g = generate_random_graph(n, p)

        bfs_time = benchmark_bfs(g)
        print(f"BFS time: {bfs_time:.4f} s")

        comp_time = benchmark_components(g)
        print(f"Components time: {comp_time:.4f} s")

        results.append({
            "n": n,
            "bfs_time": bfs_time,
            "components_time": comp_time
        })

    return results


def save_results_csv(results, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["n", "bfs_time", "components_time"]
        )
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    results = run_benchmarks()
    save_results_csv(results, "../results/python_seq.csv")
    print("\nResults saved to results/python_seq.csv")
