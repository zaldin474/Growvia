from cv_analysis.step02_profile_extractor import (
    extract_email,
    extract_phone,
    extract_skills,
    extract_profile,
    extract_education,
    extract_sections,
    extract_projects,
    extract_certifications,
    extract_languages
)

SAMPLE_CV = """
John Doe

john@example.com
+90 555 123 4567

TECHNICAL SKILLS
Python, Java, SQL, Git, Docker

PROJECTS
Built a backend REST API using Python.

EDUCATION
Bachelor in Computer Engineering
Example University
"""


def test_email():

    result = extract_email(SAMPLE_CV)

    assert result == "john@example.com"


def test_phone():

    result = extract_phone(SAMPLE_CV)

    assert result is not None

    assert "555" in result


def test_skills():

    skills = extract_skills(SAMPLE_CV)

    assert "python" in skills
    assert "java" in skills
    assert "sql" in skills
    assert "git" in skills
    assert "docker" in skills
    assert "rest api" in skills


def test_profile_structure():

    profile = extract_profile(SAMPLE_CV)

    assert "email" in profile
    assert "phone" in profile
    assert "skills" in profile
    assert "education" in profile
    assert "years_of_experience" in profile
    assert "projects" in profile
    assert "sections" in profile
    assert "word_count" in profile
    assert "certifications" in profile
    assert "languages" in profile


def test_sections():

    profile = extract_profile(SAMPLE_CV)

    assert ( profile["sections"]["projects"] is True)

    assert ( profile["sections"]["skills"] is True)

    assert ( profile["sections"]["education"] is True)
    
    
def test_education_section_only():

    text = """
    Computer Engineering Student

    SUMMARY

    Computer Engineering international student
    with strong foundations in Java,
    data structures and software development.

    EDUCATION

    TED University | 2023-2027 (Active)
    Bachelor’s in Computer Engineering

    PROJECTS

    Software Engineering Team Project (SRS & UML)
    Designed requirements and UML diagrams.

    TECHNICAL SKILLS

    Java, Python, SQL, Git
    """

    education = extract_education(
        text
    )

    assert any(
        "ted university"
        in item.lower()
        for item in education
    )

    assert any(
        "bachelor"
        in item.lower()
        and
        "computer engineering"
        in item.lower()
        for item in education
    )

    assert not any(
        item.lower()
        == "computer engineering student"
        for item in education
    )

    assert not any(
        "international student"
        in item.lower()
        for item in education
    )

    assert not any(
        "team project"
        in item.lower()
        for item in education
    )
    
    
def test_education_stops_at_projects():

    text = """
    EDUCATION

    TED University
    Bachelor of Science in Computer Engineering
    2023-2027

    PROJECTS

    Hospital Management System
    Software Engineering Team Project
    """

    education = extract_education(
        text
    )

    combined = " ".join(
        education
    ).lower()

    assert "ted university" in combined
    assert "bachelor" in combined

    assert (
        "hospital management"
        not in combined
    )

    assert (
        "team project"
        not in combined
    )
     
    
def test_education_fallback_without_heading():

    text = """
    John Doe

    Software developer interested in backend systems.

    TED University - Bachelor of Science
    in Computer Engineering, 2023-2027

    Built several Java projects.
    """

    education = extract_education(
        text
    )

    assert len(education) >= 1

    combined = " ".join(
        education
    ).lower()

    assert (
        "ted university"
        in combined
        or
        "bachelor"
        in combined
    )

    assert (
        "java projects"
        not in combined
    )
     
    
def test_project_engineering_not_education():

    text = """
    SUMMARY
    Computer Engineering Student

    PROJECTS
    Software Engineering Team Project (SRS & UML)

    Designed use cases,
    requirements and UML diagrams.
    """

    education = extract_education(
        text
    )

    assert (
        "Software Engineering Team Project (SRS & UML)"
        not in education
    )

    assert (
        "Computer Engineering Student"
        not in education
    )
    

def test_year_range_is_not_phone():

    text = """
    EDUCATION
    TED University
    2023-2027
    """

    assert extract_phone(
        text
    ) is None


