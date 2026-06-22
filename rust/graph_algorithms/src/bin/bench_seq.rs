use std::time::{Duration, Instant};
use graph_algorithms::graph::generate_random_graph;
use graph_algorithms::bfs::bfs;
use graph_algorithms::component::connected_components;

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
    let sizes: &[usize] = &[1_000, 2_000, 5_000, 10_000, 50_000, 100_000];
    let p = 0.001;
    let runs = 5u32;

    println!("{:<10} {:>14} {:>18}", "n", "bfs_time (ms)", "components_time (ms)");
    println!("{}", "-".repeat(44));

    let mut csv_lines = vec!["n,bfs_time,components_time".to_string()];

    for &n in sizes {
        let g = generate_random_graph(n, p);

        let bfs_time = measure(|| { bfs(&g, 0); }, runs);
        let comp_time = measure(|| { connected_components(&g); }, runs);

        let bfs_ms = bfs_time.as_secs_f64() * 1000.0;
        let comp_ms = comp_time.as_secs_f64() * 1000.0;

        println!("{:<10} {:>14.3} {:>18.3}", n, bfs_ms, comp_ms);
        csv_lines.push(format!("{},{:.6},{:.6}", n, bfs_time.as_secs_f64(), comp_time.as_secs_f64()));
    }

    std::fs::write("../../results/rust_seq.csv", csv_lines.join("\n") + "\n")
        .expect("Ne mogu da sačuvam CSV");
    println!("\nRezultati snimljeni u results/rust_seq.csv");
}