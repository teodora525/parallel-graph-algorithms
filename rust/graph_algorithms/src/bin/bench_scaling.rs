use std::time::{Duration, Instant};
use std::io::Write;
use graph_algorithms::graph::generate_random_graph;
use graph_algorithms::bfs::bfs;
use graph_algorithms::bfs_parallel::bfs_parallel;

fn measure_runs(f: impl Fn() -> (), runs: u32) -> Vec<f64> {
    let mut times = Vec::new();
    for _ in 0..runs {
        let t = Instant::now();
        f();
        times.push(t.elapsed().as_secs_f64());
    }
    times
}

fn mean(v: &[f64]) -> f64 {
    v.iter().sum::<f64>() / v.len() as f64
}

fn stdev(v: &[f64]) -> f64 {
    let m = mean(v);
    let var = v.iter().map(|x| (x - m).powi(2)).sum::<f64>() / (v.len() - 1) as f64;
    var.sqrt()
}

fn main() {
    let runs = 30u32;

    // ── Jako skaliranje ───────────────────────────────────────────────────
    println!("=== Jako skaliranje (Rust) ===");
    let n_strong = 20_000;
    let p = 0.001;
    let g_strong = generate_random_graph(n_strong, p);
    let thread_counts = [1usize, 2, 4, 8];

    let mut strong_rows: Vec<(usize, f64, f64)> = Vec::new();

    for &t in &thread_counts {
        let times = if t == 1 {
            measure_runs(|| { bfs(&g_strong, 0); }, runs)
        } else {
            rayon::ThreadPoolBuilder::new().num_threads(t).build_global().ok();
            measure_runs(|| { bfs_parallel(&g_strong, 0, t); }, runs)
        };
        let m = mean(&times);
        let s = stdev(&times);
        println!("threads={t} | mean={m:.6}s | stdev={s:.6}s");
        strong_rows.push((t, m, s));
    }

    // ── Slabo skaliranje ──────────────────────────────────────────────────
    println!("\n=== Slabo skaliranje (Rust) ===");
    let base_n = 5_000;
    let mut weak_rows: Vec<(usize, usize, f64, f64)> = Vec::new();

    for &t in &thread_counts {
        let n = base_n * t;
        let g = generate_random_graph(n, p);

        let times = if t == 1 {
            measure_runs(|| { bfs(&g, 0); }, runs)
        } else {
            measure_runs(|| { bfs_parallel(&g, 0, t); }, runs)
        };
        let m = mean(&times);
        let s = stdev(&times);
        println!("threads={t} | n={n} | mean={m:.6}s | stdev={s:.6}s");
        weak_rows.push((t, n, m, s));
    }

    // ── Snimi CSV ─────────────────────────────────────────────────────────
    let mut f = std::fs::File::create("../../results/rust_strong_scaling.csv").unwrap();
    writeln!(f, "threads,mean,stdev").unwrap();
    for (t, m, s) in &strong_rows {
        writeln!(f, "{t},{m:.8},{s:.8}").unwrap();
    }

    let mut f = std::fs::File::create("../../results/rust_weak_scaling.csv").unwrap();
    writeln!(f, "threads,n,mean,stdev").unwrap();
    for (t, n, m, s) in &weak_rows {
        writeln!(f, "{t},{n},{m:.8},{s:.8}").unwrap();
    }

    println!("\nSnimljeno u results/");
}