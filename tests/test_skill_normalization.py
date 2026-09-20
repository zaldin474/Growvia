# to run:
# activate .venv then 
# python -m pytest tests/test_skill_normalization.py -v

''' New Test Results

collected 19 items                                                                                                                   

tests/test_skill_normalization.py::test_cpp_and_csharp_are_not_c PASSED                                                        [  5%]
tests/test_skill_normalization.py::test_c_language PASSED                                                                      [ 10%]
tests/test_skill_normalization.py::test_javascript_alias PASSED                                                                [ 15%]
tests/test_skill_normalization.py::test_postgres_alias PASSED                                                                  [ 21%]
tests/test_skill_normalization.py::test_sklearn_alias PASSED                                                                   [ 26%]
tests/test_skill_normalization.py::test_nodejs_alias PASSED                                                                    [ 31%]
tests/test_skill_normalization.py::test_rest_aliases PASSED                                                                    [ 36%]
tests/test_skill_normalization.py::test_dotnet PASSED                                                                          [ 42%]
tests/test_skill_normalization.py::test_duplicate_aliases_produce_one_skill PASSED                                             [ 47%]
tests/test_skill_normalization.py::test_github_and_git_are_canonicalized PASSED                                                [ 52%]
tests/test_skill_normalization.py::test_spring_boot_does_not_duplicate_spring PASSED                                           [ 57%]
tests/test_skill_normalization.py::test_java_does_not_match_javascript PASSED                                                  [ 63%]
tests/test_skill_normalization.py::test_normalize_skill_name PASSED                                                            [ 68%]
tests/test_skill_normalization.py::test_normalize_skill_list PASSED                                                            [ 73%]
tests/test_skill_normalization.py::test_mixed_realistic_skill_text PASSED                                                      [ 78%]
tests/test_skill_normalization.py::test_cybersecurity_skills PASSED                                                            [ 84%]
tests/test_skill_normalization.py::test_mobile_skills PASSED                                                                   [ 89%]
tests/test_skill_normalization.py::test_qa_skills PASSED                                                                       [ 94%]
tests/test_skill_normalization.py::test_devops_skills PASSED                                                                   [100%]

======================================================== 19 passed in 0.10s =========================================================
'''

'''Old Test Results to prove it didnt break it 

collected 5 items                                                                                                                    

tests/test_profile_extractor.py::test_email PASSED                                                                             [ 20%]
tests/test_profile_extractor.py::test_phone PASSED                                                                             [ 40%]
tests/test_profile_extractor.py::test_skills PASSED                                                                            [ 60%]
tests/test_profile_extractor.py::test_profile_structure PASSED                                                                 [ 80%]
tests/test_profile_extractor.py::test_sections PASSED                                                                          [100%]

========================================================= 5 passed in 0.05s =========================================================
'''

from cv_analysis.skill_normalizer import (extract_skills,
                                          normalize_skill_name,
                                          normalize_skill_list)


# =========================================================
# C++ / C# / C
# =========================================================

def test_cpp_and_csharp_are_not_c():

    text = """Experienced with C++ and C#."""

    skills = extract_skills(text)

    assert "c++" in skills
    assert "c#" in skills

    # Important:
    # C++ / C# should not accidentally produce C.
    assert "c" not in skills


def test_c_language():

    text = """Embedded programming using C, Arduino and ESP32."""

    skills = extract_skills(text)

    assert "c" in skills
    assert "arduino" in skills
    assert "esp32" in skills


# =========================================================
# ALIASES
# =========================================================

def test_javascript_alias():

    skills = extract_skills( "Worked with JS for frontend development.")

    assert "javascript" in skills


def test_postgres_alias():

    skills = extract_skills("Built a backend using Postgres.")

    assert "postgresql" in skills


def test_sklearn_alias():

    skills = extract_skills("Built ML models with sklearn.")

    assert "scikit-learn" in skills


def test_nodejs_alias():

    skills = extract_skills( "Created APIs using NodeJS.")

    assert "node.js" in skills


def test_rest_aliases():

    text = """Designed RESTful APIs and REST services."""

    skills = extract_skills(text)

    assert "rest api" in skills


