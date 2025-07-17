# Cloud Architecture Taxonomy

This document catalogs common cloud architecture patterns and services across major providers. The AI code auditor uses these references to detect usage, governance gaps, and cost issues.

See the [Complexity Rating Guide](Complexity-Guide.md) for definitions of implementation, detection, and performance ratings.

## AWS Patterns

| Pattern | Key Concepts | Cost Optimization | Compliance Focus |
|---------|--------------|-------------------|-----------------|
| **EC2 Instance** | Virtual machine provisioning, auto scaling | Right-sizing instances, reserved instances | Security groups, encryption |
| **Lambda Function** | Event-driven compute, serverless | Memory tuning, short timeouts | IAM roles, logging |
| **S3 Bucket** | Object storage, lifecycle policies | Lifecycle rules, infrequent tiers | Public access, encryption |
| **RDS Instance** | Managed relational DB, multi-AZ | Storage autoscaling, reserved DB instances | Backup retention, encryption |
| **CloudFormation/CDK** | Infrastructure as Code templates | Stack reuse, modular design | Change sets, IAM roles |
| **IAM Policy** | Access management documents | Least privilege policies | Policy length, resource scoping |
| **VPC Configuration** | Networking isolation, security groups | Peering vs. NAT costs | CIDR planning, firewall rules |

## Azure Patterns

| Pattern | Key Concepts | Cost Optimization | Compliance Focus |
|---------|--------------|-------------------|-----------------|
| **Azure Function** | Serverless compute, consumption plan | Plan sizing, cold start reduction | Managed identities, logging |
| **Azure App Service** | Web app hosting, deployment slots | Right-size plans, auto-scale | Authentication, diagnostics |
| **ARM Template** | Declarative infrastructure, Bicep | Parameter reuse, template modularity | Role assignments, resource locks |
| **Azure AD Integration** | Identity and access, service principals | Conditional access policies | Least privilege roles |
| **Azure Storage** | Blob, queue, table services | Archive tier, access tiers | Network rules, encryption |

## GCP Patterns

| Pattern | Key Concepts | Cost Optimization | Compliance Focus |
|---------|--------------|-------------------|-----------------|
| **Compute Engine** | VM instances, instance templates | Committed use discounts | Firewall rules, service accounts |
| **Cloud Function** | Event-driven compute, HTTP triggers | Optimize memory and timeout | IAM roles, log retention |
| **Deployment Manager** | Infrastructure as Code, templates | Reusable templates | IAM bindings, audit logging |
| **GCP IAM Policy** | Roles and bindings | Principle of least privilege | Service account scoping |
| **Cloud Storage** | Bucket storage, retention policies | Nearline & Coldline tiers | Bucket policy, encryption |

## Multi-Cloud & Kubernetes

| Pattern | Key Concepts | Cost Optimization | Compliance Focus |
|---------|--------------|-------------------|-----------------|
| **Terraform Module** | Declarative resource provisioning | Module reuse, shared state | Provider credentials |
| **Kubernetes Manifest** | Pod and deployment specs | Resource limits, autoscale | Namespace policies |
| **Helm Chart** | Templated Kubernetes apps | Values overrides, chart reuse | Release security settings |
| **Service Mesh** | Networking control plane | Efficient traffic routing | Mutual TLS, policy enforcement |

## Cloud-Native Patterns

| Pattern | Key Concepts | Cost Optimization | Compliance Focus |
|---------|--------------|-------------------|-----------------|
| **Microservices Architecture** | Small, independent services | Container right-sizing | API gateway policies |
| **Event-Driven Architecture** | Async messaging, pub/sub | Scale consumers on demand | Message retention, ACLs |
| **Serverless Pattern** | Functions as a service | Pay-per-use, cold start control | Logging, IAM policies |
| **Container Orchestration** | Kubernetes, Docker Swarm | Cluster autoscaling | RBAC, network policies |

### Common Compliance Checks

- **Least Privilege**: Ensure IAM policies or role assignments grant only necessary permissions.
- **Encryption**: Verify encryption at rest and in transit for storage and databases.
- **Logging**: Confirm that audit and access logs are enabled and retained.
- **Network Security**: Validate firewall rules, VPC/VNet isolation, and service mesh policies.

### Cost Optimization Hints

- **Right-Sizing**: Analyze resource utilization to select appropriate instance sizes and plans.
- **Reserved Capacity**: Leverage reserved or committed use discounts for long-running workloads.
- **Lifecycle Policies**: Use storage lifecycle rules to transition data to cheaper tiers.
- **Autoscaling**: Configure auto scaling to match demand and avoid overprovisioning.

## Related Patterns

- **Microservices** architectures often employ the **Facade** or **API Gateway** patterns (see [Design Patterns Taxonomy](Design-Patterns-Taxonomy.md)).
- **Serverless** components align with event-driven design patterns.
- **Container** deployments benefit from **Dependency Injection** for managing resources.
