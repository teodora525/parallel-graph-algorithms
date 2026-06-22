import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── podaci ───────────────────────────────────────────────────────────────────
py_seq = pd.read_csv("../results/python_seq.csv")
rs_seq = pd.read_csv("../results/rust_seq.csv")
py_par = pd.read_csv("../results/python_mp_bfs.csv")
rs_par = pd.read_csv("../results/rust_parallel_bfs.csv")

# zajednički n za seq poređenje
common_n = [1000, 2000, 5000, 10000]
py_common = py_seq[py_seq["n"].isin(common_n)].set_index("n")
rs_common = rs_seq[rs_seq["n"].isin(common_n)].set_index("n")

# ── stil ──────────────────────────────────────────────────────────────────────
COLORS = {
    "py_seq":  "#4C72B0",
    "rs_seq":  "#DD8452",
    "py_par2": "#55A868",
    "py_par4": "#C44E52",
    "rs_par2": "#8172B2",
    "rs_par4": "#937860",
    "rs_par8": "#DA8BC3",
}
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.facecolor": "white",
})

fig = plt.figure(figsize=(16, 14))
fig.suptitle("Parallel Graph Algorithms — Python vs Rust", fontsize=16, fontweight="bold", y=0.98)
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.35)

# ── Plot 1: Seq BFS — Python vs Rust ─────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(common_n, py_common["bfs_time"] * 1000, "o-", color=COLORS["py_seq"],
         linewidth=2, markersize=6, label="Python seq")
ax1.plot(common_n, rs_common["bfs_time"] * 1000, "s-", color=COLORS["rs_seq"],
         linewidth=2, markersize=6, label="Rust seq")
ax1.set_title("BFS — sekvencijalno (Python vs Rust)", fontsize=11)
ax1.set_xlabel("Broj čvorova (n)")
ax1.set_ylabel("Vreme (ms)")
ax1.legend()
ax1.set_xticks(common_n)

# ── Plot 2: Seq Components — Python vs Rust ───────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(common_n, py_common["components_time"] * 1000, "o-", color=COLORS["py_seq"],
         linewidth=2, markersize=6, label="Python seq")
ax2.plot(common_n, rs_common["components_time"] * 1000, "s-", color=COLORS["rs_seq"],
         linewidth=2, markersize=6, label="Rust seq")
ax2.set_title("Komponente — sekvencijalno (Python vs Rust)", fontsize=11)
ax2.set_xlabel("Broj čvorova (n)")
ax2.set_ylabel("Vreme (ms)")
ax2.legend()
ax2.set_xticks(common_n)

# ── Plot 3: Paralelni BFS — Python multiprocessing ───────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
py2 = py_par[py_par["workers"] == 2].set_index("n")
py4 = py_par[py_par["workers"] == 4].set_index("n")
ns_py = sorted(py_par["n"].unique())

ax3.plot(ns_py, [py2.loc[n, "seq_bfs"] * 1000 for n in ns_py], "o-",
         color=COLORS["py_seq"], linewidth=2, markersize=6, label="Python seq")
ax3.plot(ns_py, [py2.loc[n, "mp_bfs"] * 1000 for n in ns_py], "s--",
         color=COLORS["py_par2"], linewidth=2, markersize=6, label="Python mp (2 workers)")
ax3.plot(ns_py, [py4.loc[n, "mp_bfs"] * 1000 for n in ns_py], "^--",
         color=COLORS["py_par4"], linewidth=2, markersize=6, label="Python mp (4 workers)")
ax3.set_title("BFS — Python seq vs multiprocessing", fontsize=11)
ax3.set_xlabel("Broj čvorova (n)")
ax3.set_ylabel("Vreme (ms)")
ax3.legend()
ax3.set_xticks(ns_py)

# ── Plot 4: Paralelni BFS — Rust rayon ───────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
rs2 = rs_par[rs_par["threads"] == 2].set_index("n")
rs4 = rs_par[rs_par["threads"] == 4].set_index("n")
rs8 = rs_par[rs_par["threads"] == 8].set_index("n")
ns_rs = sorted(rs_par["n"].unique())

ax4.plot(ns_rs, [rs2.loc[n, "seq_bfs"] * 1000 for n in ns_rs], "o-",
         color=COLORS["rs_seq"], linewidth=2, markersize=6, label="Rust seq")
ax4.plot(ns_rs, [rs2.loc[n, "par_bfs"] * 1000 for n in ns_rs], "s--",
         color=COLORS["rs_par2"], linewidth=2, markersize=6, label="Rust rayon (2 threads)")
ax4.plot(ns_rs, [rs4.loc[n, "par_bfs"] * 1000 for n in ns_rs], "^--",
         color=COLORS["rs_par4"], linewidth=2, markersize=6, label="Rust rayon (4 threads)")
ax4.plot(ns_rs, [rs8.loc[n, "par_bfs"] * 1000 for n in ns_rs], "D--",
         color=COLORS["rs_par8"], linewidth=2, markersize=6, label="Rust rayon (8 threads)")
ax4.set_title("BFS — Rust seq vs rayon", fontsize=11)
ax4.set_xlabel("Broj čvorova (n)")
ax4.set_ylabel("Vreme (ms)")
ax4.legend()
ax4.set_xticks(ns_rs)
ax4.tick_params(axis='x', rotation=30)

plt.savefig("../results/comparison_all.png", dpi=180, bbox_inches="tight")
print("Snimljeno: results/comparison_all.png")
plt.close()

# ── Plot 5: Rust speedup vs Python ───────────────────────────────────────────
fig2, ax5 = plt.subplots(figsize=(8, 5))
fig2.patch.set_facecolor("white")
speedups_inv = py_common["bfs_time"] / rs_common["bfs_time"]

bars = ax5.bar(range(len(common_n)), speedups_inv, color=COLORS["rs_seq"],
               alpha=0.85, edgecolor="white")
ax5.set_xticks(range(len(common_n)))
ax5.set_xticklabels([f"n={n:,}" for n in common_n])
ax5.set_ylabel("Rust ubrzanje (x puta brži od Pythona)")
ax5.set_title("BFS — koliko puta je Rust brži od Pythona (seq)",
              fontsize=12, fontweight="bold")
ax5.axhline(1, color="gray", linestyle="--", linewidth=1)
for bar, val in zip(bars, speedups_inv):
    ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f"{val:.1f}x", ha="center", va="bottom", fontweight="bold", fontsize=11)
ax5.spines["top"].set_visible(False)
ax5.spines["right"].set_visible(False)
ax5.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("../results/rust_vs_python_speedup.png", dpi=180, bbox_inches="tight")
print("Snimljeno: results/rust_vs_python_speedup.png")
plt.close()