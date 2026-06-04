use std::collections::VecDeque;

#[derive(Debug)]
struct Graph {
    n: usize,
    adj: Vec<Vec<usize>>,
}

impl Graph {
    fn new(n: usize) -> Self {
        Graph {
            n,
            adj: vec![Vec::new(); n],
        }
    }

    fn add_edge(&mut self, u: usize, v: usize) {
        if u >= self.n || v >= self.n {
            panic!("Invalid node index: {} {}", u, v);
        }

        if !self.adj[u].contains(&v) {
            self.adj[u].push(v);
        }

        if !self.adj[v].contains(&u) {
            self.adj[v].push(u);
        }
    }

    fn neighbors(&self, u: usize) -> &Vec<usize> {
        if u >= self.n {
            panic!("Invalid node index: {}", u);
        }

        &self.adj[u]
    }
}

fn bfs(graph: &Graph, start: usize) -> Vec<i32> {
    if start >= graph.n {
        panic!("Invalid start node: {}", start);
    }

    let mut distance = vec![-1; graph.n];
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

fn bfs_reachable_nodes(graph: &Graph, start: usize, visited: &mut Vec<bool>) -> Vec<usize> {
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

fn connected_components(graph: &Graph) -> Vec<Vec<usize>> {
    let mut visited = vec![false; graph.n];
    let mut components = Vec::new();

    for start in 0..graph.n {
        if !visited[start] {
            let component = bfs_reachable_nodes(graph, start, &mut visited);
            components.push(component);
        }
    }

    components
}

fn main() {
    let mut graph = Graph::new(6);

    graph.add_edge(0, 1);
    graph.add_edge(1, 2);
    graph.add_edge(3, 4);

    println!("Graph:");
    println!("{:#?}", graph);

    let distances = bfs(&graph, 0);
    println!("\nBFS distances from node 0:");
    println!("{:?}", distances);

    let components = connected_components(&graph);
    println!("\nConnected components:");
    println!("{:?}", components);
}