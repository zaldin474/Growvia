# role
# ├── description     ← used later by embeddings
# └── skills          ← used now by skill-gap analysis



ROLE_PROFILES = {

    # =====================================================
    # SOFTWARE / WEB
    # =====================================================

    "Backend Developer": {
        "description": (
            "Develops server-side applications, REST APIs, "
            "business logic, authentication systems, databases, "
            "and backend services."
        ),
        "skills": [
            "python",
            "java",
            "sql",
            "git",
            "rest api",
            "docker",
            "fastapi",
            "spring boot",
            "postgresql"
        ]
    },

    "Frontend Developer": {
        "description": (
            "Builds responsive and interactive web interfaces "
            "using modern frontend technologies, component-based "
            "frameworks, browser APIs, and user interface design."
        ),
        "skills": [
            "javascript",
            "typescript",
            "html",
            "css",
            "react",
            "git",
            "rest api"
        ]
    },

    "Full Stack Developer": {
        "description": (
            "Develops both frontend interfaces and backend services, "
            "including APIs, databases, authentication, and complete "
            "web applications."
        ),
        "skills": [
            "javascript",
            "typescript",
            "html",
            "css",
            "react",
            "python",
            "java",
            "sql",
            "rest api",
            "git",
            "docker"
        ]
    },

    "Software Engineer": {
        "description": (
            "Designs, develops, tests, and maintains software systems "
            "using programming, object-oriented design, version control, "
            "software architecture, and engineering practices."
        ),
        "skills": [
            "python",
            "java",
            "c++",
            "c#",
            "git",
            "oop",
            "sql",
            "uml"
        ]
    },


    # =====================================================
    # AI / DATA
    # =====================================================

    "Machine Learning Engineer": {
        "description": (
            "Builds, evaluates, deploys, and maintains machine learning "
            "systems using Python, machine learning frameworks, data "
            "processing, deep learning, NLP, and model deployment."
        ),
        "skills": [
            "python",
            "machine learning",
            "scikit-learn",
            "pandas",
            "numpy",
            "pytorch",
            "tensorflow",
            "deep learning",
            "sql",
            "git"
        ]
    },

    "Data Scientist": {
        "description": (
            "Analyzes data, builds statistical and machine learning "
            "models, performs feature engineering and experimentation, "
            "and communicates insights from data."
        ),
        "skills": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "scikit-learn",
            "machine learning"
        ]
    },

    "Data Analyst": {
        "description": (
            "Collects, cleans, analyzes, and interprets structured data "
            "using SQL, spreadsheets, Python, and visualization tools "
            "to produce business insights."
        ),
        "skills": [
            "sql",
            "python",
            "pandas",
            "numpy"
        ]
    },


    # =====================================================
    # DEVOPS
    # =====================================================

    "DevOps Engineer": {
    "description": (
        "Automates software delivery, deployment, infrastructure, "
        "containers, CI/CD pipelines, monitoring, and cloud-based "
        "production environments."
    ),
    "skills": [
        "linux",
        "git",
        "docker",
        "kubernetes",
        "ci/cd",
        "github actions",
        "jenkins",
        "terraform",
        "aws",
        "azure",
        "gcp"
    ]
},


    # =====================================================
    # MOBILE
    # =====================================================

    "Mobile Developer": {
    "description": (
        "Develops Android and iOS mobile applications using native "
        "or cross-platform technologies, APIs, application architecture, "
        "and mobile user interfaces."
    ),
    "skills": [
        "java",
        "kotlin",
        "swift",
        "android",
        "ios",
        "flutter",
        "react native",
        "rest api",
        "git"
    ]
},


    # =====================================================
    # CYBERSECURITY
    # =====================================================

    "Cybersecurity Engineer": {
    "description": (
        "Protects computer systems and networks through security "
        "analysis, vulnerability assessment, penetration testing, "
        "threat detection, incident response, and secure system design."
    ),
    "skills": [
        "linux",
        "python",
        "network security",
        "penetration testing",
        "vulnerability assessment",
        "incident response",
        "siem",
        "wireshark",
        "nmap",
        "burp suite",
        "git"
    ]
},


    # =====================================================
    # EMBEDDED
    # =====================================================

    "Embedded Systems Engineer": {
        "description": (
            "Develops software that interacts directly with hardware, "
            "microcontrollers, sensors, communication protocols, and "
            "resource-constrained embedded systems."
        ),
        "skills": [
            "c",
            "c++",
            "arduino",
            "esp32",
            "linux",
            "git"
        ]
    },


    # =====================================================
    # QUALITY ASSURANCE
    # =====================================================

    "QA Engineer": {
    "description": (
        "Ensures software quality through manual and automated "
        "testing, test design, API testing, regression testing, "
        "bug reporting, and software validation."
    ),
    "skills": [
        "python",
        "java",
        "git",
        "rest api",
        "api testing",
        "test automation",
        "selenium",
        "pytest",
        "junit",
        "postman",
        "regression testing"
    ]
},
}


def get_role_profile(role: str) -> dict | None:

    return ROLE_PROFILES.get(role)


def get_role_skills(role: str) -> list[str]:

    profile = get_role_profile(role)

    if profile is None:
        return []

    return profile["skills"]


def get_role_description(role: str) -> str:

    profile = get_role_profile(role)

    if profile is None:
        return ""

    return profile["description"]