import time
import csv
import statistics
from multiprocessing import cpu_count
from graph import generate_random_graph
from bfs import bfs
from bfs_parallel_mp import bfs_parallel_mp

RUNS = 10

def measure_runs(fn, runs=RUNS):
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return times

def strong_scaling():
    """Jako skaliranje — fiksan graf n=20000, menjamo broj workers."""
    n = 10000
    p = 0.001
    workers_list = [1, 2, 4, 8]
    g = generate_random_graph(n, p)

    rows = []
    for w in workers_list:
        if w == 1:
            times = measure_runs(lambda: bfs(g, 0))
        else:
            times = measure_runs(lambda: bfs_parallel_mp(g, 0, workers=w))

        mean = statistics.mean(times)
        stdev = statistics.stdev(times)
        rows.append({
            "workers": w,
            "mean": mean,
            "stdev": stdev,
            "times": times
        })
        print(f"strong | workers={w} | mean={mean:.4f}s | stdev={stdev:.4f}s")

    return rows

def weak_scaling():
    """Slabo skaliranje — n proporcionalno broju workers (base_n * workers)."""
    base_n = 5000
    p = 0.001
    workers_list = [1, 2, 4, 8]

    rows = []
    for w in workers_list:
        n = base_n * w
        g = generate_random_graph(n, p)

        if w == 1:
            times = measure_runs(lambda: bfs(g, 0))
        else:
            times = measure_runs(lambda: bfs_parallel_mp(g, 0, workers=w))

        mean = statistics.mean(times)
        stdev = statistics.stdev(times)
        rows.append({
            "workers": w,
            "n": n,
            "mean": mean,
            "stdev": stdev,
            "times": times
        })
        print(f"weak | workers={w} | n={n} | mean={mean:.4f}s | stdev={stdev:.4f}s")

    return rows

def save_csv(rows, path, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})

if __name__ == "__main__":
    print("=== Jako skaliranje (Python) ===")
    strong = strong_scaling()
    save_csv(strong, "../results/python_strong_scaling.csv",
             ["workers", "mean", "stdev"])

    print("\n=== Slabo skaliranje (Python) ===")
    weak = weak_scaling()
    save_csv(weak, "../results/python_weak_scaling.csv",
             ["workers", "n", "mean", "stdev"])

    print("\nSnimljeno u results/")