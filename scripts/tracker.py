#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
TRACKER = ROOT / "TRACKER.md"
TODAY = ROOT / "TODAY.md"
PROJECT_TASKS = ROOT / "PROJECT_TASKS.md"
SKILLS = ROOT / "SKILLS.md"

ROADMAP_DATA = [
  {
    "id": "T1",
    "week": 1,
    "type": "Learn",
    "area": "Linux",
    "topic": "Filesystem & shell",
    "subtopics": [
      "pwd / ls / cd",
      "cp / mv / rm",
      "mkdir / touch",
      "cat / less / head / tail",
      "grep / find",
      "pipes and redirection",
      "wildcards and quoting"
    ],
    "learning_outcome": "Understand and be able to explain: pwd / ls / cd, cp / mv / rm, mkdir / touch, cat / less / head / tail.",
    "project_task": "Create repo setup notes and a shell script that creates the project structure.",
    "depends_on": "",
    "done": false
  },
  {
    "id": "T2",
    "week": 1,
    "type": "Learn",
    "area": "Linux",
    "topic": "Environment & configuration",
    "subtopics": [
      "environment variables",
      "PATH",
      ".env files",
      "export / unset",
      "which / whereis",
      "exit codes"
    ],
    "learning_outcome": "Understand and be able to explain: environment variables, PATH, .env files, export / unset.",
    "project_task": "Create a local configuration pattern for the project; keep secrets out of Git.",
    "depends_on": "T1",
    "done": false
  },
  {
    "id": "T3",
    "week": 1,
    "type": "Learn",
    "area": "Linux",
    "topic": "Processes",
    "subtopics": [
      "ps",
      "top / htop",
      "kill / pkill",
      "background jobs",
      "exit codes",
      "process ownership"
    ],
    "learning_outcome": "Understand and be able to explain: ps, top / htop, kill / pkill, background jobs.",
    "project_task": "Run the FastAPI prototype as a process and practice stopping/restarting it.",
    "depends_on": "T2",
    "done": false
  },
  {
    "id": "T4",
    "week": 1,
    "type": "Build",
    "area": "Linux",
    "topic": "Logs & services",
    "subtopics": [
      "journalctl",
      "systemctl",
      "service lifecycle",
      "stdout vs stderr",
      "log files"
    ],
    "learning_outcome": "Understand and be able to explain: journalctl, systemctl, service lifecycle, stdout vs stderr.",
    "project_task": "Intentionally create a failing local service and document how you diagnose it.",
    "depends_on": "T3",
    "done": false
  },
  {
    "id": "T5",
    "week": 2,
    "type": "Learn",
    "area": "Linux",
    "topic": "Permissions",
    "subtopics": [
      "users and groups",
      "chmod",
      "chown",
      "read/write/execute",
      "umask",
      "least privilege"
    ],
    "learning_outcome": "Understand and be able to explain: users and groups, chmod, chown, read/write/execute.",
    "project_task": "Fix permissions on a project directory without using broad 777 permissions.",
    "depends_on": "T4",
    "done": false
  },
  {
    "id": "T6",
    "week": 2,
    "type": "Learn",
    "area": "Linux",
    "topic": "SSH",
    "subtopics": [
      "SSH keys",
      "known_hosts",
      "scp",
      "port basics",
      "remote command execution"
    ],
    "learning_outcome": "Understand and be able to explain: SSH keys, known_hosts, scp, port basics.",
    "project_task": "Connect to a test VM and transfer a project artifact securely.",
    "depends_on": "T5",
    "done": false
  },
  {
    "id": "T7",
    "week": 2,
    "type": "Build",
    "area": "Linux",
    "topic": "System troubleshooting",
    "subtopics": [
      "disk: df / du",
      "memory: free",
      "CPU/process inspection",
      "logs",
      "ports with ss",
      "curl health checks"
    ],
    "learning_outcome": "Understand and be able to explain: disk: df / du, memory: free, CPU/process inspection, logs.",
    "project_task": "Create a troubleshooting checklist and use it against a deliberately broken service.",
    "depends_on": "T6",
    "done": false
  },
  {
    "id": "T8",
    "week": 2,
    "type": "Build",
    "area": "Linux",
    "topic": "Bash automation",
    "subtopics": [
      "variables",
      "arguments",
      "if conditions",
      "loops",
      "functions",
      "set -e",
      "exit codes"
    ],
    "learning_outcome": "Understand and be able to explain: variables, arguments, if conditions, loops.",
    "project_task": "Write scripts for setup, tests, and local service startup.",
    "depends_on": "T7",
    "done": false
  },
  {
    "id": "T9",
    "week": 3,
    "type": "Learn",
    "area": "Networking",
    "topic": "Networking fundamentals",
    "subtopics": [
      "IPv4 basics",
      "private vs public IP",
      "subnets",
      "ports",
      "TCP vs UDP",
      "client/server"
    ],
    "learning_outcome": "Understand and be able to explain: IPv4 basics, private vs public IP, subnets, ports.",
    "project_task": "Draw the network path for a user request to the model API.",
    "depends_on": "T8",
    "done": false
  },
  {
    "id": "T10",
    "week": 3,
    "type": "Learn",
    "area": "Networking",
    "topic": "DNS",
    "subtopics": [
      "domain names",
      "DNS lookup",
      "A/AAAA records",
      "DNS caching",
      "localhost"
    ],
    "learning_outcome": "Understand and be able to explain: domain names, DNS lookup, A/AAAA records, DNS caching.",
    "project_task": "Use DNS tools to troubleshoot a sample service hostname.",
    "depends_on": "T9",
    "done": false
  },
  {
    "id": "T11",
    "week": 3,
    "type": "Learn",
    "area": "Networking",
    "topic": "HTTP/HTTPS",
    "subtopics": [
      "methods",
      "status codes",
      "headers",
      "JSON",
      "TLS basics",
      "request/response lifecycle"
    ],
    "learning_outcome": "Understand and be able to explain: methods, status codes, headers, JSON.",
    "project_task": "Test FastAPI endpoints with curl and inspect requests/responses.",
    "depends_on": "T10",
    "done": false
  },
  {
    "id": "T12",
    "week": 3,
    "type": "Learn",
    "area": "Networking",
    "topic": "Service networking",
    "subtopics": [
      "firewalls",
      "NAT",
      "reverse proxy",
      "load balancer",
      "health checks"
    ],
    "learning_outcome": "Understand and be able to explain: firewalls, NAT, reverse proxy, load balancer.",
    "project_task": "Document how traffic reaches the inference service.",
    "depends_on": "T11",
    "done": false
  },
  {
    "id": "T13",
    "week": 3,
    "type": "Learn",
    "area": "Git",
    "topic": "Git fundamentals refresh",
    "subtopics": [
      "branch",
      "merge",
      "rebase",
      "remote",
      "tag",
      "diff",
      "log"
    ],
    "learning_outcome": "Understand and be able to explain: branch, merge, rebase, remote.",
    "project_task": "Create a clean branching workflow for the project.",
    "depends_on": "T12",
    "done": false
  },
  {
    "id": "T14",
    "week": 3,
    "type": "Build",
    "area": "Git",
    "topic": "Git recovery",
    "subtopics": [
      "revert vs reset",
      "restore",
      "stash",
      "conflict resolution",
      "bisect"
    ],
    "learning_outcome": "Understand and be able to explain: revert vs reset, restore, stash, conflict resolution.",
    "project_task": "Create and recover from a deliberately bad commit.",
    "depends_on": "T13",
    "done": false
  },
  {
    "id": "T15",
    "week": 4,
    "type": "Refresh",
    "area": "GCP",
    "topic": "Compute Engine",
    "subtopics": [
      "VM lifecycle",
      "SSH",
      "machine types",
      "disks",
      "startup scripts",
      "service accounts"
    ],
    "learning_outcome": "Understand and be able to explain: VM lifecycle, SSH, machine types, disks.",
    "project_task": "Create a small test VM and deploy a simple service manually.",
    "depends_on": "T14",
    "done": false
  },
  {
    "id": "T16",
    "week": 4,
    "type": "Refresh",
    "area": "GCP",
    "topic": "Cloud Storage",
    "subtopics": [
      "buckets",
      "objects",
      "permissions",
      "regional choices",
      "CLI operations"
    ],
    "learning_outcome": "Understand and be able to explain: buckets, objects, permissions, regional choices.",
    "project_task": "Store a sample dataset/model artifact in GCS.",
    "depends_on": "T15",
    "done": false
  },
  {
    "id": "T17",
    "week": 4,
    "type": "Refresh",
    "area": "GCP",
    "topic": "BigQuery",
    "subtopics": [
      "datasets",
      "tables",
      "schemas",
      "partitioning basics",
      "SQL execution",
      "Python client"
    ],
    "learning_outcome": "Understand and be able to explain: datasets, tables, schemas, partitioning basics.",
    "project_task": "Load the public/synthetic project data into BigQuery.",
    "depends_on": "T16",
    "done": false
  },
  {
    "id": "T18",
    "week": 4,
    "type": "Refresh",
    "area": "GCP",
    "topic": "IAM",
    "subtopics": [
      "principals",
      "roles",
      "permissions",
      "predefined vs custom roles",
      "least privilege"
    ],
    "learning_outcome": "Understand and be able to explain: principals, roles, permissions, predefined vs custom roles.",
    "project_task": "Design the service-account permissions for training and deployment.",
    "depends_on": "T17",
    "done": false
  },
  {
    "id": "T19",
    "week": 4,
    "type": "Refresh",
    "area": "GCP",
    "topic": "Service accounts",
    "subtopics": [
      "service account identity",
      "impersonation",
      "attached service accounts",
      "key risks"
    ],
    "learning_outcome": "Understand and be able to explain: service account identity, impersonation, attached service accounts, key risks.",
    "project_task": "Create separate identities for CI and runtime.",
    "depends_on": "T18",
    "done": false
  },
  {
    "id": "T20",
    "week": 4,
    "type": "Refresh",
    "area": "GCP",
    "topic": "VPC & firewall",
    "subtopics": [
      "VPC",
      "subnets",
      "firewall rules",
      "ingress/egress",
      "private networking"
    ],
    "learning_outcome": "Understand and be able to explain: VPC, subnets, firewall rules, ingress/egress.",
    "project_task": "Document the network/security boundary for the project.",
    "depends_on": "T19",
    "done": false
  },
  {
    "id": "T21",
    "week": 4,
    "type": "Refresh",
    "area": "GCP",
    "topic": "Logging & Monitoring",
    "subtopics": [
      "Cloud Logging",
      "log severity",
      "structured logs",
      "basic metrics",
      "alerts"
    ],
    "learning_outcome": "Understand and be able to explain: Cloud Logging, log severity, structured logs, basic metrics.",
    "project_task": "Send application logs to Cloud Logging and inspect them.",
    "depends_on": "T20",
    "done": false
  },
  {
    "id": "T22",
    "week": 5,
    "type": "Refresh",
    "area": "CI/CD",
    "topic": "GitHub Actions fundamentals",
    "subtopics": [
      "workflow YAML",
      "events",
      "jobs",
      "steps",
      "runners",
      "artifacts",
      "secrets"
    ],
    "learning_outcome": "Understand and be able to explain: workflow YAML, events, jobs, steps.",
    "project_task": "Rebuild a CI workflow from an empty YAML file.",
    "depends_on": "T21",
    "done": false
  },
  {
    "id": "T23",
    "week": 5,
    "type": "Refresh",
    "area": "CI/CD",
    "topic": "Testing in CI",
    "subtopics": [
      "pytest command",
      "test discovery",
      "failure output",
      "caching dependencies",
      "artifacts"
    ],
    "learning_outcome": "Understand and be able to explain: pytest command, test discovery, failure output, caching dependencies.",
    "project_task": "Run the complete test suite automatically on push/PR.",
    "depends_on": "T22",
    "done": false
  },
  {
    "id": "T24",
    "week": 5,
    "type": "Refresh",
    "area": "Security",
    "topic": "Gitleaks",
    "subtopics": [
      "secret patterns",
      "false positives",
      "pre-commit vs CI",
      "failure handling"
    ],
    "learning_outcome": "Understand and be able to explain: secret patterns, false positives, pre-commit vs CI, failure handling.",
    "project_task": "Add secret scanning to CI and test it with a safe dummy secret.",
    "depends_on": "T23",
    "done": false
  },
  {
    "id": "T25",
    "week": 5,
    "type": "Refresh",
    "area": "Security",
    "topic": "OIDC / keyless GCP auth",
    "subtopics": [
      "OIDC concept",
      "GitHub identity token",
      "trust relationship",
      "workload identity federation",
      "short-lived credentials"
    ],
    "learning_outcome": "Understand and be able to explain: OIDC concept, GitHub identity token, trust relationship, workload identity federation.",
    "project_task": "Rebuild GitHub → GCP authentication without storing a service-account key.",
    "depends_on": "T24",
    "done": false
  },
  {
    "id": "T26",
    "week": 5,
    "type": "Build",
    "area": "GCP",
    "topic": "Artifact Registry",
    "subtopics": [
      "repositories",
      "Docker auth",
      "image tags",
      "immutability concepts"
    ],
    "learning_outcome": "Understand and be able to explain: repositories, Docker auth, image tags, immutability concepts.",
    "project_task": "Build and push the project image to Artifact Registry.",
    "depends_on": "T25",
    "done": false
  },
  {
    "id": "T27",
    "week": 5,
    "type": "Build",
    "area": "Security",
    "topic": "Secret Manager",
    "subtopics": [
      "secret creation",
      "access permissions",
      "runtime retrieval",
      "rotation concept"
    ],
    "learning_outcome": "Understand and be able to explain: secret creation, access permissions, runtime retrieval, rotation concept.",
    "project_task": "Move runtime secrets/config out of source code.",
    "depends_on": "T26",
    "done": false
  },
  {
    "id": "T28",
    "week": 6,
    "type": "Learn",
    "area": "Python",
    "topic": "Project structure",
    "subtopics": [
      "src layout",
      "modules",
      "packages",
      "pyproject.toml",
      "dependencies",
      "virtual environments"
    ],
    "learning_outcome": "Understand and be able to explain: src layout, modules, packages, pyproject.toml.",
    "project_task": "Refactor the project into a clean installable Python package.",
    "depends_on": "T27",
    "done": false
  },
  {
    "id": "T29",
    "week": 6,
    "type": "Learn",
    "area": "Python",
    "topic": "Type hints",
    "subtopics": [
      "typing basics",
      "Optional",
      "collections",
      "function annotations",
      "mypy concept"
    ],
    "learning_outcome": "Understand and be able to explain: typing basics, Optional, collections, function annotations.",
    "project_task": "Add useful type hints to core pipeline functions.",
    "depends_on": "T28",
    "done": false
  },
  {
    "id": "T30",
    "week": 6,
    "type": "Learn",
    "area": "Python",
    "topic": "Exceptions",
    "subtopics": [
      "custom exceptions",
      "try/except",
      "exception chaining",
      "fail-fast vs recover"
    ],
    "learning_outcome": "Understand and be able to explain: custom exceptions, try/except, exception chaining, fail-fast vs recover.",
    "project_task": "Define clear errors for data, model, and inference failures.",
    "depends_on": "T29",
    "done": false
  },
  {
    "id": "T31",
    "week": 6,
    "type": "Build",
    "area": "Python",
    "topic": "Configuration",
    "subtopics": [
      "environment-based config",
      "defaults",
      "validation",
      "dev vs prod config"
    ],
    "learning_outcome": "Understand and be able to explain: environment-based config, defaults, validation, dev vs prod config.",
    "project_task": "Create one configuration layer used by training and API code.",
    "depends_on": "T30",
    "done": false
  },
  {
    "id": "T32",
    "week": 6,
    "type": "Build",
    "area": "Testing",
    "topic": "pytest",
    "subtopics": [
      "unit tests",
      "fixtures",
      "parametrize",
      "mocking",
      "test isolation"
    ],
    "learning_outcome": "Understand and be able to explain: unit tests, fixtures, parametrize, mocking.",
    "project_task": "Write tests for data validation, feature logic, and model utilities.",
    "depends_on": "T31",
    "done": false
  },
  {
    "id": "T33",
    "week": 6,
    "type": "Build",
    "area": "Quality",
    "topic": "Logging",
    "subtopics": [
      "log levels",
      "structured logs",
      "request IDs",
      "exception logging"
    ],
    "learning_outcome": "Understand and be able to explain: log levels, structured logs, request IDs, exception logging.",
    "project_task": "Add consistent application/pipeline logging.",
    "depends_on": "T32",
    "done": false
  },
  {
    "id": "T34",
    "week": 7,
    "type": "Learn",
    "area": "FastAPI",
    "topic": "FastAPI fundamentals",
    "subtopics": [
      "routing",
      "path/query/body parameters",
      "Pydantic models",
      "validation",
      "OpenAPI"
    ],
    "learning_outcome": "Understand and be able to explain: routing, path/query/body parameters, Pydantic models, validation.",
    "project_task": "Build a small standalone FastAPI practice service.",
    "depends_on": "T33",
    "done": false
  },
  {
    "id": "T35",
    "week": 7,
    "type": "Build",
    "area": "FastAPI",
    "topic": "Inference endpoints",
    "subtopics": [
      "/health",
      "/model-info",
      "/predict",
      "HTTP status codes",
      "validation errors"
    ],
    "learning_outcome": "Understand and be able to explain: /health, /model-info, /predict, HTTP status codes.",
    "project_task": "Build the inference API around the registered model.",
    "depends_on": "T34",
    "done": false
  },
  {
    "id": "T36",
    "week": 7,
    "type": "Build",
    "area": "FastAPI",
    "topic": "API error handling",
    "subtopics": [
      "input validation",
      "model-not-loaded failure",
      "internal errors",
      "safe error messages"
    ],
    "learning_outcome": "Understand and be able to explain: input validation, model-not-loaded failure, internal errors, safe error messages.",
    "project_task": "Add robust API error handling and tests.",
    "depends_on": "T35",
    "done": false
  },
  {
    "id": "T37",
    "week": 7,
    "type": "Learn",
    "area": "Docker",
    "topic": "Docker fundamentals",
    "subtopics": [
      "image vs container",
      "Dockerfile",
      "layers",
      "build context",
      "ports"
    ],
    "learning_outcome": "Understand and be able to explain: image vs container, Dockerfile, layers, build context.",
    "project_task": "Containerize the FastAPI service.",
    "depends_on": "T36",
    "done": false
  },
  {
    "id": "T38",
    "week": 7,
    "type": "Learn",
    "area": "Docker",
    "topic": "Docker storage & networking",
    "subtopics": [
      "volumes",
      "bind mounts",
      "container networking",
      "environment variables"
    ],
    "learning_outcome": "Understand and be able to explain: volumes, bind mounts, container networking, environment variables.",
    "project_task": "Run API + supporting service locally with Docker.",
    "depends_on": "T37",
    "done": false
  },
  {
    "id": "T39",
    "week": 7,
    "type": "Build",
    "area": "Docker",
    "topic": "Production Docker",
    "subtopics": [
      "multi-stage builds",
      "non-root user",
      "small base image",
      "healthcheck",
      ".dockerignore"
    ],
    "learning_outcome": "Understand and be able to explain: multi-stage builds, non-root user, small base image, healthcheck.",
    "project_task": "Harden the inference image.",
    "depends_on": "T38",
    "done": false
  },
  {
    "id": "T40",
    "week": 8,
    "type": "Learn",
    "area": "MLflow",
    "topic": "Tracking fundamentals",
    "subtopics": [
      "experiment",
      "run",
      "params",
      "metrics",
      "artifacts",
      "tags"
    ],
    "learning_outcome": "Understand and be able to explain: experiment, run, params, metrics.",
    "project_task": "Track baseline model training in MLflow.",
    "depends_on": "T39",
    "done": false
  },
  {
    "id": "T41",
    "week": 8,
    "type": "Build",
    "area": "MLflow",
    "topic": "Reproducibility metadata",
    "subtopics": [
      "git commit",
      "dataset version",
      "timestamp",
      "model parameters",
      "evaluation metrics"
    ],
    "learning_outcome": "Understand and be able to explain: git commit, dataset version, timestamp, model parameters.",
    "project_task": "Log complete training metadata for every run.",
    "depends_on": "T40",
    "done": false
  },
  {
    "id": "T42",
    "week": 8,
    "type": "Build",
    "area": "MLflow",
    "topic": "Artifacts",
    "subtopics": [
      "model artifact",
      "plots",
      "feature metadata",
      "evaluation report"
    ],
    "learning_outcome": "Understand and be able to explain: model artifact, plots, feature metadata, evaluation report.",
    "project_task": "Store model/evaluation artifacts with each run.",
    "depends_on": "T41",
    "done": false
  },
  {
    "id": "T43",
    "week": 9,
    "type": "Learn",
    "area": "MLflow",
    "topic": "Model Registry",
    "subtopics": [
      "registered model",
      "version",
      "alias",
      "stage concept",
      "promotion"
    ],
    "learning_outcome": "Understand and be able to explain: registered model, version, alias, stage concept.",
    "project_task": "Register trained models.",
    "depends_on": "T42",
    "done": false
  },
  {
    "id": "T44",
    "week": 9,
    "type": "Build",
    "area": "MLflow",
    "topic": "Evaluation gate",
    "subtopics": [
      "validation metric",
      "threshold",
      "comparison",
      "candidate selection"
    ],
    "learning_outcome": "Understand and be able to explain: validation metric, threshold, comparison, candidate selection.",
    "project_task": "Allow promotion only when evaluation criteria pass.",
    "depends_on": "T43",
    "done": false
  },
  {
    "id": "T45",
    "week": 9,
    "type": "Build",
    "area": "MLflow",
    "topic": "Deployment model loading",
    "subtopics": [
      "registry URI",
      "model alias",
      "startup loading",
      "version reporting"
    ],
    "learning_outcome": "Understand and be able to explain: registry URI, model alias, startup loading, version reporting.",
    "project_task": "Make the API load a controlled model version and expose its version.",
    "depends_on": "T44",
    "done": false
  },
  {
    "id": "T46",
    "week": 10,
    "type": "Build",
    "area": "CI/CD",
    "topic": "ML CI pipeline",
    "subtopics": [
      "checkout",
      "Python setup",
      "dependency install",
      "pytest",
      "quality checks"
    ],
    "learning_outcome": "Understand and be able to explain: checkout, Python setup, dependency install, pytest.",
    "project_task": "Create CI pipeline for every pull request.",
    "depends_on": "T45",
    "done": false
  },
  {
    "id": "T47",
    "week": 10,
    "type": "Build",
    "area": "Security",
    "topic": "Security checks",
    "subtopics": [
      "secret scan",
      "dependency considerations",
      "Docker scan concept",
      "failure policy"
    ],
    "learning_outcome": "Understand and be able to explain: secret scan, dependency considerations, Docker scan concept, failure policy.",
    "project_task": "Fail CI when security checks fail.",
    "depends_on": "T46",
    "done": false
  },
  {
    "id": "T48",
    "week": 10,
    "type": "Build",
    "area": "ML",
    "topic": "Model evaluation in CI",
    "subtopics": [
      "test dataset",
      "metric threshold",
      "artifact output",
      "failure message"
    ],
    "learning_outcome": "Understand and be able to explain: test dataset, metric threshold, artifact output, failure message.",
    "project_task": "Run a lightweight model evaluation gate in CI.",
    "depends_on": "T47",
    "done": false
  },
  {
    "id": "T49",
    "week": 11,
    "type": "Build",
    "area": "CI/CD",
    "topic": "Container CD",
    "subtopics": [
      "Docker build",
      "image tag",
      "push",
      "commit SHA tags",
      "latest pitfalls"
    ],
    "learning_outcome": "Understand and be able to explain: Docker build, image tag, push, commit SHA tags.",
    "project_task": "Automatically build and push images after approved changes.",
    "depends_on": "T48",
    "done": false
  },
  {
    "id": "T50",
    "week": 11,
    "type": "Build",
    "area": "CI/CD",
    "topic": "Environment separation",
    "subtopics": [
      "dev",
      "staging",
      "prod",
      "environment variables",
      "approval gates"
    ],
    "learning_outcome": "Understand and be able to explain: dev, staging, prod, environment variables.",
    "project_task": "Create environment-aware deployment configuration.",
    "depends_on": "T49",
    "done": false
  },
  {
    "id": "T51",
    "week": 11,
    "type": "Build",
    "area": "CI/CD",
    "topic": "Rollback concepts",
    "subtopics": [
      "previous image",
      "model version",
      "deployment rollback",
      "database/data caveats"
    ],
    "learning_outcome": "Understand and be able to explain: previous image, model version, deployment rollback, database/data caveats.",
    "project_task": "Demonstrate rollback to a previous application/model version.",
    "depends_on": "T50",
    "done": false
  },
  {
    "id": "T52",
    "week": 12,
    "type": "Learn",
    "area": "Terraform",
    "topic": "Terraform core",
    "subtopics": [
      "provider",
      "resource",
      "variable",
      "output",
      "data source"
    ],
    "learning_outcome": "Understand and be able to explain: provider, resource, variable, output.",
    "project_task": "Provision one GCP resource with Terraform.",
    "depends_on": "T51",
    "done": false
  },
  {
    "id": "T53",
    "week": 12,
    "type": "Learn",
    "area": "Terraform",
    "topic": "Terraform state",
    "subtopics": [
      "state purpose",
      "plan",
      "apply",
      "destroy",
      "state drift"
    ],
    "learning_outcome": "Understand and be able to explain: state purpose, plan, apply, destroy.",
    "project_task": "Create and inspect project state.",
    "depends_on": "T52",
    "done": false
  },
  {
    "id": "T54",
    "week": 12,
    "type": "Build",
    "area": "Terraform",
    "topic": "Terraform structure",
    "subtopics": [
      "main.tf",
      "variables.tf",
      "outputs.tf",
      "terraform.tfvars",
      "format/validate"
    ],
    "learning_outcome": "Understand and be able to explain: main.tf, variables.tf, outputs.tf, terraform.tfvars.",
    "project_task": "Create a clean terraform/ directory.",
    "depends_on": "T53",
    "done": false
  },
  {
    "id": "T55",
    "week": 13,
    "type": "Build",
    "area": "Terraform",
    "topic": "GCP infrastructure",
    "subtopics": [
      "Artifact Registry",
      "GCS",
      "service accounts",
      "IAM bindings"
    ],
    "learning_outcome": "Understand and be able to explain: Artifact Registry, GCS, service accounts, IAM bindings.",
    "project_task": "Provision the core project infrastructure with Terraform.",
    "depends_on": "T54",
    "done": false
  },
  {
    "id": "T56",
    "week": 13,
    "type": "Learn",
    "area": "Terraform",
    "topic": "Modules",
    "subtopics": [
      "module inputs",
      "outputs",
      "reusability",
      "when not to modularize"
    ],
    "learning_outcome": "Understand and be able to explain: module inputs, outputs, reusability, when not to modularize.",
    "project_task": "Extract one reusable infrastructure component.",
    "depends_on": "T55",
    "done": false
  },
  {
    "id": "T57",
    "week": 13,
    "type": "Learn",
    "area": "Terraform",
    "topic": "Remote state",
    "subtopics": [
      "remote backend",
      "state protection",
      "team workflow",
      "separation"
    ],
    "learning_outcome": "Understand and be able to explain: remote backend, state protection, team workflow, separation.",
    "project_task": "Document and configure safe state handling for the project.",
    "depends_on": "T56",
    "done": false
  },
  {
    "id": "T58",
    "week": 14,
    "type": "Learn",
    "area": "Kubernetes",
    "topic": "Core objects",
    "subtopics": [
      "cluster",
      "node",
      "pod",
      "deployment",
      "service",
      "namespace"
    ],
    "learning_outcome": "Understand and be able to explain: cluster, node, pod, deployment.",
    "project_task": "Deploy the FastAPI service locally.",
    "depends_on": "T57",
    "done": false
  },
  {
    "id": "T59",
    "week": 14,
    "type": "Learn",
    "area": "Kubernetes",
    "topic": "Configuration",
    "subtopics": [
      "ConfigMap",
      "Secret",
      "environment injection",
      "mounted config"
    ],
    "learning_outcome": "Understand and be able to explain: ConfigMap, Secret, environment injection, mounted config.",
    "project_task": "Move non-secret and secret configuration into K8s resources.",
    "depends_on": "T58",
    "done": false
  },
  {
    "id": "T60",
    "week": 14,
    "type": "Build",
    "area": "Kubernetes",
    "topic": "Deployment manifests",
    "subtopics": [
      "replicas",
      "image",
      "ports",
      "labels",
      "selectors"
    ],
    "learning_outcome": "Understand and be able to explain: replicas, image, ports, labels.",
    "project_task": "Create deployment + service manifests.",
    "depends_on": "T59",
    "done": false
  },
  {
    "id": "T61",
    "week": 15,
    "type": "Learn",
    "area": "Kubernetes",
    "topic": "Health probes",
    "subtopics": [
      "liveness",
      "readiness",
      "startup probe",
      "failure behavior"
    ],
    "learning_outcome": "Understand and be able to explain: liveness, readiness, startup probe, failure behavior.",
    "project_task": "Add probes to the API deployment.",
    "depends_on": "T60",
    "done": false
  },
  {
    "id": "T62",
    "week": 15,
    "type": "Learn",
    "area": "Kubernetes",
    "topic": "Resources",
    "subtopics": [
      "CPU requests",
      "memory requests",
      "limits",
      "scheduling"
    ],
    "learning_outcome": "Understand and be able to explain: CPU requests, memory requests, limits, scheduling.",
    "project_task": "Add realistic resource requests/limits.",
    "depends_on": "T61",
    "done": false
  },
  {
    "id": "T63",
    "week": 15,
    "type": "Learn",
    "area": "Kubernetes",
    "topic": "Scaling",
    "subtopics": [
      "HPA",
      "CPU metrics",
      "replica scaling",
      "stability"
    ],
    "learning_outcome": "Understand and be able to explain: HPA, CPU metrics, replica scaling, stability.",
    "project_task": "Configure horizontal scaling.",
    "depends_on": "T62",
    "done": false
  },
  {
    "id": "T64",
    "week": 15,
    "type": "Build",
    "area": "Kubernetes",
    "topic": "Debugging",
    "subtopics": [
      "kubectl logs",
      "describe",
      "events",
      "rollout status",
      "exec"
    ],
    "learning_outcome": "Understand and be able to explain: kubectl logs, describe, events, rollout status.",
    "project_task": "Delete/break a pod intentionally and recover it.",
    "depends_on": "T63",
    "done": false
  },
  {
    "id": "T65",
    "week": 16,
    "type": "Build",
    "area": "GKE",
    "topic": "GKE deployment",
    "subtopics": [
      "cluster creation",
      "node pool",
      "Artifact Registry integration",
      "kubectl context"
    ],
    "learning_outcome": "Understand and be able to explain: cluster creation, node pool, Artifact Registry integration, kubectl context.",
    "project_task": "Deploy the inference service to GKE.",
    "depends_on": "T64",
    "done": false
  },
  {
    "id": "T66",
    "week": 16,
    "type": "Build",
    "area": "CI/CD",
    "topic": "CI → GKE",
    "subtopics": [
      "image push",
      "deployment update",
      "rollout",
      "deployment status"
    ],
    "learning_outcome": "Understand and be able to explain: image push, deployment update, rollout, deployment status.",
    "project_task": "Automate deployment from GitHub Actions to GKE.",
    "depends_on": "T65",
    "done": false
  },
  {
    "id": "T67",
    "week": 16,
    "type": "Learn",
    "area": "Kubernetes",
    "topic": "Ingress / external access",
    "subtopics": [
      "ingress concept",
      "TLS concept",
      "service exposure",
      "health checks"
    ],
    "learning_outcome": "Understand and be able to explain: ingress concept, TLS concept, service exposure, health checks.",
    "project_task": "Expose the API safely for the demo environment.",
    "depends_on": "T66",
    "done": false
  },
  {
    "id": "T68",
    "week": 17,
    "type": "Learn",
    "area": "Airflow",
    "topic": "DAG fundamentals",
    "subtopics": [
      "DAG",
      "task",
      "dependency",
      "schedule",
      "catchup",
      "backfill"
    ],
    "learning_outcome": "Understand and be able to explain: DAG, task, dependency, schedule.",
    "project_task": "Build a small local DAG.",
    "depends_on": "T67",
    "done": false
  },
  {
    "id": "T69",
    "week": 17,
    "type": "Learn",
    "area": "Airflow",
    "topic": "Reliability",
    "subtopics": [
      "retries",
      "retry delay",
      "timeouts",
      "failure callbacks",
      "idempotency"
    ],
    "learning_outcome": "Understand and be able to explain: retries, retry delay, timeouts, failure callbacks.",
    "project_task": "Make pipeline tasks safe to retry.",
    "depends_on": "T68",
    "done": false
  },
  {
    "id": "T70",
    "week": 17,
    "type": "Build",
    "area": "Airflow",
    "topic": "ML training DAG",
    "subtopics": [
      "data validation",
      "feature engineering",
      "training",
      "MLflow logging",
      "evaluation"
    ],
    "learning_outcome": "Understand and be able to explain: data validation, feature engineering, training, MLflow logging.",
    "project_task": "Orchestrate the end-to-end training pipeline.",
    "depends_on": "T69",
    "done": false
  },
  {
    "id": "T71",
    "week": 18,
    "type": "Learn",
    "area": "Monitoring",
    "topic": "Prometheus",
    "subtopics": [
      "metrics endpoint",
      "counter",
      "gauge",
      "histogram",
      "labels"
    ],
    "learning_outcome": "Understand and be able to explain: metrics endpoint, counter, gauge, histogram.",
    "project_task": "Instrument FastAPI with useful metrics.",
    "depends_on": "T70",
    "done": false
  },
  {
    "id": "T72",
    "week": 18,
    "type": "Build",
    "area": "Monitoring",
    "topic": "Application metrics",
    "subtopics": [
      "requests/sec",
      "p95 latency",
      "5xx rate",
      "prediction count",
      "model version"
    ],
    "learning_outcome": "Understand and be able to explain: requests/sec, p95 latency, 5xx rate, prediction count.",
    "project_task": "Expose the core inference metrics.",
    "depends_on": "T71",
    "done": false
  },
  {
    "id": "T73",
    "week": 18,
    "type": "Build",
    "area": "Monitoring",
    "topic": "Grafana",
    "subtopics": [
      "data source",
      "panels",
      "queries",
      "dashboard layout"
    ],
    "learning_outcome": "Understand and be able to explain: data source, panels, queries, dashboard layout.",
    "project_task": "Create an inference-service dashboard.",
    "depends_on": "T72",
    "done": false
  },
  {
    "id": "T74",
    "week": 19,
    "type": "Learn",
    "area": "ML Monitoring",
    "topic": "Data drift",
    "subtopics": [
      "feature distributions",
      "baseline window",
      "current window",
      "thresholds",
      "false alarms"
    ],
    "learning_outcome": "Understand and be able to explain: feature distributions, baseline window, current window, thresholds.",
    "project_task": "Create a drift simulation using synthetic data.",
    "depends_on": "T73",
    "done": false
  },
  {
    "id": "T75",
    "week": 19,
    "type": "Learn",
    "area": "ML Monitoring",
    "topic": "Prediction drift",
    "subtopics": [
      "prediction distribution",
      "class/score changes",
      "monitoring window"
    ],
    "learning_outcome": "Understand and be able to explain: prediction distribution, class/score changes, monitoring window.",
    "project_task": "Monitor prediction distribution changes.",
    "depends_on": "T74",
    "done": false
  },
  {
    "id": "T76",
    "week": 19,
    "type": "Build",
    "area": "ML Monitoring",
    "topic": "Retraining trigger",
    "subtopics": [
      "drift alert",
      "quality gate",
      "Airflow trigger",
      "cooldown concept"
    ],
    "learning_outcome": "Understand and be able to explain: drift alert, quality gate, Airflow trigger, cooldown concept.",
    "project_task": "Connect drift detection to retraining.",
    "depends_on": "T75",
    "done": false
  },
  {
    "id": "T77",
    "week": 19,
    "type": "Build",
    "area": "ML Monitoring",
    "topic": "Retraining workflow",
    "subtopics": [
      "retrain",
      "evaluate",
      "register",
      "deploy",
      "rollback"
    ],
    "learning_outcome": "Understand and be able to explain: retrain, evaluate, register, deploy.",
    "project_task": "Implement alert → retrain → evaluate → register → deploy.",
    "depends_on": "T76",
    "done": false
  },
  {
    "id": "T78",
    "week": 20,
    "type": "Build",
    "area": "Hardening",
    "topic": "Failure scenarios",
    "subtopics": [
      "bad image",
      "bad model",
      "secret failure",
      "pod crash",
      "drift alert"
    ],
    "learning_outcome": "Understand and be able to explain: bad image, bad model, secret failure, pod crash.",
    "project_task": "Run at least five failure drills and document recovery.",
    "depends_on": "T77",
    "done": false
  },
  {
    "id": "T79",
    "week": 20,
    "type": "Build",
    "area": "Hardening",
    "topic": "Security review",
    "subtopics": [
      "secrets",
      "IAM",
      "network exposure",
      "container user",
      "CI credentials"
    ],
    "learning_outcome": "Understand and be able to explain: secrets, IAM, network exposure, container user.",
    "project_task": "Review the project against a production security checklist.",
    "depends_on": "T78",
    "done": false
  },
  {
    "id": "T80",
    "week": 20,
    "type": "Build",
    "area": "Portfolio",
    "topic": "Architecture documentation",
    "subtopics": [
      "system diagram",
      "data flow",
      "deployment flow",
      "monitoring flow"
    ],
    "learning_outcome": "Understand and be able to explain: system diagram, data flow, deployment flow, monitoring flow.",
    "project_task": "Create final architecture diagram and README.",
    "depends_on": "T79",
    "done": false
  },
  {
    "id": "T81",
    "week": 20,
    "type": "Build",
    "area": "Portfolio",
    "topic": "Interview readiness",
    "subtopics": [
      "why each tool",
      "trade-offs",
      "failure modes",
      "debugging path",
      "alternatives"
    ],
    "learning_outcome": "Understand and be able to explain: why each tool, trade-offs, failure modes, debugging path.",
    "project_task": "Prepare a 10-minute live walkthrough of the entire system.",
    "depends_on": "T80",
    "done": false
  }
]

