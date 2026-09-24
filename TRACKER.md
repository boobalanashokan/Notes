# MLOps Career Tracker

> **Source of truth:** this file contains the complete roadmap converted
> from the Excel tracker. Edit the `Done?` checkbox here, or let
> `scripts/tracker.py` detect explicit completion from your notes.

## Note → Tracker automation

The tracker scans Markdown notes recursively and uses regex to detect
**explicit** completion only. A note merely existing does **not** mark a
task complete.

Recognized patterns include:

``` text
Status: Done
status: completed
## [x] Topic name
- [x] Topic name
```

It can also complete a topic when all listed subtopics in its matching
note section are checked.

------------------------------------------------------------------------

## Complete Roadmap

### T1 --- Week 1 --- Linux --- Filesystem & shell

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** None
-   **Learning / Outcome:** Understand and be able to explain: pwd / ls
    / cd, cp / mv / rm, mkdir / touch, cat / less / head / tail.
-   **Subtopics to Learn:**
    -   pwd / ls / cd
    -   cp / mv / rm
    -   mkdir / touch
    -   cat / less / head / tail
    -   grep / find
    -   pipes and redirection
    -   wildcards and quoting
-   **Project Task:** Create repo setup notes and a shell script that
    creates the project structure.

### T2 --- Week 1 --- Linux --- Environment & configuration

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T1
-   **Learning / Outcome:** Understand and be able to explain:
    environment variables, PATH, .env files, export / unset.
-   **Subtopics to Learn:**
    -   environment variables
    -   PATH
    -   .env files
    -   export / unset
    -   which / whereis
    -   exit codes
-   **Project Task:** Create a local configuration pattern for the
    project; keep secrets out of Git.

### T3 --- Week 1 --- Linux --- Processes

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T2
-   **Learning / Outcome:** Understand and be able to explain: ps, top /
    htop, kill / pkill, background jobs.
-   **Subtopics to Learn:**
    -   ps
    -   top / htop
    -   kill / pkill
    -   background jobs
    -   exit codes
    -   process ownership
-   **Project Task:** Run the FastAPI prototype as a process and
    practice stopping/restarting it.

### T4 --- Week 1 --- Linux --- Logs & services

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T3
-   **Learning / Outcome:** Understand and be able to explain:
    journalctl, systemctl, service lifecycle, stdout vs stderr.
-   **Subtopics to Learn:**
    -   journalctl
    -   systemctl
    -   service lifecycle
    -   stdout vs stderr
    -   log files
-   **Project Task:** Intentionally create a failing local service and
    document how you diagnose it.

### T5 --- Week 2 --- Linux --- Permissions

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T4
-   **Learning / Outcome:** Understand and be able to explain: users and
    groups, chmod, chown, read/write/execute.
-   **Subtopics to Learn:**
    -   users and groups
    -   chmod
    -   chown
    -   read/write/execute
    -   umask
    -   least privilege
-   **Project Task:** Fix permissions on a project directory without
    using broad 777 permissions.

### T6 --- Week 2 --- Linux --- SSH

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T5
-   **Learning / Outcome:** Understand and be able to explain: SSH keys,
    known_hosts, scp, port basics.
-   **Subtopics to Learn:**
    -   SSH keys
    -   known_hosts
    -   scp
    -   port basics
    -   remote command execution
-   **Project Task:** Connect to a test VM and transfer a project
    artifact securely.

### T7 --- Week 2 --- Linux --- System troubleshooting

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T6
-   **Learning / Outcome:** Understand and be able to explain: disk: df
    / du, memory: free, CPU/process inspection, logs.
-   **Subtopics to Learn:**
    -   disk: df / du
    -   memory: free
    -   CPU/process inspection
    -   logs
    -   ports with ss
    -   curl health checks
-   **Project Task:** Create a troubleshooting checklist and use it
    against a deliberately broken service.

### T8 --- Week 2 --- Linux --- Bash automation

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T7
-   **Learning / Outcome:** Understand and be able to explain:
    variables, arguments, if conditions, loops.
-   **Subtopics to Learn:**
    -   variables
    -   arguments
    -   if conditions
    -   loops
    -   functions
    -   set -e
    -   exit codes
