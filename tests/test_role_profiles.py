# to run 
# activate .venv
# python -m pytest tests/test_role_profiles.py -v
'''Results 

collected 8 items                                                                                                                    

tests/test_role_profiles.py::test_every_classifier_role_has_profile PASSED                                                     [ 12%]
tests/test_role_profiles.py::test_every_role_has_skills PASSED                                                                 [ 25%]
tests/test_role_profiles.py::test_every_role_has_description PASSED                                                            [ 37%]
tests/test_role_profiles.py::test_cybersecurity_profile_exists PASSED                                                          [ 50%]
tests/test_role_profiles.py::test_mobile_profile_exists PASSED                                                                 [ 62%]
tests/test_role_profiles.py::test_qa_profile_exists PASSED                                                                     [ 75%]
tests/test_role_profiles.py::test_role_description PASSED                                                                      [ 87%]
tests/test_role_profiles.py::test_unknown_role PASSED                                                                          [100%]

======================================================== 8 passed in 10.63s =========================================================
'''


from cv_analysis.step03_role_classifier import (ROLE_LABELS)

from cv_analysis.role_profiles import ( ROLE_PROFILES,
                                       get_role_skills,
                                       get_role_description)


# =========================================================
# EVERY AI ROLE MUST HAVE A PROFILE
# =========================================================

def test_every_classifier_role_has_profile():

    for role in ROLE_LABELS:

        assert role in ROLE_PROFILES, ( f"Missing role profile: {role}")


# =========================================================
# EVERY ROLE MUST HAVE SKILLS
# =========================================================

def test_every_role_has_skills():

    for role, profile in ROLE_PROFILES.items():

        assert "skills" in profile

        assert len( profile["skills"]) > 0, (f"{role} has no skill requirements.")


# =========================================================
# EVERY ROLE MUST HAVE DESCRIPTION
# =========================================================

def test_every_role_has_description():

    for role, profile in ROLE_PROFILES.items():

        description = profile.get("description", "")

        assert len(description.strip()) > 20 , (f"{role} has no useful description.")


# =========================================================
# SPECIFIC ROLES THAT WERE PREVIOUSLY MISSING
# =========================================================

def test_cybersecurity_profile_exists():

    skills = get_role_skills("Cybersecurity Engineer")

    assert len(skills) > 0
    assert "linux" in skills


def test_mobile_profile_exists():

    skills = get_role_skills( "Mobile Developer")

    assert len(skills) > 0
    assert "git" in skills


def test_qa_profile_exists():

    skills = get_role_skills( "QA Engineer")

    assert len(skills) > 0
    assert "git" in skills


# =========================================================
# DESCRIPTION ACCESS
# =========================================================

def test_role_description():

    description = get_role_description("Backend Developer")

    assert "server" in description.lower()
    assert "api" in description.lower()


# =========================================================
# UNKNOWN ROLE
# =========================================================

def test_unknown_role():

    assert (get_role_skills("Astronaut") == [])

    assert ( get_role_description("Astronaut") == "")