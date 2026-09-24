# Project Tasks

> Automatically generated from `roadmap.json`.

| ID                         | Week | Area          | Topic                      | Project Task                                                                         | Depends On                 | Done? |
| -------------------------- | ---- | ------------- | -------------------------- | ------------------------------------------------------------------------------------ | -------------------------- | ----- |
| logs-services              | 1    | Linux         | Logs & services            | Intentionally create a failing local service and document how you diagnose it.       | processes                  |       |
| system-troubleshooting     | 2    | Linux         | System troubleshooting     | Create a troubleshooting checklist and use it against a deliberately broken service. | ssh                        |       |
| bash-automation            | 2    | Linux         | Bash automation            | Write scripts for setup, tests, and local service startup.                           | system-troubleshooting     |       |
| git-recovery               | 3    | Git           | Git recovery               | Create and recover from a deliberately bad commit.                                   | git-fundamentals-refresh   |       |
| artifact-registry          | 5    | GCP           | Artifact Registry          | Build and push the project image to Artifact Registry.                               | oidc-keyless-gcp-auth      |       |
| ml-ci-pipeline             | 10   | CI/CD         | ML CI pipeline             | Create CI pipeline for every pull request.                                           | deployment-model-loading   |       |
| container-cd               | 11   | CI/CD         | Container CD               | Automatically build and push images after approved changes.                          | model-evaluation-in-ci     |       |
| environment-separation     | 11   | CI/CD         | Environment separation     | Create environment-aware deployment configuration.                                   | container-cd               |       |
| rollback-concepts          | 11   | CI/CD         | Rollback concepts          | Demonstrate rollback to a previous application/model version.                        | environment-separation     |       |
| ci-gke                     | 16   | CI/CD         | CI → GKE                   | Automate deployment from GitHub Actions to GKE.                                      | gke-deployment             |       |
| secret-manager             | 5    | Security      | Secret Manager             | Move runtime secrets/config out of source code.                                      | artifact-registry          |       |
| security-checks            | 10   | Security      | Security checks            | Fail CI when security checks fail.                                                   | ml-ci-pipeline             |       |
| configuration              | 6    | Python        | Configuration              | Create one configuration layer used by training and API code.                        | exceptions                 |       |
| pytest                     | 6    | Testing       | pytest                     | Write tests for data validation, feature logic, and model utilities.                 | configuration              |       |
| logging                    | 6    | Quality       | Logging                    | Add consistent application/pipeline logging.                                         | pytest                     |       |
| inference-endpoints        | 7    | FastAPI       | Inference endpoints        | Build the inference API around the registered model.                                 | fastapi-fundamentals       |       |
| api-error-handling         | 7    | FastAPI       | API error handling         | Add robust API error handling and tests.                                             | inference-endpoints        |       |
| production-docker          | 7    | Docker        | Production Docker          | Harden the inference image.                                                          | docker-storage-networking  |       |
| reproducibility-metadata   | 8    | MLflow        | Reproducibility metadata   | Log complete training metadata for every run.                                        | tracking-fundamentals      |       |
| artifacts                  | 8    | MLflow        | Artifacts                  | Store model/evaluation artifacts with each run.                                      | reproducibility-metadata   |       |
| evaluation-gate            | 9    | MLflow        | Evaluation gate            | Allow promotion only when evaluation criteria pass.                                  | model-registry             |       |
| deployment-model-loading   | 9    | MLflow        | Deployment model loading   | Make the API load a controlled model version and expose its version.                 | evaluation-gate            |       |
| model-evaluation-in-ci     | 10   | ML            | Model evaluation in CI     | Run a lightweight model evaluation gate in CI.                                       | security-checks            |       |
| terraform-structure        | 12   | Terraform     | Terraform structure        | Create a clean terraform/ directory.                                                 | terraform-state            |       |
| gcp-infrastructure         | 13   | Terraform     | GCP infrastructure         | Provision the core project infrastructure with Terraform.                            | terraform-structure        |       |
| deployment-manifests       | 14   | Kubernetes    | Deployment manifests       | Create deployment + service manifests.                                               | configuration-2            |       |
| debugging                  | 15   | Kubernetes    | Debugging                  | Delete/break a pod intentionally and recover it.                                     | scaling                    |       |
| gke-deployment             | 16   | GKE           | GKE deployment             | Deploy the inference service to GKE.                                                 | debugging                  |       |
| ml-training-dag            | 17   | Airflow       | ML training DAG            | Orchestrate the end-to-end training pipeline.                                        | reliability                |       |
| application-metrics        | 18   | Monitoring    | Application metrics        | Expose the core inference metrics.                                                   | prometheus                 |       |
| grafana                    | 18   | Monitoring    | Grafana                    | Create an inference-service dashboard.                                               | application-metrics        |       |
| retraining-trigger         | 19   | ML Monitoring | Retraining trigger         | Connect drift detection to retraining.                                               | prediction-drift           |       |
| retraining-workflow        | 19   | ML Monitoring | Retraining workflow        | Implement alert → retrain → evaluate → register → deploy.                            | retraining-trigger         |       |
| failure-scenarios          | 20   | Hardening     | Failure scenarios          | Run at least five failure drills and document recovery.                              | retraining-workflow        |       |
| security-review            | 20   | Hardening     | Security review            | Review the project against a production security checklist.                          | failure-scenarios          |       |
| architecture-documentation | 20   | Portfolio     | Architecture documentation | Create final architecture diagram and README.                                        | security-review            |       |
| interview-readiness        | 20   | Portfolio     | Interview readiness        | Prepare a 10-minute live walkthrough of the entire system.                           | architecture-documentation |       |
