---
name: container-engineering
description: Implement, change, review, or test Dockerfile, Containerfile, .dockerignore, BuildKit/OCI image, and Docker Compose configuration, including build contexts and stages, caches, runtime users, entrypoints, health checks, ports, networks, volumes, secrets, lifecycle, and resource or privilege controls. Do not use for routine command execution or log inspection, Kubernetes/Helm/ECS/Nomad/cloud deployment, application-only changes, supply-chain-only or security-review-only audits, hosted CI pipelines, final ship decisions, or unexplained container failures.
---

# Container Engineering

Use this skill for container build and Docker Compose configuration. Inspect
the repository's application, runtime, and existing container conventions before
changing images or service topology.

## Workflow

1. Inspect container files, ignore rules, compose files, referenced scripts,
   application build output, runtime assumptions, environment/config sources, and
   existing validation commands. Identify the build context, target platforms,
   image consumers, and service lifecycle.
2. Define build and runtime contracts: context boundaries, multi-stage artifact
   transfer, cache inputs, base/runtime separation, required writable paths,
   runtime user, entrypoint and arguments, exposed ports, and health semantics.
3. Keep build contexts minimal with `.dockerignore`; copy only required inputs;
   make cache invalidation intentional; and transfer only the needed artifacts
   between stages. Do not rely on host state or untracked files for a build.
4. Configure runtime behavior explicitly: non-root user where compatible,
   ownership and writable locations, signal-aware entrypoint behavior, health
   checks that reflect readiness, and bounded resources or privileges.
5. For Compose, model services, ports, networks, volumes, secrets/config,
   dependency ordering, health-gated startup where supported, shutdown behavior,
   and persistent-data lifecycle. Avoid coupling unrelated services by default.
6. Build and run the narrowest safe container validation available. Verify image
   build, intended target/stage, runtime user, entrypoint, health check, network
   reachability, volume behavior, and service lifecycle; broaden to integration
   checks when the change crosses service boundaries.

## Security and Supply Chain Guardrails

- Do not embed, print, or commit secrets in images, build arguments, layers,
  compose files, logs, or test artifacts. Keep secrets out of build contexts and
  image history.
- Load [`security-review`](../security-review/SKILL.md) and
  [`security-review-evidence`](../security-review-evidence/SKILL.md) for secrets,
  mounts, ports, capabilities, privileged mode, host sockets, user namespaces, or
  trust boundaries introduced by the container configuration.
- Load
  [`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md)
  for base images, packages, downloaded tools, image digests, registries,
  attestations, SBOMs, or provenance trust. Do not use this skill alone for a
  supply-chain-only audit.
- Prefer least privilege, explicit writable paths, scoped networks, and narrowly
  exposed ports. Treat host mounts, Docker sockets, privileged containers, and
  build-time network access as high-risk exceptions requiring evidence.

## Routing

- Language skills own application build commands, dependency behavior, and
  runtime code; this skill owns their image and Compose integration.
- [`justfiles`](../justfiles/SKILL.md) owns local container command wrappers.
- [`ci-release-engineering`](../ci-release-engineering/SKILL.md) owns hosted
  pipeline configuration that builds, tests, or publishes images.
- Consult current official Docker, BuildKit, OCI, and Compose syntax
  documentation after identifying the configured versions.
- [`systematic-debugging`](../systematic-debugging/SKILL.md) starts active,
  unexplained build, startup, networking, or runtime failures.
- [`release-readiness`](../release-readiness/SKILL.md) owns final ship decisions.
- For a requested review, load [`code-review`](../code-review/SKILL.md) and
  [`review-verification-protocol`](../review-verification-protocol/SKILL.md).
- Exclude routine command execution or log inspection, Kubernetes, Helm, ECS,
  Nomad, cloud deployment systems, application-only changes, and supply-chain-only
  audits.

## Validation and Reporting

- Use repository-owned checks first, then container build and composition checks
  that do not expose credentials or alter shared state. State platform, target,
  and whether caches, volumes, or external services affected the result.
- Report the files changed, image or service behavior changed, validation run and
  results, skipped checks, security-sensitive assumptions, and residual runtime
  or deployment risk.
