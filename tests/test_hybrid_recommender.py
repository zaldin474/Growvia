# run 
# activate .venv 
# python -m pytest tests/test_hybrid_recommender.py -v -s
'''Results 
collected 10 items                                                                                                                   

tests/test_hybrid_recommender.py::test_score_normalization PASSED
tests/test_hybrid_recommender.py::test_backend_skill_evidence PASSED
tests/test_hybrid_recommender.py::test_hybrid_output_structure Loading role classification model...
Loading weights: 100%|███████████████████████████████████████████████████████████████████████████| 202/202 [00:00<00:00, 2671.19it/s]
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading role embedding model...
Loading weights: 100%|███████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 2597.17it/s]
PASSED
tests/test_hybrid_recommender.py::test_hybrid_scores_sorted PASSED
tests/test_hybrid_recommender.py::test_backend_hybrid_top3 PASSED
tests/test_hybrid_recommender.py::test_ml_hybrid_top3 PASSED
tests/test_hybrid_recommender.py::test_frontend_hybrid_top3 PASSED
tests/test_hybrid_recommender.py::test_security_hybrid_top3 PASSED
tests/test_hybrid_recommender.py::test_empty_hybrid_input PASSED
tests/test_hybrid_recommender.py::test_invalid_weights PASSED

================================================== 10 passed ===================================================
'''

import math
import pytest
from cv_analysis.hybrid_role_recommender import (
                                                recommend_roles_hybrid,
                                                calculate_skill_evidence,
                                                normalize_scores
                                                )


BACKEND_CV = """
Built REST APIs using Python and FastAPI.

Designed PostgreSQL databases,
implemented authentication,
CRUD operations and server-side systems.

Used Docker and Git.
"""


ML_CV = """
Built classification models using Python,
scikit-learn and PyTorch.

Performed feature engineering,
model evaluation, NLP,
and transformer experiments.
"""


FRONTEND_CV = """
Built responsive applications using
React, TypeScript, JavaScript,
HTML and CSS.

Created reusable UI components
and integrated REST APIs.
"""


SECURITY_CV = """
Performed vulnerability assessments,
penetration testing,
network security analysis,
security auditing,
threat detection
and incident response.

Worked extensively with Linux.
"""


# =========================================================
# SCORE NORMALIZATION
# =========================================================

def test_score_normalization():

    scores = {
        "A": 10,
        "B": 5,
        "C": 0
    }

    result = normalize_scores( scores)

    assert result["A"] == 1.0
    assert result["C"] == 0.0

    assert ( 0.0 < result["B"] < 1.0)


# =========================================================
# SKILL EVIDENCE
# =========================================================

def test_backend_skill_evidence():

    result = calculate_skill_evidence(
        [
            "python",
            "fastapi",
            "postgresql",
            "rest api",
            "docker",
            "git"
        ],
        "Backend Developer"
    )

    assert result["score"] > 0

    assert "python" in result["matched"]

    assert "fastapi" in result["matched"]


# =========================================================
# STRUCTURE
# =========================================================

def test_hybrid_output_structure():

    results = recommend_roles_hybrid( BACKEND_CV, top_k=5, include_components=True)

    assert len(results) == 5

    for result in results:

        assert "role" in result
        assert "score" in result

        assert ( "deberta_score" in result)

        assert ("embedding_score" in result)

        assert ( "skill_score" in result)


# =========================================================
# SORTING
# =========================================================

def test_hybrid_scores_sorted():

    results = recommend_roles_hybrid( BACKEND_CV, top_k=5)

    scores = [result["score"] for result in results]

    assert scores == sorted(scores, reverse=True)


# =========================================================
# BACKEND
# =========================================================

def test_backend_hybrid_top3():

    results = recommend_roles_hybrid( BACKEND_CV, top_k=3)

    predicted = { result["role"] for result in results}

    expected = {
        "Backend Developer",
        "Software Engineer",
        "Full Stack Developer"
    }

    assert predicted & expected


# =========================================================
# MACHINE LEARNING
# =========================================================

def test_ml_hybrid_top3():

    results = recommend_roles_hybrid( ML_CV, top_k=3)

    predicted = {result["role"] for result in results}

    expected = {
        "Machine Learning Engineer",
        "Data Scientist"
    }

    assert predicted & expected


# =========================================================
# FRONTEND
# =========================================================

def test_frontend_hybrid_top3():

    results = recommend_roles_hybrid( FRONTEND_CV,  top_k=3)

    predicted = { result["role"]  for result in results}

    expected = {
        "Frontend Developer",
        "Full Stack Developer"
    }

    assert predicted & expected


# =========================================================
# SECURITY
# =========================================================

def test_security_hybrid_top3():

    results = recommend_roles_hybrid(  SECURITY_CV, top_k=3)

    predicted = { result["role"] for result in results}

    assert ( "Cybersecurity Engineer" in predicted)


# =========================================================
# EMPTY INPUT
# =========================================================

def test_empty_hybrid_input():

    assert (  recommend_roles_hybrid("")  == [])

    assert ( recommend_roles_hybrid("   ") == [])


# =========================================================
# INVALID WEIGHTS
# =========================================================

def test_invalid_weights():

    try:

        recommend_roles_hybrid( BACKEND_CV, weights={ "deberta": 1.0 })

        assert False

    except ValueError:

        assert True
        
    
    
def test_data_scientist_skill_evidence_beats_analyst():

    candidate_skills = [
        "python",
        "pandas",
        "numpy",
        "scikit-learn"
    ]

    scientist = calculate_skill_evidence(
        candidate_skills,
        "Data Scientist"
    )

    analyst = calculate_skill_evidence(
        candidate_skills,
        "Data Analyst"
    )

    assert (
        scientist["score"]
        >
        analyst["score"]
    )


def test_fullstack_skill_evidence_rewards_breadth():

    candidate_skills = [
        "react",
        "typescript",
        "css",
        "python",
        "rest api",
        "git",
        "docker"
    ]

    fullstack = calculate_skill_evidence(
        candidate_skills,
        "Full Stack Developer"
    )

    frontend = calculate_skill_evidence(
        candidate_skills,
        "Frontend Developer"
    )

    assert (
        fullstack["score"]
        >
        frontend["score"]
    )
    
    
def test_negative_weight_rejected():

    with pytest.raises(
        ValueError,
        match="cannot be negative"
    ):

        recommend_roles_hybrid(
            BACKEND_CV,
            weights={
                "deberta": -1.0,
                "embedding": 1.0,
                "skills": 1.0
            }
        )


def test_nan_weight_rejected():

    with pytest.raises(
        ValueError,
        match="must be finite"
    ):

        recommend_roles_hybrid(
            BACKEND_CV,
            weights={
                "deberta":
                    float("nan"),

                "embedding":
                    1.0,

                "skills":
                    1.0
            }
        )


def test_infinite_weight_rejected():

    with pytest.raises(
        ValueError,
        match="must be finite"
    ):

        recommend_roles_hybrid(
            BACKEND_CV,
            weights={
                "deberta":
                    float("inf"),

                "embedding":
                    1.0,

                "skills":
                    1.0
            }
        )


def test_non_numeric_weight_rejected():

    with pytest.raises(
        ValueError,
        match="must be a number"
    ):

        recommend_roles_hybrid(
            BACKEND_CV,
            weights={
                "deberta":
                    "high",

                "embedding":
                    1.0,

                "skills":
                    1.0
            }
        )


def test_normalize_scores_rejects_nan():

    with pytest.raises(
        ValueError,
        match="finite"
    ):

        normalize_scores(
            {
                "A": 0.5,
                "B": math.nan
            }
        )