# Algorithms & Data Structures Taxonomy

This document provides a comprehensive reference for algorithms and data structures that can be detected by the AI code auditor.

See the [Complexity Rating Guide](Complexity-Guide.md) for the meaning of implementation, detection, and performance ratings.

## Data Structures

### Linear Data Structures

| Structure | Access | Search | Insertion | Deletion | Space | Key Characteristics |
|-----------|---------|---------|-----------|----------|--------|-------------------|
| **Array** | O(1) | O(n) | O(n) | O(n) | O(n) | Contiguous memory, fixed size, index-based |
| **Dynamic Array** | O(1) | O(n) | O(1)* | O(n) | O(n) | Resizable, amortized insertion, growth factor |
| **Linked List** | O(n) | O(n) | O(1) | O(1) | O(n) | Dynamic size, sequential access, pointer overhead |
| **Doubly Linked List** | O(n) | O(n) | O(1) | O(1) | O(n) | Bidirectional traversal, extra pointer overhead |
| **Stack** | O(n) | O(n) | O(1) | O(1) | O(n) | LIFO principle, push/pop operations |
| **Queue** | O(n) | O(n) | O(1) | O(1) | O(n) | FIFO principle, enqueue/dequeue operations |

*\* Amortized complexity*

### Tree-Based Data Structures

| Structure | Access | Search | Insertion | Deletion | Space | Key Characteristics |
|-----------|---------|---------|-----------|----------|--------|-------------------|
| **Binary Tree** | O(n) | O(n) | O(n) | O(n) | O(n) | Hierarchical, two children per node |
| **Binary Search Tree** | O(log n)* | O(log n)* | O(log n)* | O(log n)* | O(n) | Ordered property, left < root < right |
| **AVL Tree** | O(log n) | O(log n) | O(log n) | O(log n) | O(n) | Self-balancing, height-balanced |
| **Red-Black Tree** | O(log n) | O(log n) | O(log n) | O(log n) | O(n) | Self-balancing, color properties |
| **Heap** | O(1) | O(n) | O(log n) | O(log n) | O(n) | Complete binary tree, heap property |

*\* Average case; worst case is O(n) for unbalanced BST*

### Hash-Based Data Structures

| Structure | Access | Search | Insertion | Deletion | Space | Key Characteristics |
|-----------|---------|---------|-----------|----------|--------|-------------------|
| **Hash Table** | O(1)* | O(1)* | O(1)* | O(1)* | O(n) | Key-value pairs, hash function, collision handling |
| **Priority Queue** | O(1) | O(n) | O(log n) | O(log n) | O(n) | Priority-based ordering, typically heap-based |

*\* Average case; worst case is O(n) with poor hash function*

### Graph Data Structures

| Structure | Space | Key Characteristics | Best Use Cases |
|-----------|--------|-------------------|----------------|
| **Adjacency Matrix** | O(V²) | Fast edge queries, dense graphs | Dense graphs, frequent edge queries |
| **Adjacency List** | O(V + E) | Space efficient, sparse graphs | Sparse graphs, graph traversals |
| **Edge List** | O(E) | Simple representation | Edge-centric algorithms |

## Sorting Algorithms

| Algorithm | Best Case | Average Case | Worst Case | Space | Stability | Key Characteristics |
|-----------|-----------|--------------|------------|--------|-----------|-------------------|
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | Stable | Simple, adjacent swaps, early termination |
| **Selection Sort** | O(n²) | O(n²) | O(n²) | O(1) | Unstable | Minimum selection, in-place |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | Stable | Adaptive, online, small datasets |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Stable | Divide-and-conquer, predictable |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | Unstable | Pivot-based, in-place, randomized |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | Unstable | Heap-based, in-place, predictable |

### Sorting Algorithm Use Cases

