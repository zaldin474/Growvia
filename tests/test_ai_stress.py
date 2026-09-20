import math

from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)

from cv_analysis.step03_role_classifier import (
    ROLE_LABELS
)


# =========================================================
# GENERAL OUTPUT INVARIANTS
# =========================================================

def test_all_roles_returned_once():

    text = """
    Computer engineering student with experience
    in Python, Java, SQL, Git, Docker, React,
    Linux and software projects.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=100
    )

    roles = [
        result["role"]
        for result in results
    ]

    assert len(results) == len(
        ROLE_LABELS
    )

    assert len(roles) == len(
        set(roles)
    )

    assert set(roles) == set(
        ROLE_LABELS
    )


def test_all_scores_are_finite():

    text = """
    Built applications using Python,
    Java, SQL, Docker and Git.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=100,
        include_components=True
    )

    numeric_fields = [
        "score",
        "deberta_score",
        "deberta_normalized",
        "embedding_score",
        "embedding_normalized",
        "skill_score",
        "skill_candidate_coverage",
        "skill_role_coverage"
    ]

    for result in results:

        for field in numeric_fields:

            value = result[field]

            assert math.isfinite(
                value
            ), (
                f"{field} is not finite "
                f"for {result['role']}: "
                f"{value}"
            )


def test_final_scores_are_between_zero_and_one():

    text = """
    Python Java C++ SQL React Docker
    Kubernetes machine learning
    Linux Git.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=100
    )

    for result in results:

        assert (
            0.0
            <= result["score"]
            <= 1.0
        )


def test_scores_are_monotonically_sorted():

    text = """
    Built web applications,
    APIs and database systems
    using Python, SQL and React.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=100
    )

    scores = [
        result["score"]
        for result in results
    ]

    assert scores == sorted(
        scores,
        reverse=True
    )
    
# =========================================================
# SPARSE / STRANGE INPUT
# =========================================================

def test_no_known_skills_still_returns_valid_results():

    text = """
    Motivated university student.

    Enjoys teamwork, communication,
    problem solving, presentations
    and learning new concepts.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=5
    )

    assert len(results) == 5

    for result in results:

        assert math.isfinite(
            result["score"]
        )


def test_no_section_headings_does_not_break_recommender():

    text = """
    I built several applications using
    Python and Java.

    I used SQL for storing data
    and Git for version control.

    I also developed REST APIs
    and used Docker.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=5
    )

    assert len(results) == 5

    roles = {
        item["role"]
        for item in results
    }

    assert (
        "Backend Developer"
        in roles
        or
        "Software Engineer"
        in roles
    )


def test_large_cv_does_not_crash():

    normal_content = """
    Developed backend applications using
    Python, FastAPI, SQL, PostgreSQL,
    REST APIs, Docker and Git.

    Implemented authentication,
    database operations,
    validation and server-side logic.
    """

    noise = (
        """
        Participated in university activities,
        coursework, presentations, teamwork,
        documentation and technical research.
        """
        * 300
    )

    text = (
        normal_content
        + noise
    )

    results = recommend_roles_hybrid(
        text,
        top_k=5
    )

    assert len(results) == 5

    assert all(
        math.isfinite(
            result["score"]
        )
        for result in results
    )


def test_heavily_repeated_skills_do_not_create_invalid_scores():

    text = (
        "Python FastAPI PostgreSQL Docker REST API "
        * 300
    )

    results = recommend_roles_hybrid(
        text,
        top_k=5
    )

    assert len(results) == 5

    assert all(
        math.isfinite(
            result["score"]
        )
        for result in results
    )
    
# =========================================================
# MIXED ROLE PROFILE
# =========================================================

def test_mixed_frontend_backend_profile_is_reasonable():

    text = """
    Built React and TypeScript interfaces
    using HTML and CSS.

    Developed REST APIs with Python
    and FastAPI.

    Stored application data in PostgreSQL
    and containerized the application
    using Docker.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=5
    )

    predicted = {
        result["role"]
        for result in results[:3]
    }

    acceptable = {
        "Full Stack Developer",
        "Backend Developer",
        "Frontend Developer"
    }

    assert predicted & acceptable