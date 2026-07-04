use crate::graph::Graph;
use crate::bfs::bfs_reachable_nodes;

/// Pronalazi sve povezane komponente u neusmerenom grafu.
/// Vraća listu komponenti, gde je svaka komponenta lista čvorova.
pub fn connected_components(graph: &Graph) -> Vec<Vec<usize>> {
    let mut visited = vec![false; graph.n];
    let mut components = Vec::new();

    for start in 0..graph.n {
        if !visited[start] {
            let comp = bfs_reachable_nodes(graph, start, &mut visited);
            components.push(comp);
        }
    }

    components
}