-   **Project Task:** Write scripts for setup, tests, and local service
    startup.

### T9 --- Week 3 --- Networking --- Networking fundamentals

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T8
-   **Learning / Outcome:** Understand and be able to explain: IPv4
    basics, private vs public IP, subnets, ports.
-   **Subtopics to Learn:**
    -   IPv4 basics
    -   private vs public IP
    -   subnets
    -   ports
    -   TCP vs UDP
    -   client/server
-   **Project Task:** Draw the network path for a user request to the
    model API.

### T10 --- Week 3 --- Networking --- DNS

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T9
-   **Learning / Outcome:** Understand and be able to explain: domain
    names, DNS lookup, A/AAAA records, DNS caching.
-   **Subtopics to Learn:**
    -   domain names
    -   DNS lookup
    -   A/AAAA records
    -   DNS caching
    -   localhost
-   **Project Task:** Use DNS tools to troubleshoot a sample service
    hostname.

### T11 --- Week 3 --- Networking --- HTTP/HTTPS

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T10
-   **Learning / Outcome:** Understand and be able to explain: methods,
    status codes, headers, JSON.
-   **Subtopics to Learn:**
    -   methods
    -   status codes
    -   headers
    -   JSON
    -   TLS basics
    -   request/response lifecycle
-   **Project Task:** Test FastAPI endpoints with curl and inspect
    requests/responses.

### T12 --- Week 3 --- Networking --- Service networking

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T11
-   **Learning / Outcome:** Understand and be able to explain:
    firewalls, NAT, reverse proxy, load balancer.
-   **Subtopics to Learn:**
    -   firewalls
    -   NAT
    -   reverse proxy
    -   load balancer
    -   health checks
-   **Project Task:** Document how traffic reaches the inference
    service.

### T13 --- Week 3 --- Git --- Git fundamentals refresh

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T12
-   **Learning / Outcome:** Understand and be able to explain: branch,
    merge, rebase, remote.
-   **Subtopics to Learn:**
    -   branch
    -   merge
    -   rebase
    -   remote
    -   tag
    -   diff
    -   log
-   **Project Task:** Create a clean branching workflow for the project.

### T14 --- Week 3 --- Git --- Git recovery

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T13
-   **Learning / Outcome:** Understand and be able to explain: revert vs
    reset, restore, stash, conflict resolution.
-   **Subtopics to Learn:**
    -   revert vs reset
    -   restore
    -   stash
    -   conflict resolution
    -   bisect
-   **Project Task:** Create and recover from a deliberately bad commit.

### T15 --- Week 4 --- GCP --- Compute Engine

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T14
-   **Learning / Outcome:** Understand and be able to explain: VM
    lifecycle, SSH, machine types, disks.
-   **Subtopics to Learn:**
    -   VM lifecycle
    -   SSH
    -   machine types
    -   disks
    -   startup scripts
    -   service accounts
-   **Project Task:** Create a small test VM and deploy a simple service
    manually.

### T16 --- Week 4 --- GCP --- Cloud Storage

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T15
-   **Learning / Outcome:** Understand and be able to explain: buckets,
    objects, permissions, regional choices.
-   **Subtopics to Learn:**
    -   buckets
    -   objects
    -   permissions
    -   regional choices
    -   CLI operations
-   **Project Task:** Store a sample dataset/model artifact in GCS.

### T17 --- Week 4 --- GCP --- BigQuery

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T16
-   **Learning / Outcome:** Understand and be able to explain: datasets,
    tables, schemas, partitioning basics.
-   **Subtopics to Learn:**
    -   datasets
    -   tables
    -   schemas
    -   partitioning basics
    -   SQL execution
    -   Python client
-   **Project Task:** Load the public/synthetic project data into
    BigQuery.

### T18 --- Week 4 --- GCP --- IAM

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T17
-   **Learning / Outcome:** Understand and be able to explain:
    principals, roles, permissions, predefined vs custom roles.
-   **Subtopics to Learn:**
    -   principals
    -   roles
    -   permissions
    -   predefined vs custom roles
    -   least privilege
-   **Project Task:** Design the service-account permissions for
    training and deployment.