# ---------- Regex rules ----------
STATUS_DONE_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?(?:status|state|progress)\s*[:\-]\s*"
    r"(?:done|complete|completed|finished)\s*$"
)
CHECKED_TOPIC_RE = re.compile(r"(?im)^\s*[-*]?\s*\[x\]\s+(?P<text>.+?)\s*$")
HEADING_RE = re.compile(r"(?im)^\s*#{1,6}\s+(?P<text>.+?)\s*$")
CHECKBOX_RE = re.compile(r"(?im)^\s*[-*]\s*\[(?P<mark>[ xX])\]\s+(?P<text>.+?)\s*$")


def normalize(value: str) -> str:
    value = re.sub(r"[`*_]", "", value)
    return re.sub(r"\s+", " ", value.strip().lower())


def topic_is_unique(topic: str) -> bool:
    n = normalize(topic)
    return sum(normalize(r["topic"]) == n for r in ROADMAP_DATA) == 1


def topic_matches(text: str, area: str, topic: str) -> bool:
    n = normalize(text)
    return normalize(topic) in n and (normalize(area) in n or topic_is_unique(topic))


def section_for_topic(note_text: str, area: str, topic: str):
    matches = list(HEADING_RE.finditer(note_text))
    for i, m in enumerate(matches):
        if topic_matches(m.group("text"), area, topic):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(note_text)
            return note_text[start:end]
    return None


