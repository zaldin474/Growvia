from app.step08_pipeline import run_cv_analysis

import pytest





SAMPLE_CV = """
John Doe
john@example.com
+90 555 123 4567

EDUCATION
Bachelor of Science in Computer Engineering

TECHNICAL SKILLS
Python, Java, SQL, Git, Docker, FastAPI

PROJECTS
Developed a REST API using Python and FastAPI.
Designed a PostgreSQL database and implemented CRUD operations.
Used Git for version control and Docker for containerization.

EXPERIENCE
Worked on server-side software projects and database-driven
applications.
"""
def test_unsupported_target_role_rejected():

    with pytest.raises(
        ValueError,
        match="Unsupported target role"):
        run_cv_analysis( cv_text="Python Java SQL", target_role="Astronaut")

def test_full_ai_pipeline():

    result = run_cv_analysis(cv_text=SAMPLE_CV,target_role="Backend Developer")

    # -----------------------------------------
    # Main response structure
    # -----------------------------------------

    required_fields = [
        "profile",
        "recommended_roles",
        "selected_target_role",
        "skill_gap",
        "cv_suggestions",
        "project_suggestions"
    ]

    for field in required_fields:
        assert field in result


    # -----------------------------------------
    # Profile
    # -----------------------------------------

    profile = result["profile"]

    assert profile["email"] == "john@example.com"

    assert "python" in profile["skills"]
    assert "java" in profile["skills"]
    assert "sql" in profile["skills"]


    # -----------------------------------------
    # Role recommendation
    # -----------------------------------------

    roles = result["recommended_roles"]

    assert len(roles) > 0

    for role in roles:
        assert "role" in role
        assert "score" in role


    # -----------------------------------------
    # Explicit target role
    # -----------------------------------------

    assert (result["selected_target_role"] == "Backend Developer")


    # -----------------------------------------
    # Skill gap
    # -----------------------------------------

    skill_gap = result["skill_gap"]

    assert (skill_gap["target_role"] == "Backend Developer")

    assert "matched_skills" in skill_gap
    assert "missing_skills" in skill_gap
    assert "skill_coverage" in skill_gap


    # -----------------------------------------
    # CV suggestions
    # -----------------------------------------

    suggestions = result["cv_suggestions"]

    assert suggestions is not None


    # -----------------------------------------
    # Project suggestions
    # -----------------------------------------

    project_suggestions = (result["project_suggestions"])

    assert project_suggestions is not None

    assert len(str(project_suggestions).strip()) > 0