use std::collections::HashSet;
use std::sync::{Arc, Mutex};
use rayon::prelude::*;
use crate::graph::Graph;

/// Level-synchronous paralelni BFS koristeći rayon.
/// Analogno Python bfs_parallel_mp — svaki level se procesira paralelno.
/// Vraća distance listu kao i sekvencijalni BFS.
pub fn bfs_parallel(graph: &Graph, start: usize, _threads: usize) -> Vec<i32> {
    assert!(start < graph.n, "Invalid start node: {}", start);

    let dist = Arc::new(Mutex::new(vec![-1i32; graph.n]));
    {
        let mut d = dist.lock().unwrap();
        d[start] = 0;
    }

    let mut frontier = vec![start];
    let mut level = 0i32;

    while !frontier.is_empty() {
        // Paralelno procesiramo sve čvorove u trenutnom frontieru
        let candidates: Vec<usize> = frontier
            .par_iter()
            .flat_map(|&u| graph.adj[u].clone())
            .collect();

        let mut next_frontier: Vec<usize> = Vec::new();
        let mut seen: HashSet<usize> = HashSet::new();
        let mut d = dist.lock().unwrap();

        for v in candidates {
            if d[v] == -1 && seen.insert(v) {
                d[v] = level + 1;
                next_frontier.push(v);
            }
        }

        frontier = next_frontier;
        level += 1;
    }

    Arc::try_unwrap(dist).unwrap().into_inner().unwrap()
}