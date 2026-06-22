use rayon::prelude::*;
use crate::graph::Graph;

pub fn bfs_parallel(graph: &Graph, start: usize, _threads: usize) -> Vec<i32> {
    assert!(start < graph.n, "Invalid start node: {}", start);

    let mut dist = vec![-1i32; graph.n];
    dist[start] = 0;

    let mut frontier = vec![start];
    let mut level = 0i32;

    while !frontier.is_empty() {
        // Paralelno skupljamo sve susede trenutnog frontiera
        let candidates: Vec<usize> = frontier
            .par_iter()
            .flat_map(|&u| graph.adj[u].par_iter().copied())
            .collect();

        let mut next_frontier: Vec<usize> = Vec::new();

        for v in candidates {
            if dist[v] == -1 {
                dist[v] = level + 1;
                next_frontier.push(v);
            }
        }

        // Ukloni duplikate
        next_frontier.dedup();
        frontier = next_frontier;
        level += 1;
    }

    dist
}