def explicit_done_in_section(section: str, topic: str, subtopics: list[str]) -> bool:
    if STATUS_DONE_RE.search(section):
        return True

    for m in CHECKED_TOPIC_RE.finditer(section):
        if normalize(topic) in normalize(m.group("text")):
            return True

    checked = [
        normalize(m.group("text"))
        for m in CHECKBOX_RE.finditer(section)
        if m.group("mark").lower() == "x"
    ]
    return bool(subtopics) and all(
        any(normalize(sub) in item for item in checked)
        for sub in subtopics
    )


def scan_notes():
    note_files = [
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts
        and ".github" not in p.parts
        and "scripts" not in p.parts
        and p.name not in {
            "README.md", "TRACKER.md", "TODAY.md",
            "PROJECT_TASKS.md", "SKILLS.md", "PROGRESS.md"
        }
    ]

    note_texts = []
    for path in note_files:
        try:
            note_texts.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            pass

    results = {}
    for row in ROADMAP_DATA:
        results[row["id"]] = any(
            (section := section_for_topic(text, row["area"], row["topic"]))
            and explicit_done_in_section(section, row["topic"], row["subtopics"])
            for text in note_texts
        )
    return results


def current_tracker_state():
    if not TRACKER.exists():
        return {}
    text = TRACKER.read_text(encoding="utf-8", errors="ignore")
    state = {}
    for row in ROADMAP_DATA:
        pattern = re.compile(
            rf"(?im)^###\s+{re.escape(row['id'])}\b.*?\n"
            rf"(?:(?!^###\s).*\n)*?"
            rf"^- \*\*Done\?:\*\* \[(?P<mark>[ xX])\]"
        )
        m = pattern.search(text)
        if m:
            state[row["id"]] = m.group("mark").lower() == "x"
    return state


