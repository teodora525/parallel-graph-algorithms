import time
import csv

from graph import generate_random_graph
from bfs import bfs
from bfs_parallel_mp import bfs_parallel_mp


def avg_time(fn, runs=5):
    ts = []
    for _ in range(runs):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        ts.append(t1 - t0)
    return sum(ts) / len(ts)


def run():
    sizes = [2_000, 5_000, 10_000, 20_000]
    p = 0.001
    workers_list = [2, 4]  # kasnije možeš dodati 8 ako imaš CPU

    rows = []

    for n in sizes:
        print(f"\n--- n={n} ---")
        g = generate_random_graph(n, p)

        seq = avg_time(lambda: bfs(g, 0))
        print(f"seq bfs: {seq:.4f}s")

        for w in workers_list:
            par = avg_time(lambda: bfs_parallel_mp(g, 0, workers=w))
            print(f"mp bfs (workers={w}): {par:.4f}s")
            rows.append({"n": n, "workers": w, "seq_bfs": seq, "mp_bfs": par})

    return rows


def save(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["n", "workers", "seq_bfs", "mp_bfs"])
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    rows = run()
    save(rows, "../results/python_mp_bfs.csv")
    print("Saved to results/python_mp_bfs.csv")
