# 17/09/2026
# AI was tested at:

   - unit level
   - API level
   - model-quality level
   - pipeline level
   - HTTP integration level

Parser/Profile/Skill Gap       10 passed          
FastAPI                         5 passed         
Role Classifier                 7 passed            
Full AI Pipeline                1 passed         
----------------------------------------'        
Total                          23 passed         


## Running `Parser/Profile/Skill Gap`
activate .venv then

python -m pytest tests -v (`Runs all tests`)

---
test session starts ================================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Masters Computer\Desktop\VScode_Growvia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Masters Computer\Desktop\VScode_Growvia\Growvia
plugins: anyio-4.15.1
collected 10 items                                                                                                  

tests/test_cv_parser.py::test_txt_cv `PASSED`                                                                   [ 10%]
tests/test_cv_parser.py::test_unsupported_file `PASSED`                                                         [ 20%]
tests/test_cv_parser.py::test_empty_cv `PASSED`                                                                 [ 30%]
tests/test_cv_parser.py::test_real_pdf `PASSED`                                                                 [ 40%]

tests/test_profile_extractor.py::test_email `PASSED`                                                            [ 50%]
tests/test_profile_extractor.py::test_phone `PASSED`                                                            [ 60%]
tests/test_profile_extractor.py::test_skills `PASSED`                                                           [ 70%]
tests/test_profile_extractor.py::test_profile_structure `PASSED`                                                [ 80%]
tests/test_profile_extractor.py::test_sections `PASSED`                                                         [ 90%]

tests/test_skill_gap.py::test_backend_skill_gap `PASSED`                                                        [100%]

================================================ 10 passed in 0.25s ================================================


##### This tells us the deterministic foundation is stable.

### What was verified:  
- CV parsing      
    ✓ TXT extraction          
    ✓ PDF extraction       
    ✓ unsupported format rejection     
    ✓ empty CV rejection       

- Profile extraction      
    ✓ email        
    ✓ phone        
    ✓ skills       
    ✓ profile structure        
    ✓ section detection        

- Skill-gap logic     
    ✓ matched skills       
    ✓ missing skills       
    ✓ coverage calculation     


---


## Running `FastAPI`  
  activate .venv   then  
     python -m pytest tests/test_api.py -v (`tests only test_api.py`)

=============================================== test session starts ================================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Masters Computer\Desktop\VScode_Growvia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Masters Computer\Desktop\VScode_Growvia\Growvia
plugins: anyio-4.15.1
collected 5 items                                                                                                   

tests/test_api.py::test_health `PASSED`                                                                         [ 20%]
tests/test_api.py::test_missing_cv `PASSED`                                                                     [ 40%]
tests/test_api.py::test_invalid_file_format `PASSED`                                                            [ 60%]
tests/test_api.py::test_valid_cv_with_target_role `PASSED`                                                      [ 80%]
tests/test_api.py::test_ai_failure_returns_500 `PASSED`                                                         [100%]
========================================== 5 passed, 2 warnings in 4.63s ===========================================


##### This tells us the Api Layer is stable.



---


## Running `Role Classifier`

 activate .venv   then  
    python -m pytest tests/test_role_classifier.py -v -s

=============================================== test session starts ================================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Masters Computer\Desktop\VScode_Growvia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Masters Computer\Desktop\VScode_Growvia\Growvia
plugins: anyio-4.15.1
collected 7 items                                                                                                   

tests/test_role_classifier.py::test_role_classifier_output_structure Loading role classification model...
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|██████████████████████████████████████████████████████████| 202/202 [00:00<00:00, 2089.40it/s]
`PASSED`

tests/test_role_classifier.py::test_role_scores_are_sorted `PASSED`

tests/test_role_classifier.py::test_expected_role_appears_in_top3[\nBackend-focused software developer.\n\nStrong experience with Python, Java, FastAPI, REST APIs,\nPostgreSQL, SQL, Docker, Git, backend architecture,\nauthentication,databases, and server-side development.\n\nBuilt multiple REST APIs and database-driven backend systems.\n-expected_roles0] `PASSED`

tests/test_role_classifier.py::test_expected_role_appears_in_top3[\nMachine learning engineer with experience in Python,\nscikit-learn, TensorFlow, PyTorch, pandas, NumPy,\nfeature engineering, model training, evaluation,\nnatural language processing, transformers, and deep learning.\n\nBuilt machine learning classification models\nand deployed trained models through APIs.\n-expected_roles1] `PASSED`

tests/test_role_classifier.py::test_expected_role_appears_in_top3[\nFrontend developer experienced with JavaScript,\nTypeScript, React, HTML, CSS, responsive design,\nweb interfaces, user experience, and frontend development.\n\nBuilt multiple interactive React web applications.\n-expected_roles2] `PASSED`

tests/test_role_classifier.py::test_expected_role_appears_in_top3[\nDevOps engineer experienced with Docker, Kubernetes,\nCI/CD pipelines, Linux, GitHub Actions, cloud deployment,\ninfrastructure automation, monitoring, and containerization.\n\nManaged deployment pipelines and production infrastructure.\n-expected_roles3] `PASSED`

tests/test_role_classifier.py::test_expected_role_appears_in_top3[\nCybersecurity specialist experienced with network security,\npenetration testing, vulnerability assessment,\nsecurity monitoring, threat detection, firewalls,\nincident response, and security auditing.\n\nPerformed security testing and vulnerability analysis.\n-expected_roles4] PASSED
========================================== 7 passed, 1 warning in 19.13s ===========================================




---


## Running `Full AI Pipeline`

 activate .venv   then  
    python -m pytest tests/test_full_pipeline.py -v -s

=============================================== test session starts ================================================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Masters Computer\Desktop\VScode_Growvia\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Masters Computer\Desktop\VScode_Growvia\Growvia
plugins: anyio-4.15.1
collected 1 item                                                                                                    

tests/test_full_pipeline.py::test_full_ai_pipeline Loading role classification model...
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|██████████████████████████████████████████████████████████| 202/202 [00:00<00:00, 4121.77it/s]
Loading CV suggestion model...
Loading weights: 100%|███████████████████████████████████████████████████████████| 282/282 [00:00<00:00, 325.58it/s]
[transformers] The tied weights mapping and config for this model specifies to tie shared.weight to lm_head.weight, but both are present in the checkpoints with different values, so we will NOT tie them. You should update the config with `tie_word_embeddings=False` to silence this warning.
`PASSED`

========================================== 1 passed in 11.64s ===========================================



# 18/09/2026

72 passed