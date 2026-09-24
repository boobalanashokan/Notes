# Project Tasks

> Automatically generated from `roadmap.json`.

| ID  | Week | Area          | Topic                      | Project Task                                                                         | Depends On | Done? |
| --- | ---- | ------------- | -------------------------- | ------------------------------------------------------------------------------------ | ---------- | ----- |
| T4  | 1    | Linux         | Logs & services            | Intentionally create a failing local service and document how you diagnose it.       | T3         |       |
| T7  | 2    | Linux         | System troubleshooting     | Create a troubleshooting checklist and use it against a deliberately broken service. | T6         |       |
| T8  | 2    | Linux         | Bash automation            | Write scripts for setup, tests, and local service startup.                           | T7         |       |
| T14 | 3    | Git           | Git recovery               | Create and recover from a deliberately bad commit.                                   | T13        |       |
| T26 | 5    | GCP           | Artifact Registry          | Build and push the project image to Artifact Registry.                               | T25        |       |
| T27 | 5    | Security      | Secret Manager             | Move runtime secrets/config out of source code.                                      | T26        |       |
| T31 | 6    | Python        | Configuration              | Create one configuration layer used by training and API code.                        | T30        |       |
| T32 | 6    | Testing       | pytest                     | Write tests for data validation, feature logic, and model utilities.                 | T31        |       |
| T33 | 6    | Quality       | Logging                    | Add consistent application/pipeline logging.                                         | T32        |       |
| T35 | 7    | FastAPI       | Inference endpoints        | Build the inference API around the registered model.                                 | T34        |       |
| T36 | 7    | FastAPI       | API error handling         | Add robust API error handling and tests.                                             | T35        |       |
| T39 | 7    | Docker        | Production Docker          | Harden the inference image.                                                          | T38        |       |
| T41 | 8    | MLflow        | Reproducibility metadata   | Log complete training metadata for every run.                                        | T40        |       |
| T42 | 8    | MLflow        | Artifacts                  | Store model/evaluation artifacts with each run.                                      | T41        |       |
| T44 | 9    | MLflow        | Evaluation gate            | Allow promotion only when evaluation criteria pass.                                  | T43        |       |
| T45 | 9    | MLflow        | Deployment model loading   | Make the API load a controlled model version and expose its version.                 | T44        |       |
| T46 | 10   | CI/CD         | ML CI pipeline             | Create CI pipeline for every pull request.                                           | T45        |       |
| T47 | 10   | Security      | Security checks            | Fail CI when security checks fail.                                                   | T46        |       |
| T48 | 10   | ML            | Model evaluation in CI     | Run a lightweight model evaluation gate in CI.                                       | T47        |       |
| T49 | 11   | CI/CD         | Container CD               | Automatically build and push images after approved changes.                          | T48        |       |
| T50 | 11   | CI/CD         | Environment separation     | Create environment-aware deployment configuration.                                   | T49        |       |
| T51 | 11   | CI/CD         | Rollback concepts          | Demonstrate rollback to a previous application/model version.                        | T50        |       |
| T54 | 12   | Terraform     | Terraform structure        | Create a clean terraform/ directory.                                                 | T53        |       |
| T55 | 13   | Terraform     | GCP infrastructure         | Provision the core project infrastructure with Terraform.                            | T54        |       |
| T60 | 14   | Kubernetes    | Deployment manifests       | Create deployment + service manifests.                                               | T59        |       |
| T64 | 15   | Kubernetes    | Debugging                  | Delete/break a pod intentionally and recover it.                                     | T63        |       |
| T65 | 16   | GKE           | GKE deployment             | Deploy the inference service to GKE.                                                 | T64        |       |
| T66 | 16   | CI/CD         | CI → GKE                   | Automate deployment from GitHub Actions to GKE.                                      | T65        |       |
| T70 | 17   | Airflow       | ML training DAG            | Orchestrate the end-to-end training pipeline.                                        | T69        |       |
| T72 | 18   | Monitoring    | Application metrics        | Expose the core inference metrics.                                                   | T71        |       |
| T73 | 18   | Monitoring    | Grafana                    | Create an inference-service dashboard.                                               | T72        |       |
| T76 | 19   | ML Monitoring | Retraining trigger         | Connect drift detection to retraining.                                               | T75        |       |
| T77 | 19   | ML Monitoring | Retraining workflow        | Implement alert → retrain → evaluate → register → deploy.                            | T76        |       |
| T78 | 20   | Hardening     | Failure scenarios          | Run at least five failure drills and document recovery.                              | T77        |       |
| T79 | 20   | Hardening     | Security review            | Review the project against a production security checklist.                          | T78        |       |
| T80 | 20   | Portfolio     | Architecture documentation | Create final architecture diagram and README.                                        | T79        |       |
| T81 | 20   | Portfolio     | Interview readiness        | Prepare a 10-minute live walkthrough of the entire system.                           | T80        |       |
