

from fastapi.testclient import TestClient

import app.step09_api as api_module


client = TestClient(api_module.app)


# =========================================================
# FAKE AI RESPONSE
# =========================================================

FAKE_ANALYSIS_RESULT = {
    "profile": {
        "email": "john@example.com",
        "phone": "+90 555 123 4567",
        "skills": [
            "python",
            "java",
            "sql"
        ],
        
        "education": [
            "Bachelor in Computer Engineering"
        ],
        "years_of_experience": None,
        
        "projects": [
    {
        "title": "Backend API",
        "description": (
            "Built a REST API using Python."
        ),
        
        "technologies": [
            "python",
            "rest api"
        ]
    }
],
        
        "certifications": [
            "AWS Certified Cloud Practitioner"
        ],

        "languages": [
            "English - C1",
            "Turkish - B1"
        ],
        
        "sections": {
            "education": True,
            "experience": False,
            "projects": True,
            "skills": True,
            "certifications": True,
            "languages": True
        },
        "word_count": 25
    },

    "recommended_roles": [
        {
            "role": "Backend Developer",
            "score": 0.91
        },
        {
            "role": "Software Engineer",
            "score": 0.84
        }
    ],

    "selected_target_role": "Backend Developer",

    "skill_gap": {
        "target_role": "Backend Developer",
        "matched_skills": [
            "python",
            "java",
            "sql"
        ],
        "missing_skills": [
            "docker",
            "rest api",
            "git"
        ],
        "skill_coverage": 50.0
    },

    "cv_suggestions": {
        "rule_based": [
            "Add measurable achievements."
        ],
        "ai_feedback": (
            "The CV has a good technical foundation "
            "but could include stronger project impact."
        )
    },

    "project_suggestions": [
    {
        "title": "Task Management REST API",

        "description": (
            "Build a REST API using FastAPI, "
            "Docker, and PostgreSQL."
        ),

        "technologies": [
            "FastAPI",
            "PostgreSQL",
            "Docker"
        ],

        "skills_targeted": [
            "fastapi",
            "postgresql",
            "docker"
        ],

        "difficulty": "Intermediate"
    }
]
}


# =========================================================
# 1. HEALTH CHECK
# =========================================================

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {"status": "healthy"}


# =========================================================
# 2. MISSING CV
# =========================================================

def test_missing_cv():

    response = client.post("/analyze-cv")

    assert response.status_code == 422


# =========================================================
# 3. UNSUPPORTED FILE FORMAT
# =========================================================

def test_invalid_file_format():

    files = {
        "cv": (
            "resume.exe",
            b"fake executable data",
            "application/octet-stream"
        )
    }

    response = client.post("/analyze-cv", files=files)

    assert response.status_code == 400

    assert ("Unsupported CV format" in response.json()["detail"])


# =========================================================
# 4. VALID CV + TARGET ROLE
# =========================================================

def test_valid_cv_with_target_role( monkeypatch ):

    def fake_run_cv_analysis(cv_text, target_role=None):

        # Verify that the uploaded file
        # really reached the CV parser.
        assert "Python Developer" in cv_text

        # Verify that the form field
        # reached the AI pipeline.
        assert ( target_role == "Backend Developer")

        return FAKE_ANALYSIS_RESULT

    monkeypatch.setattr( api_module,"run_cv_analysis",  fake_run_cv_analysis)

    cv_text = b"""
    John Doe

    Python Developer

    john@example.com

    TECHNICAL SKILLS
    Python, Java, SQL

    PROJECTS
    Built a backend API.
    """

    files = {
        "cv": (
            "resume.txt",
            cv_text,
            "text/plain"
        )
    }

    data = {"target_role": "Backend Developer"}

    response = client.post("/analyze-cv",  files=files, data=data)

    assert response.status_code == 200

    result = response.json()

    assert (result["selected_target_role"] == "Backend Developer")

    assert ( result["profile"]["email"]  == "john@example.com")

    assert ( len(result["recommended_roles"]) == 2)
    
    assert (len(result["profile"]["projects"])== 1)

    assert ( result["profile"]["projects"][0]["title"] == "Backend API" )
    
    assert (result["profile"]["certifications"][0]== "AWS Certified Cloud Practitioner")

    assert ("English - C1"in result["profile"]["languages"])

    assert isinstance( result["project_suggestions"], list)

    assert len( result["project_suggestions"]) == 1

    project = result[ "project_suggestions"][0]

    assert ( project["title"]  == "Task Management REST API")

    assert ("FastAPI"in project["technologies"])

    assert ("fastapi" in project["skills_targeted"])

    assert ( project["difficulty"] == "Intermediate")

# =========================================================
# 5. INTERNAL AI FAILURE
# =========================================================

def test_ai_failure_returns_500( monkeypatch):

    def fake_ai_failure(
        cv_text,
        target_role=None
    ):

        raise RuntimeError(
            "SECRET INTERNAL MODEL ERROR"
        )


    monkeypatch.setattr(
        api_module,
        "run_cv_analysis",
        fake_ai_failure
    )


    files = {
        "cv": (
            "resume.txt",
            b"Valid CV content",
            "text/plain"
        )
    }


    response = client.post(
        "/analyze-cv",
        files=files
    )


    assert (
        response.status_code
        == 500
    )

    assert (
        response.json()["detail"]
        == "AI analysis failed."
    )

    assert (
        "SECRET"
        not in response.text
    )
    
def test_corrupted_pdf_returns_400():

    files = {
        "cv": (
            "resume.pdf",
            b"not really a pdf",
            "application/pdf"
        )
    }

    response = client.post(
        "/analyze-cv",
        files=files
    )

    assert response.status_code == 400

    assert (
        "could not be parsed"
        in response.json()[
            "detail"
        ].lower()
    )


def test_empty_txt_returns_400():

    files = {
        "cv": (
            "resume.txt",
            b"   \n\n   ",
            "text/plain"
        )
    }

    response = client.post(
        "/analyze-cv",
        files=files
    )

    assert response.status_code == 400


def test_unsupported_target_role_returns_400():

    files = {
        "cv": (
            "resume.txt",
            b"""
            John Doe

            TECHNICAL SKILLS
            Python, Java, SQL
            """,
            "text/plain"
        )
    }

    response = client.post(
        "/analyze-cv",

        files=files,

        data={
            "target_role":
                "Astronaut"
        }
    )

    assert response.status_code == 400

    assert (
        "Unsupported target role"
        in response.json()["detail"]
    )