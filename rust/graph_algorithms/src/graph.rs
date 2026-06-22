use rand::Rng;

/// Jednostavan neusmeren graf predstavljen listom suseda.
/// Čvorovi su označeni brojevima 0..n-1.
#[derive(Debug, Clone)]
pub struct Graph {
    pub n: usize,
    pub adj: Vec<Vec<usize>>,
}

impl Graph {
    pub fn new(n: usize) -> Self {
        Graph {
            n,
            adj: vec![Vec::new(); n],
        }
    }

    pub fn add_edge(&mut self, u: usize, v: usize) {
        assert!(u < self.n && v < self.n, "Invalid node index: {} {}", u, v);
        if !self.adj[u].contains(&v) {
            self.adj[u].push(v);
        }
        if !self.adj[v].contains(&u) {
            self.adj[v].push(u);
        }
    }

    pub fn neighbors(&self, u: usize) -> &Vec<usize> {
        assert!(u < self.n, "Invalid node index: {}", u);
        &self.adj[u]
    }
}

/// Generiše random neusmeren graf sa n čvorova i gustinom ivica p.
/// Svaki par (u, v) dobija ivicu sa verovatnoćom p.
pub fn generate_random_graph(n: usize, p: f64) -> Graph {
    assert!((0.0..=1.0).contains(&p), "p mora biti između 0 i 1");
    let mut rng = rand::thread_rng();
    let mut g = Graph::new(n);
    for u in 0..n {
        for v in (u + 1)..n {
            if rng.gen::<f64>() < p {
                g.adj[u].push(v);
                g.adj[v].push(u);
            }
        }
    }
    g
}
