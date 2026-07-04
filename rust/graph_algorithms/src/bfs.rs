use std::collections::VecDeque;
use crate::graph::Graph;

/// Klasičan sekvencijalni BFS.
/// Vraća vektor distanci od `start` čvora do svih ostalih.
/// Nedostupni čvorovi dobijaju vrednost -1.
pub fn bfs(graph: &Graph, start: usize) -> Vec<i32> {
    assert!(start < graph.n, "Invalid start node: {}", start);

    let mut distance = vec![-1i32; graph.n];
    let mut queue = VecDeque::new();

    distance[start] = 0;
    queue.push_back(start);

    while let Some(u) = queue.pop_front() {
        for &v in graph.neighbors(u) {
            if distance[v] == -1 {
                distance[v] = distance[u] + 1;
                queue.push_back(v);
            }
        }
    }

    distance
}

/// BFS koji vraća sve čvorove dostupne iz `start` (jedna komponenta).
/// `visited` je zajednički niz koji se ažurira in-place.
pub fn bfs_reachable_nodes(
    graph: &Graph,
    start: usize,
    visited: &mut Vec<bool>,
) -> Vec<usize> {
    if visited[start] {
        return Vec::new();
    }

    let mut queue = VecDeque::new();
    let mut component = Vec::new();

    visited[start] = true;
    queue.push_back(start);
    component.push(start);

    while let Some(u) = queue.pop_front() {
        for &v in graph.neighbors(u) {
            if !visited[v] {
                visited[v] = true;
                queue.push_back(v);
                component.push(v);
            }
        }
    }

    component
}
