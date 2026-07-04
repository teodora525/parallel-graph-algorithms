use graph_algorithms::graph::{Graph, generate_random_graph};
use graph_algorithms::bfs::bfs;
use graph_algorithms::component::connected_components;

fn main() {
    let mut g = Graph::new(6);
    g.add_edge(0, 1);
    g.add_edge(1, 2);
    g.add_edge(3, 4);

    println!("=== Mali primer ===");
    println!("{:#?}", g);

    let distances = bfs(&g, 0);
    println!("\nBFS distance od čvora 0: {:?}", distances);

    let components = connected_components(&g);
    println!("\nPovezane komponente: {:?}", components);

    println!("\n=== Random graf (n=1000, p=0.005) ===");
    let rg = generate_random_graph(1000, 0.005);
    let rg_components = connected_components(&rg);
    println!("Broj komponenti: {}", rg_components.len());
    println!(
        "Najveća komponenta: {} čvorova",
        rg_components.iter().map(|c| c.len()).max().unwrap_or(0)
    );
}