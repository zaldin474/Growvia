# Growvia AI — Outputs

## Backend Integration Test

- AI health check: **200 / healthy**
- Backend → AI request: **200**
- Response contract: all required fields present
- Integration test: **PASSED**

### Recommended roles
1. Software Engineer — 0.8651
2. Embedded Systems Engineer — 0.6640
3. Machine Learning Engineer — 0.3337
4. Backend Developer — 0.3167
5. Cybersecurity Engineer — 0.2466

### Selected target role
Backend Developer

### Skill gap
- Matched: `git`, `java`, `python`, `sql`
- Missing: `docker`, `fastapi`, `postgresql`, `rest api`, `spring boot`
- Coverage: **44.44%**

### CV feedback
Rule-based feedback correctly identified the lack of an Experience section, missing certifications, and the short CV length.

AI feedback generated three suggestions covering:
- adding relevant experience,
- expanding project descriptions,
- building backend projects around the missing skills.

### Project suggestions
The AI generated three backend-oriented projects:
- Task Management REST API
- Student Course Registration API
- Inventory Management Service

## AI Stress Test

### 12-role stress test

| Result | Role | Top-1 |
|---|---|---|
| PASS | Backend Developer | Backend Developer |
| PASS | Frontend Developer | Frontend Developer |
| PASS | Full Stack Developer | Full Stack Developer |
| PASS | Software Engineer | Software Engineer |
| PASS | Machine Learning Engineer | Machine Learning Engineer |
| CHECK | Data Scientist | Machine Learning Engineer |
| PASS | Data Analyst | Data Analyst |
| PASS | DevOps Engineer | DevOps Engineer |
| PASS | Mobile Developer | Mobile Developer |
| PASS | Cybersecurity Engineer | Cybersecurity Engineer |
| PASS | Embedded Systems Engineer | Embedded Systems Engineer |
| PASS | QA Engineer | QA Engineer |

**Results**
- Top-1: **11/12 (91.67%)**
- Top-3: **12/12 (100%)**
- Top-5: **12/12 (100%)**

The only Top-1 case requiring review is the Data Scientist profile. Machine Learning Engineer scored 0.6693 while Data Scientist scored 0.6667. Both had full skill matches for the extracted skills.

### AI stress tests

```text
9 passed, 1 warning in 33.08s
```

## Full Test Suite

```text
92 passed, 3 warnings in 25.90s
```

## Holdout Evaluation

### DeBERTa only
- Top-1: **8/12 (66.67%)**
- Top-3: **9/12 (75.00%)**
- Top-5: **10/12 (83.33%)**

### Hybrid recommender
- Top-1: **12/12 (100%)**
- Top-3: **12/12 (100%)**
- Top-5: **12/12 (100%)**

### Holdout comparison
- Top-1: **66.67% → 100%**
- Top-3: **75.00% → 100%**

> These results are from the project's synthetic/held-out evaluation cases and should not be interpreted as production-level accuracy.

## Pipeline Verification

- Profile extractor tests: **9 passed**
- Full pipeline tests: **2 passed**
- Backend integration test: **PASSED**
- AI health check: **200 / healthy**

The full pipeline successfully loads the role-classification model, embedding model, and text-generation model.

## Current Known Limitations

- `years_of_experience` is currently `null` for the demo CV.
- Education is currently represented as a simple list rather than a fully structured object.
- Projects are detected but are not yet represented as structured project objects.
- Certifications and languages are not yet fully structured.
- Project suggestions are currently returned as a long string rather than structured JSON objects.
- The Data Scientist vs Machine Learning Engineer Top-1 case needs review.
- Hugging Face authentication warnings are non-fatal.
- The Python 3.14 PyTorch warning is non-fatal but indicates possible future compatibility concerns.
