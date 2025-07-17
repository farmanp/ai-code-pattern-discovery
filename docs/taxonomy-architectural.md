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
