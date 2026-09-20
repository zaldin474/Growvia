import pytest

from cv_analysis.step03_role_classifier import (classify_roles , ROLE_LABELS)


# =========================================================
# SAMPLE CVS
# =========================================================

BACKEND_CV = """
Backend-focused software developer.

Strong experience with Python, Java, FastAPI, REST APIs,
PostgreSQL, SQL, Docker, Git, backend architecture,
authentication, databases, and server-side development.

Built multiple REST APIs and database-driven backend systems.
"""


ML_CV = """
Machine learning engineer with experience in Python,
scikit-learn, TensorFlow, PyTorch, pandas, NumPy,
feature engineering, model training, evaluation,
natural language processing, transformers, and deep learning.

Built machine learning classification models
and deployed trained models through APIs.
"""


FRONTEND_CV = """
Frontend developer experienced with JavaScript,
TypeScript, React, HTML, CSS, responsive design,
web interfaces, user experience, and frontend development.

Built multiple interactive React web applications.
"""


DEVOPS_CV = """
DevOps engineer experienced with Docker, Kubernetes,
CI/CD pipelines, Linux, GitHub Actions, cloud deployment,
infrastructure automation, monitoring, and containerization.

Managed deployment pipelines and production infrastructure.
"""


CYBERSECURITY_CV = """
Cybersecurity specialist experienced with network security,
penetration testing, vulnerability assessment,
security monitoring, threat detection, firewalls,
incident response, and security auditing.

Performed security testing and vulnerability analysis.
"""


# =========================================================
# BASIC AI OUTPUT TEST
# =========================================================

def test_role_classifier_output_structure():

    results = classify_roles( BACKEND_CV,  top_k=5)

    assert len(results) == 5

    for result in results:

        assert "role" in result
        assert "score" in result

        assert result["role"] in ROLE_LABELS

        assert (
            0.0
            <= result["score"]
            <= 1.0
        )


# =========================================================
# CHECK SORTING
# =========================================================

def test_role_scores_are_sorted():

    results = classify_roles( BACKEND_CV, top_k=5)

    scores = [ result["score"]  for result in results ]

    assert scores == sorted( scores, reverse=True)


# =========================================================
# QUALITY TESTS
# =========================================================
#Did at least one sensible expected role appear in the model's Top 3?

@pytest.mark.parametrize( # expected Roles for each cv type
    "cv_text, expected_roles",
    [

        (
            BACKEND_CV,
            {
                "Backend Developer",
                "Software Engineer",
                "Full Stack Developer"
            }
        )
        
        ,

        (
            ML_CV,
            {
                "Machine Learning Engineer",
                "Data Scientist"
            }
        )
        
        ,

        (
            FRONTEND_CV,
            {
                "Frontend Developer",
                "Full Stack Developer"
            }
        )
        
        ,

        (
            DEVOPS_CV,
            {
                "DevOps Engineer"
            }
        )
        
        ,

        (
            CYBERSECURITY_CV,
            {
                "Cybersecurity Engineer"
            }
        )

    ]
)


def test_expected_role_appears_in_top3(cv_text, expected_roles):

    results = classify_roles(cv_text,  top_k=3)

    predicted_roles = {result["role"] for result in results}

    assert ( predicted_roles & expected_roles) , (
                                                     f"\nExpected one of: "
                                                     f"{expected_roles}\n"
                                                     f"But model predicted: "
                                                     f"{predicted_roles}"
                                                )