### T19 --- Week 4 --- GCP --- Service accounts

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T18
-   **Learning / Outcome:** Understand and be able to explain: service
    account identity, impersonation, attached service accounts, key
    risks.
-   **Subtopics to Learn:**
    -   service account identity
    -   impersonation
    -   attached service accounts
    -   key risks
-   **Project Task:** Create separate identities for CI and runtime.

### T20 --- Week 4 --- GCP --- VPC & firewall

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T19
-   **Learning / Outcome:** Understand and be able to explain: VPC,
    subnets, firewall rules, ingress/egress.
-   **Subtopics to Learn:**
    -   VPC
    -   subnets
    -   firewall rules
    -   ingress/egress
    -   private networking
-   **Project Task:** Document the network/security boundary for the
    project.

### T21 --- Week 4 --- GCP --- Logging & Monitoring

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T20
-   **Learning / Outcome:** Understand and be able to explain: Cloud
    Logging, log severity, structured logs, basic metrics.
-   **Subtopics to Learn:**
    -   Cloud Logging
    -   log severity
    -   structured logs
    -   basic metrics
    -   alerts
-   **Project Task:** Send application logs to Cloud Logging and inspect
    them.

### T22 --- Week 5 --- CI/CD --- GitHub Actions fundamentals

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T21
-   **Learning / Outcome:** Understand and be able to explain: workflow
    YAML, events, jobs, steps.
-   **Subtopics to Learn:**
    -   workflow YAML
    -   events
    -   jobs
    -   steps
    -   runners
    -   artifacts
    -   secrets
-   **Project Task:** Rebuild a CI workflow from an empty YAML file.

### T23 --- Week 5 --- CI/CD --- Testing in CI

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T22
-   **Learning / Outcome:** Understand and be able to explain: pytest
    command, test discovery, failure output, caching dependencies.
-   **Subtopics to Learn:**
    -   pytest command
    -   test discovery
    -   failure output
    -   caching dependencies
    -   artifacts
-   **Project Task:** Run the complete test suite automatically on
    push/PR.

### T24 --- Week 5 --- Security --- Gitleaks

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T23
-   **Learning / Outcome:** Understand and be able to explain: secret
    patterns, false positives, pre-commit vs CI, failure handling.
-   **Subtopics to Learn:**
    -   secret patterns
    -   false positives
    -   pre-commit vs CI
    -   failure handling
-   **Project Task:** Add secret scanning to CI and test it with a safe
    dummy secret.

### T25 --- Week 5 --- Security --- OIDC / keyless GCP auth

-   **Type:** Refresh
-   **Done?:** \[ \]
-   **Depends On:** T24
-   **Learning / Outcome:** Understand and be able to explain: OIDC
    concept, GitHub identity token, trust relationship, workload
    identity federation.
-   **Subtopics to Learn:**
    -   OIDC concept
    -   GitHub identity token
    -   trust relationship
    -   workload identity federation
    -   short-lived credentials
-   **Project Task:** Rebuild GitHub → GCP authentication without
    storing a service-account key.

### T26 --- Week 5 --- GCP --- Artifact Registry

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T25
-   **Learning / Outcome:** Understand and be able to explain:
    repositories, Docker auth, image tags, immutability concepts.
-   **Subtopics to Learn:**
    -   repositories
    -   Docker auth
    -   image tags
    -   immutability concepts
-   **Project Task:** Build and push the project image to Artifact
    Registry.

### T27 --- Week 5 --- Security --- Secret Manager

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T26
-   **Learning / Outcome:** Understand and be able to explain: secret
    creation, access permissions, runtime retrieval, rotation concept.
-   **Subtopics to Learn:**
    -   secret creation
    -   access permissions
    -   runtime retrieval
    -   rotation concept
-   **Project Task:** Move runtime secrets/config out of source code.

### T28 --- Week 6 --- Python --- Project structure

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T27
-   **Learning / Outcome:** Understand and be able to explain: src
    layout, modules, packages, pyproject.toml.
-   **Subtopics to Learn:**
    -   src layout
    -   modules
    -   packages
    -   pyproject.toml
    -   dependencies
    -   virtual environments
