from cv_analysis.generation_utils import (
    is_bad_generation
)

import cv_analysis.step05_cv_suggester as feedback_module
from cv_analysis.step05_cv_suggester import (
    build_feedback_fallback,
    is_valid_feedback_generation
)

from cv_analysis.step06_project_suggester import (
    build_project_fallback,
    is_valid_project_generation
)
import cv_analysis.step06_project_suggester as project_module

def test_short_generation_is_bad():

    assert is_bad_generation(
        "be specific",
        minimum_words=10
    )

def test_prompt_echo_is_bad():

    assert is_bad_generation(
        (
            "1. a portfolio project "
            "2. a description of the project "
            "3. technologies to learn "
            "4. the missing skills"
        ),
        minimum_words=5,
        forbidden_phrases=[
            "a portfolio project"
        ]
    )

def test_good_generation_is_valid():

    text = (
        "Improve your backend project descriptions by explaining "
        "how you used Java and SQL to implement application logic."
    )

    assert not is_bad_generation(
        text,
        minimum_words=10
    )

def test_cv_feedback_fallback():

    result = build_feedback_fallback(
        profile={
            "skills": [
                "java",
                "python",
                "sql"
            ],
            "sections": {
                "experience": False,
                "certifications": False
            },
            "word_count": 188
        },
        target_role="Backend Developer",
        missing_skills=[
            "docker",
            "fastapi",
            "postgresql"
        ]
    )

    assert len(result.split()) > 20

    assert "Backend Developer" in result

    assert (
        "docker" in result.lower()
        or
        "fastapi" in result.lower()
    )

def test_backend_project_fallback():

    result = build_project_fallback(
        target_role="Backend Developer",
        missing_skills=[
            "docker",
            "fastapi",
            "postgresql",
            "rest api",
            "spring boot"
        ]
    )

    assert isinstance(result, list)
    assert len(result) == 3

    titles = [
        project["title"]
        for project in result
    ]

    assert "Task Management REST API" in titles
    assert "Student Course Registration API" in titles
    assert "Inventory Management Service" in titles

    first = result[0]

    assert "title" in first
    assert "description" in first
    assert "technologies" in first
    assert "skills_targeted" in first
    assert "difficulty" in first
    
def test_project_generator_accepts_current_skills_signature():

    import inspect

    from cv_analysis.step06_project_suggester import (
        generate_project_suggestions
    )

    parameters = inspect.signature(
        generate_project_suggestions
    ).parameters

    assert "target_role" in parameters
    assert "missing_skills" in parameters
    assert "current_skills" in parameters
    
def test_real_prompt_echo_is_invalid_project_generation():

    bad_output = (
        "Create 3 portfolio project ideas for a university student "
        "targeting the role of Backend Developer. "
        "Skills the student already has: "
        "1. A specific project title "
        "2. A one-sentence description "
        "3. Technologies to use "
        "4. Which missing skills the project helps practice"
    )

    assert not is_valid_project_generation(
        bad_output
    )
    
def test_project_fallback_has_three_projects():

    result = build_project_fallback(
        target_role="Backend Developer",
        missing_skills=[
            "docker",
            "fastapi",
            "postgresql",
            "rest api",
            "spring boot"
        ]
    )

    assert isinstance(result, list)
    assert len(result) == 3

    for project in result:

        assert isinstance(project, dict)

        assert project["title"]
        assert project["description"]

        assert isinstance(
            project["technologies"],
            list
        )

        assert isinstance(
            project["skills_targeted"],
            list
        )

        assert (
            project["difficulty"]
            in {
                "Beginner",
                "Intermediate",
                "Advanced"
            }
        )
    