def apply_note_status():
    note_state = scan_notes()
    old_state = current_tracker_state()
    for row in ROADMAP_DATA:
        # Explicit note completion wins. Otherwise preserve the existing checkbox.
        row["done"] = note_state.get(row["id"], False) or old_state.get(row["id"], False)


def write_tracker():
    lines = [
        "# MLOps Career Tracker", "",
        "> **Source of truth:** this file contains the complete roadmap converted from the Excel tracker.",
        "> Update `Done?` manually, or let explicit completion in your notes update it.", "",
        "## Note → Tracker automation", "",
        "The generator recursively scans Markdown notes and uses regex to detect explicit completion.",
        "A note merely existing does **not** complete a roadmap item.", "",
        "Recognized patterns include:", "",
        "```text",
        "Status: Done",
        "status: completed",
        "## [x] Topic name",
        "- [x] Topic name",
        "```", "",
        "It also recognizes a topic as complete when all listed subtopics are checked in the matching note section.", "",
        "---", "",
        "## Complete Roadmap", ""
    ]
    for r in ROADMAP_DATA:
        lines += [
            f"### {r['id']} — Week {r['week']} — {r['area']} — {r['topic']}", "",
            f"- **Type:** {r['type']}",
            f"- **Done?:** [{'x' if r['done'] else ' '}]",
            f"- **Depends On:** {r['depends_on'] or 'None'}",
            f"- **Learning / Outcome:** {r['learning_outcome']}",
            "- **Subtopics to Learn:**"
        ]
        lines += [f"  - {s}" for s in r["subtopics"]]
        lines += [f"- **Project Task:** {r['project_task']}", ""]
    lines += [
        "---", "", "## Completion Rules", "",
        "- Mark Yes only when you can explain the subtopics and reproduce the task yourself.",
        "- Do not mark a task complete because GPT produced the code.",
        "- Learning flow: try first → official docs → build/debug → GPT when stuck.",
        "- Portfolio work should use public/synthetic data only.",
        "- Do not upload VECV proprietary data, code, credentials, internal architecture, or confidential information.", ""
    ]
    TRACKER.write_text("\n".join(lines), encoding="utf-8")