-   **Project Task:** Refactor the project into a clean installable
    Python package.

### T29 --- Week 6 --- Python --- Type hints

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T28
-   **Learning / Outcome:** Understand and be able to explain: typing
    basics, Optional, collections, function annotations.
-   **Subtopics to Learn:**
    -   typing basics
    -   Optional
    -   collections
    -   function annotations
    -   mypy concept
-   **Project Task:** Add useful type hints to core pipeline functions.

### T30 --- Week 6 --- Python --- Exceptions

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T29
-   **Learning / Outcome:** Understand and be able to explain: custom
    exceptions, try/except, exception chaining, fail-fast vs recover.
-   **Subtopics to Learn:**
    -   custom exceptions
    -   try/except
    -   exception chaining
    -   fail-fast vs recover
-   **Project Task:** Define clear errors for data, model, and inference
    failures.

### T31 --- Week 6 --- Python --- Configuration

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T30
-   **Learning / Outcome:** Understand and be able to explain:
    environment-based config, defaults, validation, dev vs prod config.
-   **Subtopics to Learn:**
    -   environment-based config
    -   defaults
    -   validation
    -   dev vs prod config
-   **Project Task:** Create one configuration layer used by training
    and API code.

### T32 --- Week 6 --- Testing --- pytest

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T31
-   **Learning / Outcome:** Understand and be able to explain: unit
    tests, fixtures, parametrize, mocking.
-   **Subtopics to Learn:**
    -   unit tests
    -   fixtures
    -   parametrize
    -   mocking
    -   test isolation
-   **Project Task:** Write tests for data validation, feature logic,
    and model utilities.

### T33 --- Week 6 --- Quality --- Logging

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T32
-   **Learning / Outcome:** Understand and be able to explain: log
    levels, structured logs, request IDs, exception logging.
-   **Subtopics to Learn:**
    -   log levels
    -   structured logs
    -   request IDs
    -   exception logging
-   **Project Task:** Add consistent application/pipeline logging.

### T34 --- Week 7 --- FastAPI --- FastAPI fundamentals

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T33
-   **Learning / Outcome:** Understand and be able to explain: routing,
    path/query/body parameters, Pydantic models, validation.
-   **Subtopics to Learn:**
    -   routing
    -   path/query/body parameters
    -   Pydantic models
    -   validation
    -   OpenAPI
-   **Project Task:** Build a small standalone FastAPI practice service.

### T35 --- Week 7 --- FastAPI --- Inference endpoints

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T34
-   **Learning / Outcome:** Understand and be able to explain: /health,
    /model-info, /predict, HTTP status codes.
-   **Subtopics to Learn:**
    -   /health
    -   /model-info
    -   /predict
    -   HTTP status codes
    -   validation errors
-   **Project Task:** Build the inference API around the registered
    model.

### T36 --- Week 7 --- FastAPI --- API error handling

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T35
-   **Learning / Outcome:** Understand and be able to explain: input
    validation, model-not-loaded failure, internal errors, safe error
    messages.
-   **Subtopics to Learn:**
    -   input validation
    -   model-not-loaded failure
    -   internal errors
    -   safe error messages
-   **Project Task:** Add robust API error handling and tests.

### T37 --- Week 7 --- Docker --- Docker fundamentals

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T36
-   **Learning / Outcome:** Understand and be able to explain: image vs
    container, Dockerfile, layers, build context.
-   **Subtopics to Learn:**
    -   image vs container
    -   Dockerfile
    -   layers
    -   build context
    -   ports
-   **Project Task:** Containerize the FastAPI service.

### T38 --- Week 7 --- Docker --- Docker storage & networking

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T37
-   **Learning / Outcome:** Understand and be able to explain: volumes,
    bind mounts, container networking, environment variables.
-   **Subtopics to Learn:**
    -   volumes
    -   bind mounts
    -   container networking
    -   environment variables
-   **Project Task:** Run API + supporting service locally with Docker.

### T39 --- Week 7 --- Docker --- Production Docker

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T38
-   **Learning / Outcome:** Understand and be able to explain:
    multi-stage builds, non-root user, small base image, healthcheck.
