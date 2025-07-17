# Architectural Pattern Taxonomy

This document catalogs high-level architectural patterns that the AI code auditor aims to detect in codebases. The detectability rating indicates how reliably the current tooling can identify the pattern:

- ✅ **High** – Strong signals exist and detection is reliable.
- ⚠️ **Partial** – Some signals exist but detection may be incomplete.
- ❌ **None** – No direct detection capability yet.

| Pattern | Description | Example Technologies / Signals | Detectability | Spec Link |
|---------|-------------|--------------------------------|---------------|-----------|
| **Monorepo** | Multiple projects managed in a single repository. | `packages/` or `apps/` directories, `nx.json`, Turborepo config files. | ✅ | N/A |
| **Microservices** | Independent services communicating over a network. | Multiple service directories each with a `Dockerfile`, `services/` folder. | ✅ | [cloud-architecture-spec](../specs/cloud-architecture-spec.yaml) |
| **Event-Driven** | Components communicate via events rather than direct calls. | Message broker configs, pub/sub code, event schema files. | ✅ | [cloud-architecture-spec](../specs/cloud-architecture-spec.yaml) |
| **Layered** | Separation into presentation, domain, and infrastructure layers. | `ui/`, `domain/`, `infrastructure/` folders or packages. | ✅ | N/A |
| **Serverless** | Logic deployed as functions without managing servers. | `serverless.yml`, `*.lambda.js`, IaC referencing AWS/GCP functions. | ✅ | [cloud-architecture-spec](../specs/cloud-architecture-spec.yaml) |

This file serves as the canonical index of supported architectural patterns for detection.

The sections below provide a grouped index inspired by [microservices.io](https://microservices.io). Each bullet notes typical detection signals such as configuration files, code structures, or infrastructure manifests.

## Architectural Style
- **Monolithic Architecture** – Single deployable unit. *Detection:* build configs, single container (code, infra).
- **Microservice Architecture** – Independently deployable services. *Detection:* service directories, network configs (code, config).
- **Event-Driven Architecture** – Publish/subscribe communication via events. *Detection:* broker configs, event classes (config, code).
- **Serverless Architecture** – Functions managed by a cloud provider. *Detection:* function definitions, `serverless.yml` (code, config).
- **Service Mesh** – Layer for service-to-service networking. *Detection:* mesh configuration files, sidecar containers (infra).

## Service Boundaries
- **Decompose by Business Capability** – Split services around distinct capabilities. *Detection:* domain folders, team ownership (code).
- **Decompose by Subdomain** – Boundaries follow domain-driven design subdomains. *Detection:* context packages, modeling artifacts (code).
- **Self-Contained Service** – UI, logic, and data packaged together. *Detection:* service folder containing frontend and backend (code).
- **Service Per Team** – Teams independently own deployment units. *Detection:* repository metadata, code owners (config).
- **Strangler Application** – Gradually replace legacy system with new services. *Detection:* proxy routes, integration wrappers (code, config).
- **Anti-Corruption Layer** – Adapter layer to isolate legacy models. *Detection:* translation classes, interface adapters (code).

## Service Collaboration
- **API Gateway** – Single entry point routing to services. *Detection:* gateway configuration, route mappings (config).
- **Aggregator** – Service composes responses from others. *Detection:* orchestrator classes, HTTP client calls (code).
- **Orchestration** – Central workflow engine coordinates services. *Detection:* workflow definitions, orchestrator configuration (code, config).
- **Choreography** – Services react to events without a central coordinator. *Detection:* event subscriptions, event publishing (code).

## Messaging & Consistency
- **Event Sourcing** – Persist domain events as the source of truth. *Detection:* event store configuration, replay logic (code, config).
- **CQRS** – Separate read/write models. *Detection:* command handlers, query handlers (code).
- **Saga** – Manage long-running distributed transactions. *Detection:* saga definitions, compensation handlers (code).
- **Transactional Outbox** – Publish events from a database outbox table. *Detection:* outbox table schema, publisher job (code, infra).
- **Domain Event** – Domain model publishes events on changes. *Detection:* event classes in domain layer (code).

## Deployment Models
- **Service Instance per Host** – Dedicated VM or physical host per service. *Detection:* infrastructure provisioning scripts (infra).
- **Multiple Service Instances per Host** – Several services share the same host. *Detection:* process manager settings (config).
- **Service Instance per Container** – One service per container, often orchestrated with Kubernetes. *Detection:* Dockerfiles, deployment manifests (config, infra).
- **Serverless Function** – Each function deployed individually in the cloud. *Detection:* cloud function config, IaC templates (config).
- **Sidecar Deployment** – Sidecar containers provide cross-cutting capabilities. *Detection:* Kubernetes pod definitions with sidecars (config, infra).

## Communication Patterns
- **Synchronous REST** – Services communicate via HTTP requests. *Detection:* REST controllers, HTTP clients (code).
- **gRPC/Thrift** – Binary RPC protocols. *Detection:* `.proto`/IDL files, RPC stubs (code).
- **Asynchronous Messaging** – Messaging via queues or pub/sub. *Detection:* message broker configs, consumer code (config, code).
- **GraphQL** – Clients issue flexible queries via a schema. *Detection:* schema files, resolver code (code).
- **Service Mesh Routing** – Mesh handles inter-service routing and retries. *Detection:* mesh policies, virtual services (config, infra).

## Observability & Monitoring
- **Health Check Endpoint** – Endpoint for liveness/readiness checks. *Detection:* `/health` routes, monitoring configs (code, config).
- **Logging Aggregation** – Centralized log collection. *Detection:* log collection configs (config, infra).
- **Distributed Tracing** – Tracing across service boundaries. *Detection:* tracing libraries, instrumentation (code).
- **Metrics Collection** – Expose metrics for monitoring. *Detection:* metrics endpoints, Prometheus config (code, config).
- **Exception Tracking** – Report errors to centralized service. *Detection:* error tracking integrations (code).

## Security & Reliability
- **Circuit Breaker** – Prevent cascading failures. *Detection:* resilience library configuration (code).
- **Bulkhead** – Isolate resources per service or request. *Detection:* thread pool and queue settings (config, code).
- **Rate Limiting** – Throttle incoming requests. *Detection:* gateway policies, middleware (config, code).
- **OAuth/OpenID Connect** – Standardized authentication flows. *Detection:* auth server configuration, security middleware (config, code).
- **mTLS** – Mutual TLS between services. *Detection:* certificate configuration, mesh policies (config, infra).

## UI Composition
- **Backend for Frontend (BFF)** – Custom API for each UI. *Detection:* dedicated BFF service, UI-specific code (code).
- **Page Fragment Composition** – Build pages from service-provided fragments. *Detection:* server-side includes, edge templates (code).
- **Micro Frontend** – Independently deployable front-end modules. *Detection:* module federation configs, build scripts (code).
- **Mobile Adapter** – API adapter optimized for mobile clients. *Detection:* mobile-specific endpoints and config (code).

This structured index helps map code and infrastructure evidence to established architectural concepts.