def test_structurally_invalid_project_generation_uses_fallback( monkeypatch):

    bad_generation = """
    1. Inventory Application
    Description: Build a reasonably detailed inventory application
    for managing products, users, stock changes, authentication,
    database records, reporting, validation, transactions,
    searching, filtering and application settings.
    Technologies: Python, SQL, Git
    Skills practiced: application development and databases.
    """

    monkeypatch.setattr(
        project_module,
        "generate_text",
        lambda *args, **kwargs:
            bad_generation
    )

    result = (
        project_module
        .generate_project_suggestions(
            target_role="Backend Developer",
            current_skills=[
                "python",
                "sql"
            ],
            missing_skills=[
                "fastapi",
                "docker",
                "postgresql"
            ]
        )
    )

    assert isinstance(result, list)
    
    assert len(result) == 3

    assert any(project["title"]== "Task Management REST API"for project in result)

    assert ( result != bad_generation)   
    
    
    titles = [  project["title"] for project in result]

    assert "Task Management REST API" in titles
    
    assert "Student Course Registration API" in titles
    
    assert "Inventory Management Service" in titles
    
    
def test_feedback_paragraph_is_not_valid_structure():

    text = (
        "Improve the CV by adding more detail about projects and "
        "technical experience. Mention relevant technologies and "
        "describe measurable outcomes so recruiters can understand "
        "the candidate's technical abilities more clearly."
    )

    assert not is_valid_feedback_generation(
        text
    )
    
def test_feedback_paragraph_is_not_valid_structure():

    text = (
        "Improve the CV by adding more detail about projects and "
        "technical experience. Mention relevant technologies and "
        "describe measurable outcomes so recruiters can understand "
        "the candidate's technical abilities more clearly."
    )

    assert not is_valid_feedback_generation(
        text
    )
    
def test_feedback_generation_exception_uses_fallback(
    monkeypatch
):

    def fail_generation(
        *args,
        **kwargs
    ):

        raise RuntimeError(
            "model unavailable"
        )


    monkeypatch.setattr(
        feedback_module,
        "generate_text",
        fail_generation
    )


    result = (
        feedback_module
        .generate_ai_feedback(
            profile={
                "skills": [
                    "python",
                    "sql"
                ],

                "sections": {
                    "experience": False,
                    "projects": True,
                    "skills": True,
                    "certifications": False
                },

                "word_count": 150
            },

            target_role=
                "Backend Developer",

            missing_skills=[
                "docker",
                "fastapi",
                "postgresql"
            ]
        )
    )


    assert "1. " in result
    assert "2. " in result
    assert "3. " in result

    assert (
        "docker"
        in result.lower()
        or
        "fastapi"
        in result.lower()
    )
    
def test_project_generation_exception_uses_fallback( monkeypatch):

    def fail_generation(
        *args,
        **kwargs
    ):

        raise RuntimeError(
            "model unavailable"
        )


    monkeypatch.setattr(
        project_module,
        "generate_text",
        fail_generation
    )


    result = (
        project_module
        .generate_project_suggestions(
            target_role=
                "Backend Developer",

            current_skills=[
                "python",
                "sql"
            ],

            missing_skills=[
                "fastapi",
                "postgresql",
                "docker"
            ]
        )
    )


    assert isinstance(result, list)
    assert len(result) == 3

    titles = [ project["title"]for project in result]

    assert "Task Management REST API" in titles

    assert "1. " in result
    assert "2. " in result
    assert "3. " in result
    
    
def test_project_generation_exception_uses_fallback(
    monkeypatch
):

    def fail_generation(
        *args,
        **kwargs
    ):

        raise RuntimeError(
            "model unavailable"
        )


    monkeypatch.setattr(
        project_module,
        "generate_text",
        fail_generation
    )


    result = (
        project_module
        .generate_project_suggestions(
            target_role=
                "Backend Developer",

            current_skills=[
                "python",
                "sql"
            ],

            missing_skills=[
                "fastapi",
                "postgresql",
                "docker"
            ]
        )
    )


    assert isinstance(result, list)
    assert len(result) == 3

    titles = [ project["title"] for project in result]

    assert "Task Management REST API" in titles

    assert "Student Course Registration API" in titles
    assert "Inventory Management Service" in titles