-   **Subtopics to Learn:**
    -   multi-stage builds
    -   non-root user
    -   small base image
    -   healthcheck
    -   .dockerignore
-   **Project Task:** Harden the inference image.

### T40 --- Week 8 --- MLflow --- Tracking fundamentals

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T39
-   **Learning / Outcome:** Understand and be able to explain:
    experiment, run, params, metrics.
-   **Subtopics to Learn:**
    -   experiment
    -   run
    -   params
    -   metrics
    -   artifacts
    -   tags
-   **Project Task:** Track baseline model training in MLflow.

### T41 --- Week 8 --- MLflow --- Reproducibility metadata

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T40
-   **Learning / Outcome:** Understand and be able to explain: git
    commit, dataset version, timestamp, model parameters.
-   **Subtopics to Learn:**
    -   git commit
    -   dataset version
    -   timestamp
    -   model parameters
    -   evaluation metrics
-   **Project Task:** Log complete training metadata for every run.

### T42 --- Week 8 --- MLflow --- Artifacts

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T41
-   **Learning / Outcome:** Understand and be able to explain: model
    artifact, plots, feature metadata, evaluation report.
-   **Subtopics to Learn:**
    -   model artifact
    -   plots
    -   feature metadata
    -   evaluation report
-   **Project Task:** Store model/evaluation artifacts with each run.

### T43 --- Week 9 --- MLflow --- Model Registry

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T42
-   **Learning / Outcome:** Understand and be able to explain:
    registered model, version, alias, stage concept.
-   **Subtopics to Learn:**
    -   registered model
    -   version
    -   alias
    -   stage concept
    -   promotion
-   **Project Task:** Register trained models.

### T44 --- Week 9 --- MLflow --- Evaluation gate

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T43
-   **Learning / Outcome:** Understand and be able to explain:
    validation metric, threshold, comparison, candidate selection.
-   **Subtopics to Learn:**
    -   validation metric
    -   threshold
    -   comparison
    -   candidate selection
-   **Project Task:** Allow promotion only when evaluation criteria
    pass.

### T45 --- Week 9 --- MLflow --- Deployment model loading

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T44
-   **Learning / Outcome:** Understand and be able to explain: registry
    URI, model alias, startup loading, version reporting.
-   **Subtopics to Learn:**
    -   registry URI
    -   model alias
    -   startup loading
    -   version reporting
-   **Project Task:** Make the API load a controlled model version and
    expose its version.

### T46 --- Week 10 --- CI/CD --- ML CI pipeline

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T45
-   **Learning / Outcome:** Understand and be able to explain: checkout,
    Python setup, dependency install, pytest.
-   **Subtopics to Learn:**
    -   checkout
    -   Python setup
    -   dependency install
    -   pytest
    -   quality checks
-   **Project Task:** Create CI pipeline for every pull request.

### T47 --- Week 10 --- Security --- Security checks

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T46
-   **Learning / Outcome:** Understand and be able to explain: secret
    scan, dependency considerations, Docker scan concept, failure
    policy.
-   **Subtopics to Learn:**
    -   secret scan
    -   dependency considerations
    -   Docker scan concept
    -   failure policy
-   **Project Task:** Fail CI when security checks fail.

### T48 --- Week 10 --- ML --- Model evaluation in CI

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T47
-   **Learning / Outcome:** Understand and be able to explain: test
    dataset, metric threshold, artifact output, failure message.
-   **Subtopics to Learn:**
    -   test dataset
    -   metric threshold
    -   artifact output
    -   failure message
-   **Project Task:** Run a lightweight model evaluation gate in CI.

### T49 --- Week 11 --- CI/CD --- Container CD

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T48
-   **Learning / Outcome:** Understand and be able to explain: Docker
    build, image tag, push, commit SHA tags.
-   **Subtopics to Learn:**
    -   Docker build
    -   image tag
    -   push
    -   commit SHA tags
    -   latest pitfalls
-   **Project Task:** Automatically build and push images after approved
    changes.

### T50 --- Week 11 --- CI/CD --- Environment separation

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T49
-   **Learning / Outcome:** Understand and be able to explain: dev,
    staging, prod, environment variables.
