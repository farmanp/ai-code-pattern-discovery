# Design Patterns Taxonomy

This document provides a comprehensive reference for design patterns that can be detected by the AI code auditor.

See the [Complexity Rating Guide](Complexity-Guide.md) for definitions of implementation, detection, and performance categories used throughout the specifications.

## Creational Patterns

Patterns that deal with object creation mechanisms, trying to create objects in a manner suitable to the situation.

| Pattern | Category | Key Concepts | Complexity | Use Cases |
|---------|----------|--------------|------------|-----------|
| **Singleton** | Creational | Single instance, global access, lazy initialization | Medium | Configuration managers, logging, caching |
| **Factory Method** | Creational | Product creation, creator hierarchy, polymorphism | Medium | UI components, database connections |
| **Abstract Factory** | Creational | Product families, factory interface, consistency | High | Cross-platform applications, theme systems |
| **Builder** | Creational | Step-by-step construction, fluent API, complex objects | Medium | Configuration objects, SQL query builders |
| **Prototype** | Creational | Object cloning, performance optimization | Medium | Object copying, template systems |

## Structural Patterns

Patterns that deal with object composition and relationships between entities.

| Pattern | Category | Key Concepts | Complexity | Use Cases |
|---------|----------|--------------|------------|-----------|
| **Adapter** | Structural | Interface conversion, legacy integration | Low | Third-party library integration, legacy code |
| **Bridge** | Structural | Abstraction separation, implementation independence | High | Device drivers, GUI frameworks |
| **Composite** | Structural | Tree structures, uniform treatment | Medium | File systems, UI hierarchies, organization charts |
| **Decorator** | Structural | Dynamic behavior addition, wrapper pattern | Medium | Stream processing, middleware, UI enhancements |
| **Facade** | Structural | Simplified interface, subsystem encapsulation | Low | API wrappers, complex system simplification |
| **Flyweight** | Structural | Memory optimization, intrinsic/extrinsic state | High | Text editors, game engines, caching |
| **Proxy** | Structural | Placeholder, access control, lazy loading | Medium | Remote objects, security, caching |

## Behavioral Patterns

Patterns that focus on communication between objects and the assignment of responsibilities.

| Pattern | Category | Key Concepts | Complexity | Use Cases |
|---------|----------|--------------|------------|-----------|
| **Observer** | Behavioral | Event notification, loose coupling | Medium | MVC architectures, event systems |
| **Strategy** | Behavioral | Algorithm families, runtime selection | Low | Payment processing, sorting algorithms |
| **Command** | Behavioral | Request encapsulation, undo/redo | Medium | GUI actions, macro recording, queuing |
| **State** | Behavioral | State-dependent behavior, state transitions | Medium | State machines, game characters, protocols |
| **Template Method** | Behavioral | Algorithm skeleton, hook methods | Low | Frameworks, data processing pipelines |
| **Chain of Responsibility** | Behavioral | Request handling chain, decoupling | Medium | Event handling, validation chains |
| **Mediator** | Behavioral | Communication centralization, loose coupling | Medium | Dialog boxes, chat systems |
| **Memento** | Behavioral | State capture, undo functionality | Medium | Text editors, game save states |
| **Iterator** | Behavioral | Sequential access, collection traversal | Low | Collection frameworks, data structures |
| **Visitor** | Behavioral | Operation externalization, double dispatch | High | Compilers, object hierarchies, reporting |

## Architectural Patterns

High-level patterns that define the overall structure of applications.

| Pattern | Category | Key Concepts | Complexity | Use Cases |
|---------|----------|--------------|------------|-----------|
| **Model-View-Controller (MVC)** | Architectural | Separation of concerns, user interface | Medium | Web applications, desktop applications |
| **Model-View-Presenter (MVP)** | Architectural | Testable views, presenter logic | Medium | Android applications, web forms |
| **Model-View-ViewModel (MVVM)** | Architectural | Data binding, declarative UI | High | WPF applications, modern web frameworks |
| **Repository** | Architectural | Data access abstraction, domain objects | Medium | Data access layers, testing |
| **Dependency Injection** | Architectural | Inversion of control, loose coupling | Medium | Enterprise applications, testing, modularity |

## Pattern Detection Guidelines

### Key Indicators
- **Naming Conventions**: Look for pattern-specific class names and method signatures
- **Structural Elements**: Identify characteristic class relationships and hierarchies
- **Behavioral Signatures**: Recognize typical method calls and interaction patterns
- **Code Organization**: Observe how responsibilities are distributed across classes

### Common Anti-patterns
- **God Object**: Classes that do too much (anti-Singleton)
- **Anemic Domain Model**: Data classes without behavior (anti-Repository)
- **Feature Envy**: Methods that use more features of other classes than their own

### Detection Complexity Levels
- **Simple**: Patterns with clear structural signatures and naming conventions
- **Moderate**: Patterns requiring analysis of method interactions and relationships
- **Complex**: Patterns involving behavioral analysis or multiple variants

## Implementation Quality Metrics

### Thread Safety
- Singleton: Double-checked locking, enum implementation
- Observer: Concurrent modification handling
- Command: Thread-safe command queues

### Performance Considerations
- Flyweight: Memory usage optimization
- Prototype: Cloning vs. construction performance
- Proxy: Lazy loading effectiveness

### Maintainability Factors
- Strategy: Algorithm extensibility
- Template Method: Hook method design
- Visitor: Adding new operations vs. new elements

## Related Patterns

- **Iterator** ↔ Graph traversal algorithms (see [Algorithms & Data Structures Taxonomy](Algorithms-DS-Taxonomy.md))
- **Strategy** ↔ Sorting algorithm selection
- **Visitor** ↔ Tree traversal algorithms
- **Repository** ↔ DataHub datasets (see [DataHub Taxonomy Reference](DataHub-Taxonomy-Reference.md))
- **Observer** ↔ DataHub lineage tracking
- **Factory Method** ↔ DataHub entity creation
- **Singleton** ↔ Thread safety concerns
- **Factory Method** ↔ Input validation patterns
- **Proxy** ↔ Authentication/authorization checks
- **Facade/API Gateway** ↔ Microservices architectures
- **Event-Driven** ↔ Serverless deployments
- **Dependency Injection** ↔ Container orchestration