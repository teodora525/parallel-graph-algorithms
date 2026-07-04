import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt


def load_csv(path: str):
    rows = []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "n": int(r["n"]),
                "workers": int(r["workers"]),
                "seq_bfs": float(r["seq_bfs"]),
                "mp_bfs": float(r["mp_bfs"]),
            })
    return rows


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def plot_runtime(rows, out_path):
    by_workers = defaultdict(list)

    for r in rows:
        by_workers[r["workers"]].append(r)

    plt.figure()

    # Sekvencijalno vreme je isto za svaki workers red, pa uzimamo jednu vrednost po n
    seq_by_n = {}
    for r in rows:
        seq_by_n[r["n"]] = r["seq_bfs"]

    ns = sorted(seq_by_n.keys())
    seq_times = [seq_by_n[n] for n in ns]

    plt.plot(ns, seq_times, marker="o", label="Sequential BFS")

    for workers, items in sorted(by_workers.items()):
        items.sort(key=lambda x: x["n"])
        x = [r["n"] for r in items]
        y = [r["mp_bfs"] for r in items]
        plt.plot(x, y, marker="o", label=f"Multiprocessing BFS ({workers} workers)")

    plt.title("Python BFS runtime: sequential vs multiprocessing")
    plt.xlabel("Number of nodes (n)")
    plt.ylabel("Time (s)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_speedup(rows, out_path):
    by_workers = defaultdict(list)

    for r in rows:
        by_workers[r["workers"]].append(r)

    plt.figure()

    for workers, items in sorted(by_workers.items()):
        items.sort(key=lambda x: x["n"])
        x = [r["n"] for r in items]
        y = [r["seq_bfs"] / r["mp_bfs"] if r["mp_bfs"] > 0 else 0 for r in items]
        plt.plot(x, y, marker="o", label=f"{workers} workers")

    plt.axhline(y=1.0, linestyle="--", label="No speedup")
    plt.title("Python multiprocessing BFS speedup")
    plt.xlabel("Number of nodes (n)")
    plt.ylabel("Speedup = sequential time / parallel time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    csv_path = os.path.join("..", "results", "python_mp_bfs.csv")
    out_dir = os.path.join("..", "results")
    ensure_dir(out_dir)

    rows = load_csv(csv_path)

    plot_runtime(
        rows,
        os.path.join(out_dir, "python_mp_bfs_runtime.png")
    )

    plot_speedup(
        rows,
        os.path.join(out_dir, "python_mp_bfs_speedup.png")
    )

    print("Saved plots:")
    print("- results/python_mp_bfs_runtime.png")
    print("- results/python_mp_bfs_speedup.png")