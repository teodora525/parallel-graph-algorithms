import csv
import os
import matplotlib.pyplot as plt


def load_csv(path: str):
    rows = []
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "n": int(r["n"]),
                "bfs_time": float(r["bfs_time"]),
                "components_time": float(r["components_time"]),
            })
    rows.sort(key=lambda x: x["n"])
    return rows


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def plot_line(xs, ys, title, xlabel, ylabel, out_path):
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    csv_path = os.path.join("..", "results", "python_seq.csv")
    out_dir = os.path.join("..", "results")
    ensure_dir(out_dir)

    rows = load_csv(csv_path)
    ns = [r["n"] for r in rows]

    bfs_times = [r["bfs_time"] for r in rows]
    comp_times = [r["components_time"] for r in rows]

    plot_line(
        ns, bfs_times,
        title="Python (Sequential) - BFS runtime",
        xlabel="Number of nodes (n)",
        ylabel="Time (s)",
        out_path=os.path.join(out_dir, "python_seq_bfs.png")
    )

    plot_line(
        ns, comp_times,
        title="Python (Sequential) - Connected components runtime",
        xlabel="Number of nodes (n)",
        ylabel="Time (s)",
        out_path=os.path.join(out_dir, "python_seq_components.png")
    )

    print("Saved plots to results/: python_seq_bfs.png, python_seq_components.png")