-   **Subtopics to Learn:**
    -   dev
    -   staging
    -   prod
    -   environment variables
    -   approval gates
-   **Project Task:** Create environment-aware deployment configuration.

### T51 --- Week 11 --- CI/CD --- Rollback concepts

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T50
-   **Learning / Outcome:** Understand and be able to explain: previous
    image, model version, deployment rollback, database/data caveats.
-   **Subtopics to Learn:**
    -   previous image
    -   model version
    -   deployment rollback
    -   database/data caveats
-   **Project Task:** Demonstrate rollback to a previous
    application/model version.

### T52 --- Week 12 --- Terraform --- Terraform core

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T51
-   **Learning / Outcome:** Understand and be able to explain: provider,
    resource, variable, output.
-   **Subtopics to Learn:**
    -   provider
    -   resource
    -   variable
    -   output
    -   data source
-   **Project Task:** Provision one GCP resource with Terraform.

### T53 --- Week 12 --- Terraform --- Terraform state

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T52
-   **Learning / Outcome:** Understand and be able to explain: state
    purpose, plan, apply, destroy.
-   **Subtopics to Learn:**
    -   state purpose
    -   plan
    -   apply
    -   destroy
    -   state drift
-   **Project Task:** Create and inspect project state.

### T54 --- Week 12 --- Terraform --- Terraform structure

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T53
-   **Learning / Outcome:** Understand and be able to explain: main.tf,
    variables.tf, outputs.tf, terraform.tfvars.
-   **Subtopics to Learn:**
    -   main.tf
    -   variables.tf
    -   outputs.tf
    -   terraform.tfvars
    -   format/validate
-   **Project Task:** Create a clean terraform/ directory.

### T55 --- Week 13 --- Terraform --- GCP infrastructure

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T54
-   **Learning / Outcome:** Understand and be able to explain: Artifact
    Registry, GCS, service accounts, IAM bindings.
-   **Subtopics to Learn:**
    -   Artifact Registry
    -   GCS
    -   service accounts
    -   IAM bindings
-   **Project Task:** Provision the core project infrastructure with
    Terraform.

### T56 --- Week 13 --- Terraform --- Modules

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T55
-   **Learning / Outcome:** Understand and be able to explain: module
    inputs, outputs, reusability, when not to modularize.
-   **Subtopics to Learn:**
    -   module inputs
    -   outputs
    -   reusability
    -   when not to modularize
-   **Project Task:** Extract one reusable infrastructure component.

### T57 --- Week 13 --- Terraform --- Remote state

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T56
-   **Learning / Outcome:** Understand and be able to explain: remote
    backend, state protection, team workflow, separation.
-   **Subtopics to Learn:**
    -   remote backend
    -   state protection
    -   team workflow
    -   separation
-   **Project Task:** Document and configure safe state handling for the
    project.

### T58 --- Week 14 --- Kubernetes --- Core objects

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T57
-   **Learning / Outcome:** Understand and be able to explain: cluster,
    node, pod, deployment.
-   **Subtopics to Learn:**
    -   cluster
    -   node
    -   pod
    -   deployment
    -   service
    -   namespace
-   **Project Task:** Deploy the FastAPI service locally.

### T59 --- Week 14 --- Kubernetes --- Configuration

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T58
-   **Learning / Outcome:** Understand and be able to explain:
    ConfigMap, Secret, environment injection, mounted config.
-   **Subtopics to Learn:**
    -   ConfigMap
    -   Secret
    -   environment injection
    -   mounted config
-   **Project Task:** Move non-secret and secret configuration into K8s
    resources.

### T60 --- Week 14 --- Kubernetes --- Deployment manifests

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T59
-   **Learning / Outcome:** Understand and be able to explain: replicas,
    image, ports, labels.
-   **Subtopics to Learn:**
    -   replicas
    -   image
    -   ports
    -   labels
    -   selectors
-   **Project Task:** Create deployment + service manifests.

### T61 --- Week 15 --- Kubernetes --- Health probes

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T60
-   **Learning / Outcome:** Understand and be able to explain: liveness,
    readiness, startup probe, failure behavior.
-   **Subtopics to Learn:**
    -   liveness
    -   readiness
    -   startup probe
    -   failure behavior