def test_section_words_inside_sentences_are_not_headings():

    text = """
    John Doe

    Experienced software developer
    with strong technical skills.

    I completed several personal projects.
    """

    sections = extract_sections(
        text
    )

    assert (
        sections["experience"]
        is False
    )

    assert (
        sections["skills"]
        is False
    )


def test_real_section_heading_is_detected():

    text = """
    SUMMARY
    Software developer.

    EXPERIENCE
    Internship at Example Company.
    """

    sections = extract_sections(
        text
    )

    assert (
        sections["experience"]
        is True
    )
    
    
def test_merged_pdf_section_headings_are_detected():

    text = """
    ABOUT ME
    Computer engineering student.

    EDUCATION LANGUAGES
    Arabic (Native)
    TED University | 2023-2027 (Active)
    English (Advanced)
    Bachelor’s in Computer Engineering

    PROJECTS
    Example Project

    TECHNICAL SKILLS
    Python, Java, SQL
    """

    sections = extract_sections(
        text
    )

    assert (
        sections["education"]
        is True
    )

    assert (
        sections["projects"]
        is True
    )

    assert (
        sections["skills"]
        is True
    )
    
def test_combined_words_in_sentence_are_not_sections():

    text = """
    My education and languages helped me
    work on international software projects.
    """

    sections = extract_sections(
        text
    )

    assert (
        sections["education"]
        is False
    )

    assert (
        sections["projects"]
        is False
    )
    
def test_years_of_experience_from_explicit_statement():
    cv = """
    John Smith

    Software Engineer with 3 years of experience.

    Skills:
    Python, SQL, Git
    """

    profile = extract_profile(cv)

    assert profile["years_of_experience"] == 3.0
    
def test_years_of_experience_from_date_range():
    cv = """
    John Smith

    EXPERIENCE

    Software Engineer
    ABC Technologies
    2021 - 2024

    EDUCATION

    Example University
    2020 - 2024
    """

    profile = extract_profile(cv)

    assert profile["years_of_experience"] == 3.0
    
def test_years_of_experience_present():
    cv = """
    John Smith

    EXPERIENCE

    Software Engineer
    ABC Technologies
    2024 - Present

    EDUCATION

    Example University
    2020 - 2024
    """

    profile = extract_profile(cv)

    assert profile["years_of_experience"] is not None
    assert profile["years_of_experience"] >= 1.0
    
def test_years_of_experience_multiple_jobs():
    cv = """
    EXPERIENCE

    Software Engineer
    Company A
    2018 - 2020

    Backend Developer
    Company B
    2021 - 2024
    """

    profile = extract_profile(cv)

    assert profile["years_of_experience"] == 5.0
    
def test_education_does_not_count_as_experience():
    cv = """
    EDUCATION

    TED University
    Computer Engineering
    2023 - 2027

    PROJECTS

    Hospital Management System
    Java, SQL, UML
    """

    profile = extract_profile(cv)

    assert profile["years_of_experience"] is None
      
def test_extract_structured_project():

    text = """
    PROJECTS

    Task Management API
    Built a REST API using Python, FastAPI,
    PostgreSQL and Docker.

    EDUCATION
    Example University
    """

    projects = extract_projects(
        text
    )

    assert len(projects) == 1

    project = projects[0]

    assert (
        project["title"]
        == "Task Management API"
    )

    assert (
        "Built a REST API"
        in project["description"]
    )

    assert "python" in project["technologies"]
    assert "fastapi" in project["technologies"]
    assert "postgresql" in project["technologies"]
    assert "docker" in project["technologies"]
    assert "rest api" in project["technologies"]

def test_extract_multiple_projects():

    text = """
    PROJECTS

    Inventory Management API
    Built a backend API using Python,
    FastAPI and PostgreSQL.

    ESP32 Smart Room
    Developed an ESP32 and Arduino based
    home automation system.

    EDUCATION
    Example University
    """

    projects = extract_projects(
        text
    )

    assert len(projects) == 2

    assert (
        projects[0]["title"]
        == "Inventory Management API"
    )

    assert (
        projects[1]["title"]
        == "ESP32 Smart Room"
    )

    assert (
        "fastapi"
        in projects[0]["technologies"]
    )

    assert (
        "esp32"
        in projects[1]["technologies"]
    )

    assert (
        "arduino"
        in projects[1]["technologies"]
    )

