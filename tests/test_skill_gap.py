# to run
# activate .venv
# python -m pytest tests/test_skill_gap.py -v
'''Results 

collected 4 items                                                                                                                    

tests/test_skill_gap.py::test_backend_skill_gap PASSED                                                                         [ 25%]
tests/test_skill_gap.py::test_cybersecurity_role_no_longer_returns_empty PASSED                                                [ 50%]
tests/test_skill_gap.py::test_mobile_role_no_longer_returns_empty PASSED                                                       [ 75%]
tests/test_skill_gap.py::test_qa_role_no_longer_returns_empty PASSED                                                           [100%]

========================================================= 4 passed in 0.04s =========================================================
'''

from cv_analysis.step04_skill_gap_analyzer import (
    analyze_skill_gap
)
# Does the system correctly classify known candidate skills as matched and known absent skills as missing

def test_backend_skill_gap():

    current_skills = [
        "python",
        "java",
        "sql",
        "git"
    ]

    result = analyze_skill_gap( current_skills=current_skills,   target_role="Backend Developer")

    assert (  result["target_role"] == "Backend Developer")

    for skill in [
        "python",
        "java",
        "sql",
        "git"
    ]:

        assert skill in result[ "matched_skills"]

    assert ("docker"in result["missing_skills"])

    assert ( "rest api"in result["missing_skills"])

    assert (0 < result["skill_coverage"]< 100)
    
    
def test_cybersecurity_role_no_longer_returns_empty():

    result = analyze_skill_gap(
        current_skills=[
            "python",
            "linux"
        ],
        target_role="Cybersecurity Engineer"
    )

    assert len(result["matched_skills"]) > 0

    assert ( result["skill_coverage"] > 0)


def test_mobile_role_no_longer_returns_empty():

    result = analyze_skill_gap(
        current_skills=[
            "java",
            "git"
        ],
        target_role="Mobile Developer"
    )

    assert len( result["matched_skills"]) > 0


def test_qa_role_no_longer_returns_empty():

    result = analyze_skill_gap(
        current_skills=[
            "python",
            "git",
            "rest api"
        ],
        target_role="QA Engineer"
    )

    assert len(result["matched_skills"]) > 0