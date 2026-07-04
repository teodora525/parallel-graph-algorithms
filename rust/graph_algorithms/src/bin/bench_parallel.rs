use std::time::{Duration, Instant};
use graph_algorithms::graph::generate_random_graph;
use graph_algorithms::bfs::bfs;
use graph_algorithms::bfs_parallel::bfs_parallel;

fn measure<F: Fn()>(f: F, runs: u32) -> Duration {
    let mut total = Duration::ZERO;
    for _ in 0..runs {
        let t = Instant::now();
        f();
        total += t.elapsed();
    }
    total / runs
}

fn main() {
    let sizes: &[usize] = &[2_000, 5_000, 10_000, 50_000, 100_000];
    let p = 0.001;
    let runs = 5u32;
    let thread_counts = [2, 4, 8];

    println!(
        "{:<10} {:>8} {:>14} {:>16} {:>10}",
        "n", "threads", "seq (ms)", "parallel (ms)", "speedup"
    );
    println!("{}", "-".repeat(62));

    let mut csv_lines = vec!["n,threads,seq_bfs,par_bfs".to_string()];

    for &n in sizes {
            let g = generate_random_graph(n, p);
        let seq_time = measure(|| { bfs(&g, 0); }, runs);
        let seq_ms = seq_time.as_secs_f64() * 1000.0;

        for &t in &thread_counts {
            rayon::ThreadPoolBuilder::new()
                .num_threads(t)
                .build_global()
                .ok(); // ignorišemo grešku ako je već podešeno

            let par_time = measure(|| { bfs_parallel(&g, 0, t); }, runs);
            let par_ms = par_time.as_secs_f64() * 1000.0;
            let speedup = seq_ms / par_ms;

            println!(
                "{:<10} {:>8} {:>14.3} {:>16.3} {:>10.2}",
                n, t, seq_ms, par_ms, speedup
            );

            csv_lines.push(format!(
                "{},{},{:.6},{:.6}",
                n, t,
                seq_time.as_secs_f64(),
                par_time.as_secs_f64()
            ));
        }
        println!();
    }

    std::fs::write("../../results/rust_parallel_bfs.csv", csv_lines.join("\n") + "\n")
        .expect("Ne mogu da sačuvam CSV");
    println!("Rezultati snimljeni u results/rust_parallel_bfs.csv");
}