def progress():
    total = len(ROADMAP_DATA)
    completed = sum(r["done"] for r in ROADMAP_DATA)
    remaining = total - completed
    pct = completed / total if total else 0
    next_row = next((r for r in ROADMAP_DATA if not r["done"]), None)
    return total, completed, remaining, pct, next_row


def bar(pct, width=20):
    filled = round(pct * width)
    return "`" + "█" * filled + "░" * (width - filled) + "`"


def update_readme():
    total, completed, remaining, pct, next_row = progress()
    focus = (
        f"**Area:** {next_row['area']}  \n**Topic:** {next_row['topic']}  \n\n"
        f"**Project Task:** {next_row['project_task']}"
        if next_row else "All roadmap units are complete."
    )
    dashboard = f"""<!-- TRACKER-DASHBOARD:START -->
<!-- This section is generated by scripts/tracker.py. Remove everything between these markers to remove the dashboard. -->

## 📊 MLOps Career Tracker

| Metric | Value |
|---|---:|
| Total Units | {total} |
| Completed | {completed} |
| Remaining | {remaining} |
| Completion | {pct:.0%} |
| Current Week | {next_row['week'] if next_row else 'Complete'} |
| Next Topic | {next_row['topic'] if next_row else 'All complete'} |

**Progress:** {bar(pct)}

### Current Focus

{focus}

> Update `TRACKER.md` or complete a topic explicitly in your notes. Run `python scripts/tracker.py` to refresh this dashboard.

<!-- TRACKER-DASHBOARD:END -->"""
    text = README.read_text(encoding="utf-8", errors="ignore") if README.exists() else "# MLOps Career Tracker\n\n"
    pattern = re.compile(r"<!-- TRACKER-DASHBOARD:START -->.*?<!-- TRACKER-DASHBOARD:END -->", re.S)
    text = pattern.sub(dashboard, text, count=1) if pattern.search(text) else dashboard + "\n\n" + text.lstrip()
    README.write_text(text, encoding="utf-8")