def test_projects_stop_at_next_section():

    text = """
    PROJECTS

    Backend API
    Built using Python and FastAPI.

    EDUCATION

    Example University
    Bachelor of Computer Science
    """

    projects = extract_projects(
        text
    )

    assert len(projects) == 1

    combined = str(
        projects
    ).lower()

    assert "backend api" in combined

    assert (
        "example university"
        not in combined
    )

    assert (
        "bachelor"
        not in combined
    )

def test_no_projects_returns_empty_list():

    text = """
    EDUCATION
    Example University

    TECHNICAL SKILLS
    Python, Java, SQL
    """

    projects = extract_projects(
        text
    )

    assert projects == []

def test_project_without_explicit_title():

    text = """
    PROJECTS

    Developed a REST API using Python
    and FastAPI.
    Used PostgreSQL for data storage.

    EDUCATION
    Example University
    """

    projects = extract_projects(
        text
    )

    assert len(projects) == 1

    project = projects[0]

    # The extractor should not invent
    # a project title.
    assert project["title"] is None

    assert (
        "Developed a REST API"
        in project["description"]
    )

    assert "python" in project["technologies"]
    assert "fastapi" in project["technologies"]
    assert "postgresql" in project["technologies"]
    
    
def test_extract_certifications():

    text = """
    CERTIFICATIONS

    AWS Certified Cloud Practitioner
    Google Data Analytics Professional Certificate

    EDUCATION
    Example University
    """

    certifications = extract_certifications(
        text
    )

    assert len(certifications) == 2

    assert (
        "AWS Certified Cloud Practitioner"
        in certifications
    )

    assert (
        "Google Data Analytics Professional Certificate"
        in certifications
    )
    
def test_extract_certifications():

    text = """
    CERTIFICATIONS

    AWS Certified Cloud Practitioner
    Google Data Analytics Professional Certificate

    EDUCATION
    Example University
    """

    certifications = extract_certifications(
        text
    )

    assert len(certifications) == 2

    assert (
        "AWS Certified Cloud Practitioner"
        in certifications
    )

    assert (
        "Google Data Analytics Professional Certificate"
        in certifications
    )
    
def test_no_certifications_returns_empty_list():

    text = """
    EDUCATION
    Example University

    SKILLS
    Python
    SQL
    """

    assert (
        extract_certifications(text)
        == []
    )

def test_extract_languages():

    text = """
    LANGUAGES

    English - C1
    Turkish - B1
    Arabic - Native

    EDUCATION
    Example University
    """

    languages = extract_languages(
        text
    )

    assert len(languages) == 3

    assert "English - C1" in languages
    assert "Turkish - B1" in languages
    assert "Arabic - Native" in languages
    
def test_extract_languages_single_line():

    text = """
    LANGUAGES

    English, Turkish, Arabic

    EDUCATION
    Example University
    """

    languages = extract_languages(
        text
    )

    assert languages == [
        "English",
        "Turkish",
        "Arabic"
    ]
    
    
def test_languages_stop_at_next_section():

    text = """
    LANGUAGES

    English - C1
    Turkish - B1

    PROJECTS

    Backend API
    Built using Python and FastAPI.
    """

    languages = extract_languages(
        text
    )

    combined = " ".join(
        languages
    ).lower()

    assert "english" in combined
    assert "turkish" in combined

    assert "backend api" not in combined
    assert "fastapi" not in combined
    
    
def test_no_languages_returns_empty_list():

    text = """
    EDUCATION
    Example University

    SKILLS
    Python
    Java
    """

    assert (
        extract_languages(text)
        == []
    )
    
def test_languages_remove_duplicates():

    text = """
    LANGUAGES

    English
    Turkish
    English

    EDUCATION
    Example University
    """

    languages = extract_languages(
        text
    )

    assert languages == [
        "English",
        "Turkish"
    ]
    
def test_certifications_remove_duplicates():

    text = """
    CERTIFICATIONS

    AWS Certified Cloud Practitioner
    AWS Certified Cloud Practitioner

    EDUCATION
    Example University
    """

    certifications = extract_certifications(
        text
    )

    assert certifications == [
        "AWS Certified Cloud Practitioner"
    ]