def test_dotnet():

    text = """ Developed backend applications with .NET."""

    skills = extract_skills(text)

    assert ".net" in skills


# =========================================================
# DUPLICATES
# =========================================================

def test_duplicate_aliases_produce_one_skill():

    text = """JavaScript, JS and javascript."""

    skills = extract_skills(text)

    assert skills.count("javascript") == 1


def test_github_and_git_are_canonicalized():

    text = """Used Git and GitHub for version control."""

    skills = extract_skills(text)

    assert "git" in skills

    assert skills.count("git") == 1

    assert "github" not in skills


# =========================================================
# OVERLAPPING SKILLS
# =========================================================

def test_spring_boot_does_not_duplicate_spring():

    skills = extract_skills("Developed APIs using Spring Boot.")

    assert "spring boot" in skills

    assert "spring" not in skills


def test_java_does_not_match_javascript():

    skills = extract_skills( "Experienced with JavaScript.")

    assert "javascript" in skills
    assert "java" not in skills


# =========================================================
# LIST NORMALIZATION
# =========================================================

def test_normalize_skill_name():

    assert ( normalize_skill_name("JS")== "javascript")

    assert ( normalize_skill_name("Postgres") == "postgresql")

    assert ( normalize_skill_name("C Sharp") == "c#")


def test_normalize_skill_list():

    skills = normalize_skill_list(
        [
            "JS",
            "JavaScript",
            "javascript",
            "Postgres",
            "PostgreSQL",
            "GitHub",
            "Git"
        ]
    )

    assert skills == [
        "git",
        "javascript",
        "postgresql"
    ]
    
    
def test_mixed_realistic_skill_text():

    text = """
    TECHNICAL SKILLS

    Languages:
    Python | C++ | C# | JS | TypeScript

    Frameworks:
    FastAPI, NodeJS, Spring Boot, React.js

    Databases:
    PostgreSQL / MongoDB

    Tools:
    GitHub, Docker, K8s

    AI:
    sklearn, PyTorch, NumPy

    APIs:
    RESTful APIs, GraphQL

    Other:
    .NET, Linux, OOP
    """

    skills = extract_skills(text)

    expected = {
        "python",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "fastapi",
        "node.js",
        "spring boot",
        "react",
        "postgresql",
        "mongodb",
        "git",
        "docker",
        "kubernetes",
        "scikit-learn",
        "pytorch",
        "numpy",
        "rest api",
        "graphql",
        ".net",
        "linux",
        "oop"
    }

    assert expected.issubset(set(skills))
    
#===========================    
# edge-case extraction tests
#===========================    

def test_cybersecurity_skills():

    text = """
    Performed penetration testing,
    vulnerability assessments,
    network security analysis,
    incident response using Wireshark,
    Nmap and Burp Suite.
    """

    skills = extract_skills(text)

    expected = {
        "penetration testing",
        "vulnerability assessment",
        "network security",
        "incident response",
        "wireshark",
        "nmap",
        "burp suite"
    }

    assert expected.issubset(
        set(skills)
    )


def test_mobile_skills():

    text = """
    Built Android apps using Kotlin
    and iOS applications using Swift.

    Also worked with Flutter,
    React Native and REST APIs.
    """

    skills = extract_skills(text)

    expected = {
        "android",
        "kotlin",
        "ios",
        "swift",
        "flutter",
        "react native",
        "rest api"
    }

    assert expected.issubset(
        set(skills)
    )


def test_qa_skills():

    text = """
    Created automated tests using
    Selenium and pytest.

    Performed API testing with Postman,
    regression testing and test automation.
    """

    skills = extract_skills(text)

    expected = {
        "selenium",
        "pytest",
        "api testing",
        "postman",
        "regression testing",
        "test automation"
    }

    assert expected.issubset(
        set(skills)
    )


def test_devops_skills():

    text = """
    Built CI/CD pipelines using
    GitHub Actions and Jenkins.

    Managed infrastructure with Terraform,
    Docker and Kubernetes.
    """

    skills = extract_skills(text)

    expected = {
        "ci/cd",
        "github actions",
        "jenkins",
        "terraform",
        "docker",
        "kubernetes"
    }

    assert expected.issubset(
        set(skills)
    )