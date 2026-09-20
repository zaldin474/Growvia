Step11's purpose is:

“Can another application send a CV to my AI service over HTTP and receive a valid result?”

---
it does :       

step11                
   |              
   | HTTP request               
   v                
step09 FastAPI              
   |                
   v                
AI pipeline             
   |        
   | HTTP JSON response     
   v        
step11          

---
### Simple Flow:    

Backend     
   ↓        
HTTP POST       
   ↓        
Growvia AI FastAPI      
   ↓        
CV parsing      
   ↓        
AI pipeline     
   ↓        
JSON        
   ↓        
Backend     
---
### Flow in detail:     

User uploads CV     
      ↓     
Backend receives it     
      ↓     
Backend calls (the service):        

POST http://ai-service:8001/analyze-cv      
      ↓         
Growvia ai analyzes it              
      ↓         
Backend gets JSON             
      ↓     
Backend stores analysis         
      ↓         
Frontend gets result                

---
### Running instructions :      

in terminal 1       
first activate venv then in Growvia     
then run Ai api (step9)     
python -m uvicorn step09_api:app --reload --port 8001       

then in terminal 2      
run the simulated backend       
python step11_backend_integration_test.py       


To **`keep the services separate`** :         
- Backend      → 8000         
- Growvia AI   → 8001     

------------------
### *Example Expected result *

AI HEALTH CHECK
Status code: 200

BACKEND -> AI RESPONSE
Status code: 200

RESPONSE CONTRACT TEST

✓ profile
✓ recommended_roles
✓ selected_target_role
✓ skill_gap
✓ cv_suggestions
✓ project_suggestions

All required fields are present.

==============================
INTEGRATION TEST PASSED
==============================



-------------------
### Actual resualt


==============================
AI HEALTH CHECK
==============================
Status code: 200
Response: {'status': 'healthy'}

==============================
BACKEND -> AI RESPONSE
==============================
Status code: 200
{
    "profile": {
        "email": "zaldin474@gmail.com",
        "phone": "+90-534-258-75-53",
        "skills": [
            "arduino",
            "c",
            "git",
            "github",
            "java",
            "mysql",
            "oop",
            "python",
            "sql",
            "uml"
        ],
        "education": [
            "Computer Engineering Student",
            "Computer Engineering international student with strong foundations in Java, data",
            "TED University | 2023-2027 (Active)",
            "Bachelor’s in Computer Engineering",
            "Software Engineering Team Project (SRS & UML)"
        ],
        "years_of_experience": null,
        "sections": {
            "education": true,
            "experience": false,
            "projects": true,
            "skills": true,
            "certifications": false
        },
        "word_count": 188
    },
    "recommended_roles": [
        {
            "role": "Software Engineer",
            "score": 0.8495
        },
        {
            "role": "Embedded Systems Engineer",
            "score": 0.4401
        },
        {
            "role": "Data Analyst",
            "score": 0.1326
        },
        {
            "role": "Data Scientist",
            "score": 0.1032
        },
        {
            "role": "Frontend Developer",
            "score": 0.0984
        }
    ],
    "selected_target_role": "Backend Developer",
    "skill_gap": {
        "target_role": "Backend Developer",
        "matched_skills": [
            "git",
            "java",
            "python",
            "sql"
        ],
        "missing_skills": [
            "docker",
            "rest api"
        ],
        "skill_coverage": 66.67
    },
    "cv_suggestions": {
        "rule_based": [
            "If you have internships, volunteer work, or relevant technical experience, add an Experience section.",
            "Consider listing relevant certifications if you have completed any.",
            "The CV appears very short. Add more detail about projects, responsibilities, and technical achievements."
        ],
        "ai_feedback": "be specific"
    },
    "project_suggestions": "1. Backend Developer 2. One-sentence description 3. Docker 4. Rest API"
}

==============================
RESPONSE CONTRACT TEST
==============================
✓ profile
✓ recommended_roles
✓ selected_target_role
✓ skill_gap
✓ cv_suggestions
✓ project_suggestions

All required fields are present.

==============================
INTEGRATION TEST PASSED
==============================



---------------
#### Error codes that can occur

| Situation                         | HTTP response |
| --------------------------------- | ------------: |
| Valid CV                          |         `200` |
| Unsupported `.exe`, `.jpg`, etc.  |         `400` |
| File contains no readable text    |         `400` |
| Missing `cv` field entirely       |         `422` |
| Unexpected internal/model failure |         `500` |


##### it can be dealt with such as: 

if response.status_code == 200:     
    save_analysis()     

elif response.status_code == 400:       
    tell_user_cv_is_invalid()       

elif response.status_code == 422:       
    log_bad_request()       

else:       
    treat_as_ai_service_failure()   