-   **Project Task:** Add probes to the API deployment.

### T62 --- Week 15 --- Kubernetes --- Resources

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T61
-   **Learning / Outcome:** Understand and be able to explain: CPU
    requests, memory requests, limits, scheduling.
-   **Subtopics to Learn:**
    -   CPU requests
    -   memory requests
    -   limits
    -   scheduling
-   **Project Task:** Add realistic resource requests/limits.

### T63 --- Week 15 --- Kubernetes --- Scaling

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T62
-   **Learning / Outcome:** Understand and be able to explain: HPA, CPU
    metrics, replica scaling, stability.
-   **Subtopics to Learn:**
    -   HPA
    -   CPU metrics
    -   replica scaling
    -   stability
-   **Project Task:** Configure horizontal scaling.

### T64 --- Week 15 --- Kubernetes --- Debugging

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T63
-   **Learning / Outcome:** Understand and be able to explain: kubectl
    logs, describe, events, rollout status.
-   **Subtopics to Learn:**
    -   kubectl logs
    -   describe
    -   events
    -   rollout status
    -   exec
-   **Project Task:** Delete/break a pod intentionally and recover it.

### T65 --- Week 16 --- GKE --- GKE deployment

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T64
-   **Learning / Outcome:** Understand and be able to explain: cluster
    creation, node pool, Artifact Registry integration, kubectl context.
-   **Subtopics to Learn:**
    -   cluster creation
    -   node pool
    -   Artifact Registry integration
    -   kubectl context
-   **Project Task:** Deploy the inference service to GKE.

### T66 --- Week 16 --- CI/CD --- CI → GKE

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T65
-   **Learning / Outcome:** Understand and be able to explain: image
    push, deployment update, rollout, deployment status.
-   **Subtopics to Learn:**
    -   image push
    -   deployment update
    -   rollout
    -   deployment status
-   **Project Task:** Automate deployment from GitHub Actions to GKE.

### T67 --- Week 16 --- Kubernetes --- Ingress / external access

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T66
-   **Learning / Outcome:** Understand and be able to explain: ingress
    concept, TLS concept, service exposure, health checks.
-   **Subtopics to Learn:**
    -   ingress concept
    -   TLS concept
    -   service exposure
    -   health checks
-   **Project Task:** Expose the API safely for the demo environment.

### T68 --- Week 17 --- Airflow --- DAG fundamentals

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T67
-   **Learning / Outcome:** Understand and be able to explain: DAG,
    task, dependency, schedule.
-   **Subtopics to Learn:**
    -   DAG
    -   task
    -   dependency
    -   schedule
    -   catchup
    -   backfill
-   **Project Task:** Build a small local DAG.

### T69 --- Week 17 --- Airflow --- Reliability

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T68
-   **Learning / Outcome:** Understand and be able to explain: retries,
    retry delay, timeouts, failure callbacks.
-   **Subtopics to Learn:**
    -   retries
    -   retry delay
    -   timeouts
    -   failure callbacks
    -   idempotency
-   **Project Task:** Make pipeline tasks safe to retry.

### T70 --- Week 17 --- Airflow --- ML training DAG

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T69
-   **Learning / Outcome:** Understand and be able to explain: data
    validation, feature engineering, training, MLflow logging.
-   **Subtopics to Learn:**
    -   data validation
    -   feature engineering
    -   training
    -   MLflow logging
    -   evaluation
-   **Project Task:** Orchestrate the end-to-end training pipeline.

### T71 --- Week 18 --- Monitoring --- Prometheus

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T70
-   **Learning / Outcome:** Understand and be able to explain: metrics
    endpoint, counter, gauge, histogram.
-   **Subtopics to Learn:**
    -   metrics endpoint
    -   counter
    -   gauge
    -   histogram
    -   labels
-   **Project Task:** Instrument FastAPI with useful metrics.

### T72 --- Week 18 --- Monitoring --- Application metrics

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T71
-   **Learning / Outcome:** Understand and be able to explain:
    requests/sec, p95 latency, 5xx rate, prediction count.
