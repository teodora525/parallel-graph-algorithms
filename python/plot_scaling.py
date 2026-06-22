import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# ── podaci ───────────────────────────────────────────────────────────────────
# Python strong scaling — iz CSV
py_strong = pd.DataFrame({
    "workers": [1, 2, 4, 8],
    "mean":    [0.004756, 0.346846, 0.695850, 1.377423],
    "stdev":   [0.000460, 0.027705, 0.161089, 0.090710],
})

# Python weak scaling (workers=8 nije izmereno — process killed)
py_weak = pd.DataFrame({
    "workers": [1, 2, 4],
    "n":       [5000, 10000, 20000],
    "mean":    [0.0029, 0.8752, 2.4833],
    "stdev":   [0.0004, 0.1008, 0.2698],
})

# Rust strong scaling
rs_strong = pd.DataFrame({
    "workers": [1, 2, 4, 8],
    "mean":    [0.004030, 0.047814, 0.040523, 0.040299],
    "stdev":   [0.001023, 0.006260, 0.002989, 0.004823],
})

# Rust weak scaling
rs_weak = pd.DataFrame({
    "workers": [1, 2, 4, 8],
    "n":       [5000, 10000, 20000, 40000],
    "mean":    [0.000308, 0.015381, 0.034783, 0.090026],
    "stdev":   [0.000093, 0.001407, 0.004119, 0.010485],
})

# ── Amdahl — teorijski maksimum ───────────────────────────────────────────────
# f = sekvencijalni deo (procenjeno iz merenja)
# Za Python: seq=0.0048s, par@2=0.3468s → overhead dominira, f≈1 (skoro sve seq)
# Za Rust:   seq=0.004030s, par@2=0.047814s → slično
# Koristimo f=0.95 (95% sekvencijalno) — konzervativna procena za BFS
def amdahl_speedup(p_parallel, n_cores):
    f = 1 - p_parallel
    return 1 / (f + p_parallel / n_cores)

# Za Gustafson: efficiency = T_seq(1) / T_par(p) * p
def gustafson_speedup(p_parallel, n_cores):
    return n_cores - (1 - p_parallel) * (n_cores - 1)

cores = np.array([1, 2, 4, 8])
f_parallel = 0.05  # samo 5% paralelizabilno (BFS je inherentno sekvencijalan)
ideal_speedup = cores  # linearno ubrzanje

amdahl = amdahl_speedup(f_parallel, cores)
gustafson = gustafson_speedup(f_parallel, cores)

# ── stil ──────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.facecolor": "white",
})

C_PY  = "#4C72B0"
C_RS  = "#DD8452"
C_TH  = "#888888"
C_AM  = "#C44E52"

fig = plt.figure(figsize=(16, 14))
fig.suptitle("Jako i slabo skaliranje — Python vs Rust", fontsize=16, fontweight="bold", y=0.98)
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# ── Plot 1: Jako skaliranje Python (Amdahl) ───────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
seq_py = py_strong[py_strong["workers"] == 1]["mean"].values[0]
py_speedup_strong = seq_py / py_strong["mean"].values

ax1.plot(cores, ideal_speedup, "--", color=C_TH, linewidth=1.5, label="Idealno (linearno)")
ax1.plot(cores, amdahl, "-.", color=C_AM, linewidth=1.5, label=f"Amdahl (p={f_parallel:.0%})")
ax1.errorbar(cores, py_speedup_strong,
             yerr=py_strong["stdev"].values / py_strong["mean"].values,
             fmt="o-", color=C_PY, linewidth=2, markersize=6, capsize=4,
             label="Python mp (izmereno)")
ax1.set_title("Jako skaliranje — Python (Amdahl)", fontsize=11)
ax1.set_xlabel("Broj jezgara")
ax1.set_ylabel("Ubrzanje (speedup)")
ax1.set_xticks(cores)
ax1.set_ylim(bottom=0)
ax1.legend(fontsize=9)

# ── Plot 2: Jako skaliranje Rust (Amdahl) ────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
seq_rs = rs_strong[rs_strong["workers"] == 1]["mean"].values[0]
rs_speedup_strong = seq_rs / rs_strong["mean"].values

ax2.plot(cores, ideal_speedup, "--", color=C_TH, linewidth=1.5, label="Idealno (linearno)")
ax2.plot(cores, amdahl, "-.", color=C_AM, linewidth=1.5, label=f"Amdahl (p={f_parallel:.0%})")
ax2.errorbar(cores, rs_speedup_strong,
             yerr=rs_strong["stdev"].values / rs_strong["mean"].values,
             fmt="s-", color=C_RS, linewidth=2, markersize=6, capsize=4,
             label="Rust rayon (izmereno)")