def update_today():
    rows = [r for r in ROADMAP_DATA if not r["done"]][:12]
    lines = ["# Today", "", "> Automatically generated. Shows the first incomplete units; the full roadmap remains in `TRACKER.md`.", ""]
    if rows:
        lines += [f"- [ ] **{r['id']} — {r['area']} — {r['topic']}** — {r['project_task']}" for r in rows]
    else:
        lines.append("🎉 All roadmap units are complete.")
    TODAY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_project_tasks():
    lines = [
        "# Project Tasks", "",
        "> Automatically generated from all `Build` units.", "",
        "| ID | Week | Area | Topic | Project Task | Depends On | Done? |",
        "|---|---:|---|---|---|---|:---:|"
    ]
    for r in ROADMAP_DATA:
        if r["type"].lower() == "build":
            lines.append(
                f"| {r['id']} | {r['week']} | {r['area']} | {r['topic']} | "
                f"{r['project_task']} | {r['depends_on'] or '—'} | {'x' if r['done'] else ' '} |"
            )
    PROJECT_TASKS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_skills():
    areas = list(dict.fromkeys(r["area"] for r in ROADMAP_DATA))
    lines = [
        "# Skills Progress", "",
        "| Area | Units | Done | Progress | What this proves |",
        "|---|---:|---:|---:|---|"
    ]
    for area in areas:
        rows = [r for r in ROADMAP_DATA if r["area"] == area]
        done = sum(r["done"] for r in rows)
        pct = done / len(rows) if rows else 0
        proof = "All planned units completed" if pct == 1 else ("In progress" if done else "Not started")
        lines.append(f"| {area} | {len(rows)} | {done} | {pct:.0%} | {proof} |")
    SKILLS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    apply_note_status()
    write_tracker()
    update_readme()
    update_today()
    update_project_tasks()
    update_skills()
    total, completed, remaining, pct, next_row = progress()
    print(f"Tracker updated: {completed}/{total} complete ({pct:.0%}); {remaining} remaining.")
    if next_row:
        print(f"Next: {next_row['id']} — {next_row['area']} — {next_row['topic']}")


if __name__ == "__main__":
    main()