-   **Subtopics to Learn:**
    -   requests/sec
    -   p95 latency
    -   5xx rate
    -   prediction count
    -   model version
-   **Project Task:** Expose the core inference metrics.

### T73 --- Week 18 --- Monitoring --- Grafana

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T72
-   **Learning / Outcome:** Understand and be able to explain: data
    source, panels, queries, dashboard layout.
-   **Subtopics to Learn:**
    -   data source
    -   panels
    -   queries
    -   dashboard layout
-   **Project Task:** Create an inference-service dashboard.

### T74 --- Week 19 --- ML Monitoring --- Data drift

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T73
-   **Learning / Outcome:** Understand and be able to explain: feature
    distributions, baseline window, current window, thresholds.
-   **Subtopics to Learn:**
    -   feature distributions
    -   baseline window
    -   current window
    -   thresholds
    -   false alarms
-   **Project Task:** Create a drift simulation using synthetic data.

### T75 --- Week 19 --- ML Monitoring --- Prediction drift

-   **Type:** Learn
-   **Done?:** \[ \]
-   **Depends On:** T74
-   **Learning / Outcome:** Understand and be able to explain:
    prediction distribution, class/score changes, monitoring window.
-   **Subtopics to Learn:**
    -   prediction distribution
    -   class/score changes
    -   monitoring window
-   **Project Task:** Monitor prediction distribution changes.

### T76 --- Week 19 --- ML Monitoring --- Retraining trigger

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T75
-   **Learning / Outcome:** Understand and be able to explain: drift
    alert, quality gate, Airflow trigger, cooldown concept.
-   **Subtopics to Learn:**
    -   drift alert
    -   quality gate
    -   Airflow trigger
    -   cooldown concept
-   **Project Task:** Connect drift detection to retraining.

### T77 --- Week 19 --- ML Monitoring --- Retraining workflow

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T76
-   **Learning / Outcome:** Understand and be able to explain: retrain,
    evaluate, register, deploy.
-   **Subtopics to Learn:**
    -   retrain
    -   evaluate
    -   register
    -   deploy
    -   rollback
-   **Project Task:** Implement alert → retrain → evaluate → register →
    deploy.

### T78 --- Week 20 --- Hardening --- Failure scenarios

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T77
-   **Learning / Outcome:** Understand and be able to explain: bad
    image, bad model, secret failure, pod crash.
-   **Subtopics to Learn:**
    -   bad image
    -   bad model
    -   secret failure
    -   pod crash
    -   drift alert
-   **Project Task:** Run at least five failure drills and document
    recovery.

### T79 --- Week 20 --- Hardening --- Security review

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T78
-   **Learning / Outcome:** Understand and be able to explain: secrets,
    IAM, network exposure, container user.
-   **Subtopics to Learn:**
    -   secrets
    -   IAM
    -   network exposure
    -   container user
    -   CI credentials
-   **Project Task:** Review the project against a production security
    checklist.

### T80 --- Week 20 --- Portfolio --- Architecture documentation

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T79
-   **Learning / Outcome:** Understand and be able to explain: system
    diagram, data flow, deployment flow, monitoring flow.
-   **Subtopics to Learn:**
    -   system diagram
    -   data flow
    -   deployment flow
    -   monitoring flow
-   **Project Task:** Create final architecture diagram and README.

### T81 --- Week 20 --- Portfolio --- Interview readiness

-   **Type:** Build
-   **Done?:** \[ \]
-   **Depends On:** T80
-   **Learning / Outcome:** Understand and be able to explain: why each
    tool, trade-offs, failure modes, debugging path.
-   **Subtopics to Learn:**
    -   why each tool
    -   trade-offs
    -   failure modes
    -   debugging path
    -   alternatives
-   **Project Task:** Prepare a 10-minute live walkthrough of the entire
    system.

------------------------------------------------------------------------

## Completion Rules

-   Mark **Yes** only when you can explain the subtopics and reproduce
    the task yourself.
-   Do not mark a task complete because GPT produced the code.
-   Learning flow: try first → official docs → build/debug → GPT when
    stuck.
-   Portfolio work should use public/synthetic data only.
-   Do not upload VECV proprietary data, code, credentials, internal
    architecture, or confidential information.
