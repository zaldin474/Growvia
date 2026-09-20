## Prototype Structure

CV PDF
   ↓
pdfplumber
   ↓
CV text
   ↓
Transformer models
   ├── Skill / category extraction
   ├── Semantic understanding
   └── Text generation
   ↓
Structured CV analysis
   ↓
Suggestions + project ideas


## local architecture

                    CV
                     │
                     ▼
                PDF Parser
                     │
                     ▼
              Extracted Text
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
   FLAN-T5                  MiniLM
 Transformers          Sentence Transformers
        │                         │
        ▼                         ▼
 CV Suggestions          Semantic Matching
 Project Ideas                  │
 Missing Skills                 ▼
                         Match Similarity





### `for me` part 

CV
 ↓
01 Parse CV
 ↓
02 Extract structured profile
 ↓
03 Predict suitable roles
 ↓
04 Detect skill gaps
 ↓
05 Generate CV suggestions
 ↓
06 Generate project suggestions
 ↓
08 Combine everything
 ↓
09 API





## Multiple systems design:

---------------------------
### CV analysis: 


#### **Flow**:

1- CV Parser
PDF/DOCX/TXT → raw text

2- Profile Extractor
Raw CV text → structured data like skills, education, experience, projects

3- Role Classifier
CV → recommended role categories **(career-role recommendation)**

4- CV Suggester
Detect weak sections and generate improvement suggestions

5- Project Suggester
Use extracted skills + missing skills + target role to suggest projects

6- Final CV Analysis Pipeline
One function/API call that runs all of the above and returns one JSON response


-----------------------






### (projected) MATCHING: 

#### Design:

Structured profile + job description
 ↓
Sentence Transformer
 ↓
Embedding similarity
 ↓
Structured matching features
 ↓
Match score

#### Flow:



### RANKING

#### Design:

Match features
 ↓
XGBoost / LightGBM
 ↓
Ranking score

#### Flow:






#### CV analysis's required Files from backend

1- CV file access (uploaded file it self or backend endpoint with the content)

like :  *GET /users/{user_id}/cv*

2- User profile data

like: GET /users/{user_id}/profile

structured fields like :
{
  "user_id": 123,
  "name": "...",
  "skills": ["Java", "Python", "SQL"],
  "education": [...],
  "experience": [...],
  "projects": [...],
  "certifications": [...],
  "languages": [...],
  "interests": [...],
  "preferred_roles": [...],
  "preferred_industries": [...]
}


3- Target role

{
  "target_role": "Data Scientist"
}


4- endpoint or service call for the ai to return results

   - such as:

   call FastApi:
   *POST /analyze-cv*

   - with:
   *user_id*
   *cv file*
   *target_role* 

   - it returns:
    {
   "profile": {...},
   "recommended_roles": [...],
   "skill_gap": {...},
   "cv_suggestions": {...},
   "project_suggestions": [...]
    }

5- database to store results instead of calculating from scratch everytime (if nothing changes).

6- Re-analysis triggers
   such as:
   user reuploads cv.
   user edits profile.
   user changes target role.
   user requests analyze another time.
   ...

7- hard constraints such as location , language, ...
 in a separate place



### what is given to backend 

AI Base URL:
http://<growvia-ai-host>:8001 (ai host hasnt been decided yet)

Health:
GET /health

CV Analysis:
POST /analyze-cv

Content-Type:
multipart/form-data


# Architicture update 18/09/2026
                         CV
                          │
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
         DeBERTa        Skills       MiniLM
            │             │             │
        NLI score     coverage      cosine score
            │             │             │
            └─────────────┼─────────────┘
                          ↓
                    Hybrid score
                          ↓
                    Ranked roles



# Full system is now roughly :
CV file
 ↓
parser
 ↓
section-aware profile extraction
 ↓
canonical skill normalization
 ↓
hybrid career-role recommender
   ├─ DeBERTa
   ├─ MiniLM embeddings
   └─ skill evidence
 ↓
career skill-gap analysis
 ↓
CV feedback
   ├─ FLAN-T5
   ├─ quality validation
   └─ deterministic fallback
 ↓
portfolio project ideas
   ├─ FLAN-T5
   ├─ structural validation
   └─ role-specific fallback
 ↓
FastAPI
 ↓
backend



# Cleaner version

CV
 ↓
Parsing
 ↓
Structured profile extraction
 ↓
Skill normalization
 ↓
Hybrid career recommendation
 ├── DeBERTa
 ├── MiniLM semantic similarity
 └── skill evidence
 ↓
Target role
 ↓
Career skill gap
 ↓
CV improvement feedback
 ├── FLAN-T5
 ├── validation
 └── deterministic fallback
 ↓
Portfolio project recommendations
 ├── FLAN-T5
 ├── structural validation
 └── role-specific fallback
 ↓
FastAPI
 ↓
Backend

## last recommendation evaluation


Original DeBERTa, 36-case benchmark:
Top-1  44.44%
Top-3  86.11%

Hybrid, 36-case development benchmark:
Top-1  97.22%
Top-3 100.00%

Fresh 12-case holdout:
DeBERTa Top-1  66.67%
Hybrid  Top-1 100.00%


# 12-role natural-language stress test

Top-1: 11/12 = 91.67%
Top-3: 12/12 = 100%
Top-5: 12/12 = 100%

Software stress tests:
9/9 passed


## bugs fixed 19/09/2026

✓ corrupt PDF/DOCX → 400 rather than 500
✓ DOCX table content is now parsed
✓ education year range no longer becomes phone number
✓ words like "experienced" no longer fake an Experience section
✓ actual section-heading detection
✓ project structural validator was wired incorrectly
✓ FLAN-T5 exceptions now fall back safely
✓ CV-feedback structural validation
✓ project-generation structural validation
✓ generic project fallback no longer leaks Backend content
✓ invalid hybrid weights rejected
✓ NaN / infinity protection
✓ internal server errors no longer exposed to API clients
✓ malformed API request coverage
✓ long/noisy/sparse CV stress testing