- **Bubble Sort**: Educational purposes, very small datasets
- **Selection Sort**: Memory-constrained environments, small datasets
- **Insertion Sort**: Small datasets, nearly sorted data, online algorithms
- **Merge Sort**: Stable sorting required, linked lists, external sorting
- **Quick Sort**: General-purpose, average-case performance critical
- **Heap Sort**: Worst-case guarantees, in-place sorting required

## Search Algorithms

### Basic Search

| Algorithm | Data Structure | Time Complexity | Space | Key Characteristics |
|-----------|----------------|-----------------|--------|-------------------|
| **Linear Search** | Any | O(n) | O(1) | Sequential scan, works on unsorted data |
| **Binary Search** | Sorted Array | O(log n) | O(1) | Divide-and-conquer, requires sorted data |

### Graph Search

| Algorithm | Time | Space | Key Characteristics | Best Use Cases |
|-----------|------|--------|-------------------|----------------|
| **Depth-First Search (DFS)** | O(V + E) | O(V) | Stack-based, explores deep | Topological sort, cycle detection |
| **Breadth-First Search (BFS)** | O(V + E) | O(V) | Queue-based, level-by-level | Shortest path, level traversal |

## Dynamic Programming Patterns

| Pattern | Example | Time Complexity | Space | Key Characteristics |
|---------|---------|-----------------|--------|-------------------|
| **Fibonacci** | Classic DP | O(n) | O(n) | Overlapping subproblems, memoization |
| **Longest Common Subsequence** | String matching | O(m×n) | O(m×n) | 2D table, optimal substructure |

## String Algorithms

| Algorithm | Time | Space | Key Characteristics | Use Cases |
|-----------|------|--------|-------------------|-----------|
| **KMP (Knuth-Morris-Pratt)** | O(n + m) | O(m) | Pattern preprocessing, failure function | Pattern matching, text search |

## Algorithm Analysis Categories

### Time Complexity Classes
- **O(1)**: Constant time - hash table access, array indexing
- **O(log n)**: Logarithmic - binary search, balanced tree operations
- **O(n)**: Linear - array traversal, linear search
- **O(n log n)**: Linearithmic - efficient sorting algorithms
- **O(n²)**: Quadratic - nested loops, simple sorting algorithms
- **O(2ⁿ)**: Exponential - recursive algorithms without memoization

### Space Complexity Considerations
- **In-place algorithms**: O(1) extra space (heap sort, quick sort)
- **Linear space**: O(n) extra space (merge sort, hash tables)
- **Recursive space**: O(log n) to O(n) for call stack

## Detection Guidelines

### Code Pattern Recognition
- **Data Structure Usage**: Constructor patterns, method signatures
- **Algorithm Implementation**: Loop structures, recursive patterns
- **Complexity Indicators**: Nested loops, recursive calls, data access patterns

### Performance Characteristics
- **Best Case**: Optimal input conditions
- **Average Case**: Expected performance under random conditions
- **Worst Case**: Pathological input conditions
- **Amortized**: Average performance over sequence of operations

### Common Implementation Variants
- **Iterative vs Recursive**: Stack usage, tail recursion optimization
- **In-place vs Extra Space**: Memory usage trade-offs
- **Stable vs Unstable**: Relative order preservation in sorting

## Quality Metrics

### Efficiency Metrics
- **Time Complexity**: Theoretical and practical performance
- **Space Complexity**: Memory usage patterns
- **Cache Performance**: Memory access patterns

### Implementation Quality
- **Correctness**: Boundary conditions, edge cases
- **Robustness**: Error handling, input validation
- **Maintainability**: Code clarity, documentation

### Optimization Opportunities
- **Early Termination**: Loop optimization conditions
- **Memory Access**: Cache-friendly patterns
- **Branch Prediction**: Conditional optimization

## Related Patterns

- Graph traversal algorithms ↔ **Iterator** pattern (see [Design Patterns Taxonomy](Design-Patterns-Taxonomy.md))
- Sorting algorithm selection ↔ **Strategy** pattern
- Tree traversal techniques ↔ **Visitor** pattern