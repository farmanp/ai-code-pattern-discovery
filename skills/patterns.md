# Code Pattern to Skill Mapping

This document maps observable code patterns (things the Repo Analyzer Agent detects) to the interview skills they exercise. Use this as the primary lookup table when running the Skills Extractor Agent.

---

## Algorithm Patterns

### Sorting & Searching

| Detected Pattern | Maps To Skills | Difficulty Bump |
|---|---|---|
| Custom comparator / key function in sort call | `sorting` | — |
| Binary search on a sorted array / answer space | `binary-search` | — |
| Two-pointer scan toward the center | `two-pointers` | — |
| Sliding window with max/min tracking | `sliding-window`, `monotonic-stack` | +1 if deque-based |
| Prefix-sum array built before queries | `prefix-sum` | — |

### Graph & Tree Algorithms

| Detected Pattern | Maps To Skills | Difficulty Bump |
|---|---|---|
| Recursive traversal with backtrack on return | `depth-first-search`, `backtracking` | — |
| BFS loop with a queue, level-by-level processing | `breadth-first-search` | — |
| Shortest-path with a priority queue / relaxation | `graph-shortest-path` | +1 if multi-source or negative weights |
| Topological ordering of tasks / dependencies | `topological-sort` | — |
| Union-Find (parent/rank arrays, path compression) | `union-find` | — |
| Segment tree or Fenwick tree for range queries | `segment-tree` | always hard |

### Dynamic Programming

| Detected Pattern | Maps To Skills | Difficulty Bump |
|---|---|---|
| Memoization cache on a recursive function | `dynamic-programming` | — |
| Bottom-up DP table (1-D or 2-D array) | `dynamic-programming` | +1 if 2-D |
| Optimal sub-structure combined with greedy choice | `dynamic-programming`, `greedy` | — |
| Bit-mask DP over subsets | `dynamic-programming`, `bit-manipulation` | always hard |

---

## Data Structure Patterns

| Detected Pattern | Maps To Skills | Notes |
|---|---|---|
| Array with O(1) index access, in-place swaps | `array` | — |
| Linked-list node class with `.next` pointer | `linked-list` | Cycle-detection if Floyd's present |
| `push`/`pop` from one end only | `stack` | — |
| `enqueue`/`dequeue` or `appendleft`/`pop` | `queue` | `deque` → also `monotonic-stack` |
| Dictionary / map for frequency counting or caching | `hash-map` | LRU pattern → also `lru-cache` |
| Set used for O(1) membership testing | `hash-set` | — |
| Class with `left`/`right` child references | `binary-tree` | BST if ordering invariant maintained |
| Heap / `heapq` / `PriorityQueue` in task dispatch | `heap` | — |
| Trie node class with children dict/array | `trie` | — |
| Adjacency list or adjacency matrix | `graph` | — |
| Doubly-linked list + hash map for cache | `lru-cache` | also `hash-map`, `linked-list` |

---

## Design Pattern Signals

| Detected Pattern | Maps To Skills | Notes |
|---|---|---|
| Class with private constructor + static `instance` field | `singleton` | Thread-safety if `synchronized`/lock present |
| `create_*` / `make_*` factory function or `Factory` class | `factory` | Abstract Factory if interface-based |
| Fluent builder with method chaining | `builder` | — |
| `subscribe`/`on_event` callbacks, event emitter | `observer` | also `message-queue` if broker involved |
| Strategy object injected at runtime | `strategy`, `dependency-injection` | — |
| Wrapper class delegating to wrapped object | `decorator` | also `adapter` if interface mismatch |
| Command object with `execute`/`undo` methods | `command` | — |
| Repository/DAO class abstracting persistence | `repository-pattern` | — |
| Constructor injection / DI container | `dependency-injection` | — |
| Retry + open/half-open/closed state machine | `circuit-breaker` | — |
| Compensation handlers for distributed steps | `saga` | also `message-queue` |
| Separate read/write models or services | `cqrs` | — |
| Event store / event log as source of truth | `event-sourcing` | — |

---

## System Design Signals

| Detected Pattern | Maps To Skills | Notes |
|---|---|---|
| HTTP client calls to external services | `api-design` | REST vs. gRPC if proto files present |
| In-memory cache (Redis, Memcached, dict-based) | `caching` | TTL config → eviction policy |
| Message broker config (Kafka, RabbitMQ, SQS) | `message-queue` | Topic/queue names reveal domain |
| Rate-limiter middleware or token-bucket class | `rate-limiting` | — |
| Load-balancer config (nginx, HAProxy, k8s ingress) | `load-balancing` | — |
| ORM models with indices, foreign keys, migrations | `database-design` | — |
| Shard-key logic or partition routing | `sharding` | — |
| Replica set config or read-replica routing | `replication` | — |
| Multiple independent services with own DBs | `microservices` | — |
| Tracing / logging middleware (OpenTelemetry) | `distributed-tracing` | — |
| `/health`, `/ready`, `/live` endpoints | `health-checks` | — |
| Idempotency keys or deduplication IDs | `idempotency` | — |

---

## Difficulty Adjustment Rules

Use these rules **after** initial skill assignment to bump the default difficulty tier:

1. **Combination bonus (+1):** If a single location uses 2+ patterns simultaneously (e.g., BFS + hash-map for visited), bump the combined skill difficulty by one tier.
2. **Scale bonus (+1):** If a concept appears in a production-grade, performance-critical context (e.g., rate limiter used in API gateway), bump by one tier.
3. **Novelty bonus (+1):** If the implementation is non-standard or represents an optimization beyond textbook approaches, bump by one tier.
4. **Trivial cap (−1):** If the pattern is a trivial 2-line usage (e.g., `list.sort()`), cap at easy regardless of the pattern's default.
