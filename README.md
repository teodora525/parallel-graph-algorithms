# Parallel Graph Algorithms: BFS and Connected Components in Python and Rust

## Project Description
This project implements and analyzes sequential and parallel algorithms for large undirected graphs, focusing on:
- Breadth-First Search (BFS)
- Finding Connected Components

The project is implemented in both Python and Rust to compare:
- Sequential and parallel implementations
- Performance between programming languages
- Scalability with respect to the number of threads/processes and graph sizes

---

## Functional Requirements

### 1. Graph Representation
- The graph is undirected and represented using an adjacency list.
- Nodes are numbered from `0` to `n-1`.
- Graph input options:
  - Manually defined (for testing)
  - Randomly generated (for performance measurements)

### 2. Sequential BFS (Python)
- Implements the classic BFS algorithm:
  - Input: Graph and starting node
  - Output: Distances from the starting node to all others
  - Nodes not reachable return `-1`

### 3. Finding Connected Components (Python)
- Implements an algorithm to find all connected components:
  - BFS as a base operation
  - Output: A list of components (each component is a list of its nodes)

### 4. Parallel Algorithms (Python)
- Parallel BFS using the `multiprocessing` library:
  - Parallelization by BFS level frontier or node sets
  - Runtime comparison between sequential and parallel versions

### 5. Sequential Implementation in Rust
- Implements BFS and connected components with Rust:
  - Efficient data structures (`Vec<Vec<usize>>`)
  - Validates correctness by comparison with Python results

### 6. Parallel Implementation in Rust
- Implements parallel BFS/connected components using:
  - Standard threads (`std::thread`)
  - Rayon library (optional)
- Allows thread count adjustment for scalability analysis

### 7. Experimental Evaluation and Measurements
- For graph sizes (e.g., 10k, 50k, 100k nodes), measures:
  - Execution time
  - Comparisons between:
    - Python (sequential and parallel)
    - Rust (sequential and parallel)
- Analysis of:
  - Strong scaling (fixed graph size, increasing threads)
  - Weak scaling (graph size proportional to threads)
- Results presented in tables and graphs.

### 8. Result Visualization
- Displays:
  - BFS levels (distances from starting node)
  - Connected components (distinct colors for each component)
- Visualization implemented in Python or Rust using plots, heatmaps, graphs.

---

## Non-Functional Requirements
- Clear modular code organization
- Version-controlled project (Git)
- Python and Rust implementations maintain identical algorithmic approaches for fair comparison
- Performance measurements conducted on the same machine

---

## Technologies Used
### Python
- `collections.deque`
- `multiprocessing`
- `matplotlib` (plots/graphs)

### Rust
- Standard library
- `rayon` (optional parallelism)

---

## Expected Results
- Functional sequential and parallel implementations of BFS and connected components
- Quantitative performance analysis
- Comprehensive comparison of Python and Rust implementations

---

## Goals of the Project
- Demonstrate understanding of:
  - Graph algorithms
  - Parallel programming
  - Scalability and performance analysis
- Showcase concepts from advanced concurrent programming, including:
  - Parallelization
  - Handling large data structures
  - Measuring and presenting performance insights

---

## How to Run
1. Clone this repository:
   ```
   git clone https://github.com/teodora525/parallel-graph-algorithms.git
   ```
2. Navigate to the project directory:
   ```
   cd parallel-graph-algorithms
   ```
3. Follow the instructions in respective `Python` and `Rust` subdirectories to build and execute the project.

---

## Authors
Teodora525

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.