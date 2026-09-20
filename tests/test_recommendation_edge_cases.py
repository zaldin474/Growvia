from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)


def test_very_short_cv_does_not_crash():

    results = recommend_roles_hybrid(
        "Python student interested in software.",
        top_k=5
    )

    assert len(results) == 5


def test_cv_with_no_known_skills_does_not_crash():

    text = """
    Motivated student who enjoys
    solving problems, teamwork,
    learning and communication.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=5
    )

    assert len(results) == 5


def test_top_k_is_clamped():

    results = recommend_roles_hybrid(
        "Python Java SQL backend development.",
        top_k=100
    )

    # Growvia currently supports 12 roles.
    assert len(results) == 12


def test_scores_are_valid():

    results = recommend_roles_hybrid(
        """
        Built backend services using
        Python, FastAPI, PostgreSQL,
        Docker and REST APIs.
        """,
        top_k=12
    )

    for result in results:

        assert (
            0.0
            <= result["score"]
            <= 1.0
        )


def test_repeated_skills_do_not_break_ranking():

    text = """
    Python Python Python Python Python.
    FastAPI FastAPI FastAPI.
    PostgreSQL PostgreSQL.
    REST APIs.
    """

    results = recommend_roles_hybrid(
        text,
        top_k=5
    )

    assert len(results) == 5

    assert (
        results[0]["role"]
        in {
            "Backend Developer",
            "Software Engineer",
            "Full Stack Developer"
        }
    )