# Skills Database

This document defines every skill that the Skills Extractor Agent can assign. Each skill has a unique `skill_id`, a human-readable name, a category, a default difficulty tier, and a brief description of what it tests in an interview.

---

## Category: Algorithms

| skill_id | Skill Name | Default Difficulty | Description |
|---|---|---|---|
| `binary-search` | Binary Search | Easy | Efficiently locating an element in a sorted collection; log-n guarantee. |
| `two-pointers` | Two-Pointer Technique | Easy | Using two indices to scan inward/outward to solve array/string problems in O(n). |
| `sliding-window` | Sliding Window | Medium | Maintaining a dynamic window over a sequence to track a condition without recomputation. |
| `depth-first-search` | Depth-First Search (DFS) | Medium | Recursive or stack-based traversal of graphs or trees, exploring as deep as possible before backtracking. |
| `breadth-first-search` | Breadth-First Search (BFS) | Medium | Level-order traversal of graphs or trees using a queue; shortest-path in unweighted graphs. |
| `dynamic-programming` | Dynamic Programming | Hard | Breaking problems into overlapping sub-problems; memoization vs. tabulation trade-offs. |
| `greedy` | Greedy Algorithms | Medium | Making locally optimal choices at each step to achieve a global optimum. |
| `divide-and-conquer` | Divide and Conquer | Medium | Recursively splitting a problem, solving sub-problems, and merging results (merge sort, quick sort). |
| `backtracking` | Backtracking | Hard | Exhaustive search with pruning; combinatorial problems (N-queens, permutations, subsets). |
| `sorting` | Sorting Algorithms | Easy | Comparison-based and non-comparison-based sorts; stability, in-place, and adaptive properties. |
| `graph-shortest-path` | Shortest Path (Dijkstra / Bellman-Ford) | Hard | Finding the minimum-cost path between nodes in a weighted graph. |
| `topological-sort` | Topological Sort | Medium | Ordering nodes in a DAG; dependency resolution, build systems. |
| `union-find` | Union-Find / Disjoint Set | Medium | Efficiently tracking connected components; cycle detection in undirected graphs. |
| `bit-manipulation` | Bit Manipulation | Medium | Using bitwise operations for space-efficient solutions and low-level optimizations. |
| `prefix-sum` | Prefix Sum / Cumulative Sum | Easy | Precomputing prefix sums to answer range-sum queries in O(1). |

---

## Category: Data Structures

| skill_id | Skill Name | Default Difficulty | Description |
|---|---|---|---|
| `array` | Arrays & Dynamic Arrays | Easy | Random access, in-place manipulation, amortized resizing. |
| `linked-list` | Linked Lists | Easy | Node-pointer traversal, reversal, cycle detection (Floyd's algorithm). |
| `stack` | Stack | Easy | LIFO semantics; balancing problems, expression evaluation, DFS iteration. |
| `queue` | Queue / Deque | Easy | FIFO semantics; BFS, task scheduling, sliding-window max. |
| `hash-map` | Hash Map / Hash Table | Easy | O(1) average-case lookup/insert; collision resolution, load factor. |
| `hash-set` | Hash Set | Easy | Membership testing in O(1); duplicate detection, intersection/union. |
| `binary-tree` | Binary Tree | Medium | Recursive tree algorithms, height, diameter, path sum. |
| `binary-search-tree` | Binary Search Tree | Medium | In-order traversal gives sorted output; insertion, deletion, balancing. |
| `heap` | Heap / Priority Queue | Medium | O(log n) insert and extract-min/max; top-k problems, Dijkstra's algorithm. |
| `trie` | Trie (Prefix Tree) | Medium | Efficient prefix lookups; autocomplete, spell checking, IP routing. |
| `graph` | Graph Representations | Medium | Adjacency list vs. matrix; directed, undirected, weighted, bipartite. |
| `segment-tree` | Segment Tree | Hard | Range query and point/range update in O(log n); interval problems. |
| `lru-cache` | LRU Cache | Medium | Combining a doubly-linked list and hash map for O(1) get/put with eviction. |
| `monotonic-stack` | Monotonic Stack | Medium | Maintaining a strictly increasing or decreasing stack for next-greater-element style problems. |

---

## Category: Design Patterns

| skill_id | Skill Name | Default Difficulty | Description |
|---|---|---|---|
| `singleton` | Singleton | Easy | Ensuring a single instance; thread-safety considerations. |
| `factory` | Factory / Abstract Factory | Easy | Encapsulating object creation; extensibility and the open/closed principle. |
| `builder` | Builder | Easy | Step-by-step construction of complex objects; fluent interfaces. |
| `observer` | Observer / Event-Listener | Medium | Decoupled publish/subscribe; change notification without tight coupling. |
| `strategy` | Strategy | Medium | Swapping algorithms at runtime; replacing conditionals with polymorphism. |
| `decorator` | Decorator / Wrapper | Medium | Adding behavior to objects without subclassing; middleware stacks. |
| `command` | Command | Medium | Encapsulating requests as objects; undo/redo, task queues. |
| `adapter` | Adapter / Anti-Corruption Layer | Medium | Bridging incompatible interfaces; integration layers. |
| `repository-pattern` | Repository Pattern | Medium | Abstracting data access behind an interface; testability and swappable backends. |
| `dependency-injection` | Dependency Injection / IoC | Medium | Injecting collaborators rather than hard-coding them; testability. |
| `circuit-breaker` | Circuit Breaker | Hard | Preventing cascading failures in distributed systems. |
| `saga` | Saga Pattern | Hard | Managing distributed transactions through compensating actions. |
| `cqrs` | CQRS | Hard | Separating read and write models to optimize each independently. |
| `event-sourcing` | Event Sourcing | Hard | Storing state as a sequence of events; audit trail and temporal queries. |

---

## Category: System Design

| skill_id | Skill Name | Default Difficulty | Description |
|---|---|---|---|
| `api-design` | API Design (REST / GraphQL / gRPC) | Medium | Resource modeling, versioning, idempotency, and contract-first design. |
| `caching` | Caching Strategies | Medium | Cache-aside, write-through, write-behind; TTL, eviction policies, CDN. |
| `message-queue` | Message Queues & Async Messaging | Medium | Decoupling services via Kafka, RabbitMQ, SQS; at-least-once delivery, ordering. |
| `rate-limiting` | Rate Limiting | Medium | Token bucket, leaky bucket, fixed/sliding window; protecting services from abuse. |
| `load-balancing` | Load Balancing | Medium | Round-robin, least-connections, consistent hashing; session affinity. |
| `database-design` | Database Design & Indexing | Medium | Normalization, denormalization, index selection, query optimization. |
| `sharding` | Sharding & Partitioning | Hard | Horizontal scaling of data stores; shard-key selection, hotspot avoidance. |
| `replication` | Replication & Consistency | Hard | Leader-follower, multi-leader; CAP theorem, eventual vs. strong consistency. |
| `microservices` | Microservices Architecture | Hard | Service decomposition, inter-service communication, service mesh, observability. |
| `distributed-tracing` | Observability & Distributed Tracing | Hard | Structured logging, metrics, traces (OpenTelemetry); debugging distributed systems. |
| `health-checks` | Health Checks & Liveness Probes | Easy | Readiness vs. liveness; graceful shutdown and rolling deployments. |
| `idempotency` | Idempotency & At-Least-Once Delivery | Medium | Designing operations safe to retry; idempotency keys. |
