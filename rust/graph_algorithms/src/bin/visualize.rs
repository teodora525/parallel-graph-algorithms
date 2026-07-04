use plotters::prelude::*;
use graph_algorithms::graph::generate_random_graph;
use graph_algorithms::bfs::bfs;
use graph_algorithms::component::connected_components;

fn main() {
    let n = 500;
    let p = 0.008;
    let g = generate_random_graph(n, p);

    // ── Plot 1: BFS distance heatmap ─────────────────────────────────────
    {
        let dist = bfs(&g, 0);
        let max_dist = *dist.iter().filter(|&&d| d >= 0).max().unwrap_or(&1) as f64;

        let root = BitMapBackend::new("../../results/rust_bfs_distances.png", (800, 600))
            .into_drawing_area();
        root.fill(&WHITE).unwrap();

        let mut chart = ChartBuilder::on(&root)
            .caption("BFS Distance od čvora 0 (Rust)", ("sans-serif", 24))
            .margin(20)
            .x_label_area_size(40)
            .y_label_area_size(40)
            .build_cartesian_2d(0usize..n, -1i32..(max_dist as i32 + 1))
            .unwrap();

        chart.configure_mesh()
            .x_desc("Čvor")
            .y_desc("Distanca")
            .draw()
            .unwrap();

        // Tačke obojene po distanci
        chart.draw_series(
            dist.iter().enumerate().filter(|(_, &d)| d >= 0).map(|(i, &d)| {
                let ratio = d as f64 / max_dist;
                let r = (255.0 * ratio) as u8;
                let b = (255.0 * (1.0 - ratio)) as u8;
                Circle::new((i, d), 2, RGBColor(r, 50, b).filled())
            })
        ).unwrap();

        // Nedostupni čvorovi
        chart.draw_series(
            dist.iter().enumerate().filter(|(_, &d)| d == -1).map(|(i, _)| {
                Circle::new((i, 0), 2, RGBColor(200, 200, 200).filled())
            })
        ).unwrap();

        root.present().unwrap();
        println!("Snimljeno: results/rust_bfs_distances.png");
    }

    // ── Plot 2: Komponente — bar chart ───────────────────────────────────
    {
        let components = connected_components(&g);
        let mut comp_sizes: Vec<usize> = components.iter().map(|c| c.len()).collect();
        comp_sizes.sort_unstable_by(|a, b| b.cmp(a));
        let top = comp_sizes.iter().take(15).cloned().collect::<Vec<_>>();
        let max_size = *top.iter().max().unwrap_or(&1);

        let root = BitMapBackend::new("../../results/rust_components.png", (800, 500))
            .into_drawing_area();
        root.fill(&WHITE).unwrap();

        let mut chart = ChartBuilder::on(&root)
            .caption(
                format!("Povezane komponente (Rust) — ukupno: {}", components.len()),
                ("sans-serif", 22),
            )
            .margin(20)
            .x_label_area_size(40)
            .y_label_area_size(50)
            .build_cartesian_2d(0usize..top.len(), 0usize..max_size + 10)
            .unwrap();

        chart.configure_mesh()
            .x_desc("Komponenta (sortirano po veličini)")
            .y_desc("Broj čvorova")
            .draw()
            .unwrap();

        chart.draw_series(
            top.iter().enumerate().map(|(i, &size)| {
                let color = RGBColor(
                    (80 + i * 12) as u8,
                    (120 + i * 8) as u8,
                    200u8.saturating_sub(i as u8 * 10),
                );
                Rectangle::new([(i, 0), (i + 1, size)], color.filled())
            })
        ).unwrap();

        root.present().unwrap();
        println!("Snimljeno: results/rust_components.png");
    }

    // ── Plot 3: Scaling rezultati iz CSV ─────────────────────────────────
    {
        // Strong scaling
        let threads = [1usize, 2, 4, 8];
        let means =   [0.004030f64, 0.047814, 0.040523, 0.040299];
        let speedups: Vec<f64> = means.iter().map(|&m| means[0] / m).collect();

        let root = BitMapBackend::new("../../results/rust_strong_scaling.png", (700, 500))
            .into_drawing_area();
        root.fill(&WHITE).unwrap();

        let mut chart = ChartBuilder::on(&root)
            .caption("Jako skaliranje — Rust BFS", ("sans-serif", 22))
            .margin(20)
            .x_label_area_size(40)
            .y_label_area_size(50)
            .build_cartesian_2d(0usize..9, 0f64..2.0)
            .unwrap();

        chart.configure_mesh()
            .x_desc("Broj threadova")
            .y_desc("Ubrzanje (speedup)")
            .draw()
            .unwrap();

        // Idealna linija
        chart.draw_series(LineSeries::new(
            vec![(0, 0.0), (1, 1.0), (2, 2.0), (4, 4.0), (8, 8.0)]
                .into_iter()
                .map(|(x, y): (usize, f64)| (x, y.min(2.0))),
            &RGBColor(150, 150, 150),
        )).unwrap()
          .label("Idealno")
          .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RGBColor(150, 150, 150)));

        // Izmereno
        chart.draw_series(LineSeries::new(
            threads.iter().copied().zip(speedups.iter().copied()),
            &RGBColor(221, 132, 82),
        )).unwrap()
          .label("Izmereno")
          .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RGBColor(221, 132, 82)));

        chart.draw_series(
            threads.iter().copied().zip(speedups.iter().copied())
                .map(|(t, s)| Circle::new((t, s), 5, RGBColor(221, 132, 82).filled()))
        ).unwrap();

        chart.configure_series_labels()
            .background_style(&WHITE)
            .border_style(&BLACK)
            .draw()
            .unwrap();

        root.present().unwrap();
        println!("Snimljeno: results/rust_strong_scaling.png");
    }
}