ax2.set_title("Jako skaliranje — Rust (Amdahl)", fontsize=11)
ax2.set_xlabel("Broj jezgara")
ax2.set_ylabel("Ubrzanje (speedup)")
ax2.set_xticks(cores)
ax2.set_ylim(bottom=0)
ax2.legend(fontsize=9)

# ── Plot 3: Slabo skaliranje Python (Gustafson) ───────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
# efficiency = T(1)/T(p) — idealno bi trebalo da ostane 1.0
cores_py_weak = py_weak["workers"].values
seq_weak_py = py_weak[py_weak["workers"] == 1]["mean"].values[0]
py_efficiency = seq_weak_py / py_weak["mean"].values

ax3.axhline(1.0, linestyle="--", color=C_TH, linewidth=1.5, label="Idealno (efficiency=1)")
ax3.plot(cores[:3], (gustafson / gustafson[0] / cores)[:3],
         "-.", color=C_AM, linewidth=1.5, label=f"Gustafson (p={f_parallel:.0%})")
ax3.errorbar(cores_py_weak, py_efficiency,
             yerr=py_weak["stdev"].values / py_weak["mean"].values,
             fmt="o-", color=C_PY, linewidth=2, markersize=6, capsize=4,
             label="Python mp (izmereno, workers=1-4)")
ax3.set_title("Slabo skaliranje — Python (Gustafson)", fontsize=11)
ax3.set_xlabel("Broj jezgara")
ax3.set_ylabel("Efikasnost (efficiency)")
ax3.set_xticks(cores_py_weak)
ax3.set_ylim(bottom=0)
ax3.legend(fontsize=9)

# ── Plot 4: Slabo skaliranje Rust (Gustafson) ─────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
seq_weak_rs = rs_weak[rs_weak["workers"] == 1]["mean"].values[0]
rs_efficiency = seq_weak_rs / rs_weak["mean"].values

ax4.axhline(1.0, linestyle="--", color=C_TH, linewidth=1.5, label="Idealno (efficiency=1)")
ax4.plot(cores[:len(gustafson)], gustafson / gustafson[0] / cores,
         "-.", color=C_AM, linewidth=1.5, label=f"Gustafson (p={f_parallel:.0%})")
ax4.errorbar(cores, rs_efficiency,
             yerr=rs_weak["stdev"].values / rs_weak["mean"].values,
             fmt="s-", color=C_RS, linewidth=2, markersize=6, capsize=4,
             label="Rust rayon (izmereno)")
ax4.set_title("Slabo skaliranje — Rust (Gustafson)", fontsize=11)
ax4.set_xlabel("Broj jezgara")
ax4.set_ylabel("Efikasnost (efficiency)")
ax4.set_xticks(cores)
ax4.set_ylim(bottom=0)
ax4.legend(fontsize=9)

plt.savefig("results/scaling_all.png", dpi=180, bbox_inches="tight")
print("Snimljeno: results/scaling_all.png")
plt.close()

# ── Potporne tabele ───────────────────────────────────────────────────────────
print("\n=== Jako skaliranje — Python ===")
print(f"{'Workers':>8} {'Mean (s)':>12} {'Stdev (s)':>12} {'Speedup':>10}")
print("-" * 46)
for _, row in py_strong.iterrows():
    sp = seq_py / row["mean"]
    print(f"{int(row['workers']):>8} {row['mean']:>12.4f} {row['stdev']:>12.4f} {sp:>10.3f}")

print("\n=== Jako skaliranje — Rust ===")
print(f"{'Workers':>8} {'Mean (s)':>12} {'Stdev (s)':>12} {'Speedup':>10}")
print("-" * 46)
for _, row in rs_strong.iterrows():
    sp = seq_rs / row["mean"]
    print(f"{int(row['workers']):>8} {row['mean']:>12.6f} {row['stdev']:>12.6f} {sp:>10.3f}")

print("\n=== Slabo skaliranje — Rust ===")
print(f"{'Workers':>8} {'n':>8} {'Mean (s)':>12} {'Stdev (s)':>12} {'Efficiency':>12}")
print("-" * 56)
for _, row in rs_weak.iterrows():
    eff = seq_weak_rs / row["mean"]
    print(f"{int(row['workers']):>8} {int(row['n']):>8} {row['mean']:>12.6f} {row['stdev']:>12.6f} {eff:>12.4f}")