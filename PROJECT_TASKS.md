# Project Tasks

> Automatically generated from all `Build` units.

  ---------------------------------------------------------------------------------------------------
  ID              Week Area         Topic             Project Task           Depends       Done?
                                                                             On        
  -------- ----------- ------------ ----------------- ---------------------- --------- --------------
  T4                 1 Linux        Logs & services   Intentionally create a T3        
                                                      failing local service            
                                                      and document how you             
                                                      diagnose it.                     

  T7                 2 Linux        System            Create a               T6        
                                    troubleshooting   troubleshooting                  
                                                      checklist and use it             
                                                      against a deliberately           
                                                      broken service.                  

  T8                 2 Linux        Bash automation   Write scripts for      T7        
                                                      setup, tests, and                
                                                      local service startup.           

  T14                3 Git          Git recovery      Create and recover     T13       
                                                      from a deliberately              
                                                      bad commit.                      

  T26                5 GCP          Artifact Registry Build and push the     T25       
                                                      project image to                 
                                                      Artifact Registry.               

  T27                5 Security     Secret Manager    Move runtime           T26       
                                                      secrets/config out of            
                                                      source code.                     

  T31                6 Python       Configuration     Create one             T30       
                                                      configuration layer              
                                                      used by training and             
                                                      API code.                        

  T32                6 Testing      pytest            Write tests for data   T31       
                                                      validation, feature              
                                                      logic, and model                 
                                                      utilities.                       

  T33                6 Quality      Logging           Add consistent         T32       
                                                      application/pipeline             
                                                      logging.                         

  T35                7 FastAPI      Inference         Build the inference    T34       
                                    endpoints         API around the                   
                                                      registered model.                

  T36                7 FastAPI      API error         Add robust API error   T35       
                                    handling          handling and tests.              

  T39                7 Docker       Production Docker Harden the inference   T38       
                                                      image.                           

  T41                8 MLflow       Reproducibility   Log complete training  T40       
                                    metadata          metadata for every               
                                                      run.                             

  T42                8 MLflow       Artifacts         Store model/evaluation T41       
                                                      artifacts with each              
                                                      run.                             

  T44                9 MLflow       Evaluation gate   Allow promotion only   T43       
                                                      when evaluation                  
                                                      criteria pass.                   

  T45                9 MLflow       Deployment model  Make the API load a    T44       
                                    loading           controlled model                 
                                                      version and expose its           
                                                      version.                         

  T46               10 CI/CD        ML CI pipeline    Create CI pipeline for T45       
                                                      every pull request.              

  T47               10 Security     Security checks   Fail CI when security  T46       
                                                      checks fail.                     

  T48               10 ML           Model evaluation  Run a lightweight      T47       
                                    in CI             model evaluation gate            
                                                      in CI.                           

  T49               11 CI/CD        Container CD      Automatically build    T48       
                                                      and push images after            
                                                      approved changes.                

  T50               11 CI/CD        Environment       Create                 T49       
                                    separation        environment-aware                
                                                      deployment                       
                                                      configuration.                   

  T51               11 CI/CD        Rollback concepts Demonstrate rollback   T50       
                                                      to a previous                    
                                                      application/model                
                                                      version.                         

  T54               12 Terraform    Terraform         Create a clean         T53       
                                    structure         terraform/ directory.            

  T55               13 Terraform    GCP               Provision the core     T54       
                                    infrastructure    project infrastructure           
                                                      with Terraform.                  

  T60               14 Kubernetes   Deployment        Create deployment +    T59       
                                    manifests         service manifests.               

  T64               15 Kubernetes   Debugging         Delete/break a pod     T63       
                                                      intentionally and                
                                                      recover it.                      

  T65               16 GKE          GKE deployment    Deploy the inference   T64       
                                                      service to GKE.                  

  T66               16 CI/CD        CI → GKE          Automate deployment    T65       
                                                      from GitHub Actions to           
                                                      GKE.                             

  T70               17 Airflow      ML training DAG   Orchestrate the        T69       
                                                      end-to-end training              
                                                      pipeline.                        

  T72               18 Monitoring   Application       Expose the core        T71       
                                    metrics           inference metrics.               

  T73               18 Monitoring   Grafana           Create an              T72       
                                                      inference-service                
                                                      dashboard.                       

  T76               19 ML           Retraining        Connect drift          T75       
                       Monitoring   trigger           detection to                     
                                                      retraining.                      

  T77               19 ML           Retraining        Implement alert →      T76       
                       Monitoring   workflow          retrain → evaluate →             
                                                      register → deploy.               

  T78               20 Hardening    Failure scenarios Run at least five      T77       
                                                      failure drills and               
                                                      document recovery.               

  T79               20 Hardening    Security review   Review the project     T78       
                                                      against a production             
                                                      security checklist.              

  T80               20 Portfolio    Architecture      Create final           T79       
                                    documentation     architecture diagram             
                                                      and README.                      

  T81               20 Portfolio    Interview         Prepare a 10-minute    T80       
                                    readiness         live walkthrough of              
                                                      the entire system.               
  ---------------------------------------------------------------------------------------------------
