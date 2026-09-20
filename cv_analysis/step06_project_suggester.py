from .generation_utils import ( generate_text, is_bad_generation)
from .skill_normalizer import normalize_skill_name
import re

# helper function
def build_project_suggestion( title: str, skills_targeted: list[str] | None = None, description: str = "", difficulty: str = "Intermediate", technologies: list[str] | None = None) -> dict:

    return {
        "title": title.strip(),

        "description": description.strip(),

        "technologies": (
            technologies
            if technologies
            else []
        ),

        "skills_targeted": (
            skills_targeted
            if skills_targeted
            else []
        ),

        "difficulty": difficulty
    }
    
def _split_project_values( text: str) -> list[str]:

    if not text:
        return []

    return [
        item.strip()
        for item in re.split(
            r"[,;|]",
            text
        )
        if item.strip()
    ]

def _filter_missing_skills( practiced_skills: list[str], missing_skills: list[str]) -> list[str]:
    """
    Only return skills that are actually part of
    the candidate's missing-skill list.
    """

    missing_lookup = {
        skill.lower(): skill
        for skill in missing_skills
    }

    result = []

    for skill in practiced_skills:

        key = skill.lower()

        if key in missing_lookup:

            canonical = missing_lookup[key]

            if canonical not in result:
                result.append(
                    canonical
                )

    return result

def parse_project_generation( text: str, missing_skills: list[str]) -> list[dict]:
    """
    Convert the model's formatted text output into
    structured project dictionaries.
    """

    blocks = re.split(
        r"(?m)^\s*[123][\.\)]\s+",
        text
    )

    # The first element is normally empty text
    # before "1."
    blocks = [
        block.strip()
        for block in blocks
        if block.strip()
    ]

    projects = []

    for block in blocks:

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        if not lines:
            continue

        title = lines[0]

        description = ""
        technologies = []
        practiced_skills = []
        difficulty = "Intermediate"

        for line in lines[1:]:

            lower = line.lower()

            if lower.startswith(
                "description:"
            ):
                description = line.split(
                    ":",
                    1
                )[1].strip()

            elif lower.startswith(
                "technologies:"
            ):
                value = line.split(
                    ":",
                    1
                )[1].strip()

                technologies = (
                    _split_project_values(
                        value
                    )
                )

            elif lower.startswith(
                "skills practiced:"
            ):
                value = line.split(
                    ":",
                    1
                )[1].strip()

                practiced_skills = (
                    _split_project_values(
                        value
                    )
                )

            elif lower.startswith(
                "difficulty:"
            ):
                value = line.split(
                    ":",
                    1
                )[1].strip()

                if value in {
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                }:
                    difficulty = value

        targeted = _filter_missing_skills(
            practiced_skills,
            missing_skills
        )

        # If the AI forgot or badly formatted
        # "Skills practiced", try matching the
        # technology list against missing skills.
        if not targeted:

            targeted = _filter_missing_skills(
                technologies,
                missing_skills
            )

        projects.append(
            build_project_suggestion(
                title=title,
                description=description,
                technologies=technologies,
                skills_targeted=targeted,
                difficulty=difficulty
            )
        )

    return projects

def generate_project_suggestions(target_role: str,missing_skills: list[str], current_skills: list[str] | None = None) -> list[dict]:

    current_skills = ( current_skills or [])

    current_text = (
            ", ".join(current_skills)
            if current_skills
            else "No technical skills detected"
        )

    missing_text = (
            ", ".join(missing_skills)
            if missing_skills
            else "No major missing skills detected"
        )
        

    prompt = f"""
Generate exactly 3 portfolio projects for a university student targeting {target_role}.

Current skills:
{current_text}

Skills to develop:
{missing_text}

Use exactly this format:

1. PROJECT TITLE
Description: one sentence
Technologies: comma-separated technologies
Skills practiced: comma-separated missing skills
Difficulty: Beginner, Intermediate, or Advanced

2. PROJECT TITLE
Description: one sentence
Technologies: comma-separated technologies
Skills practiced: comma-separated missing skills
Difficulty: Beginner, Intermediate, or Advanced

3. PROJECT TITLE
Description: one sentence
Technologies: comma-separated technologies
Skills practiced: comma-separated missing skills
Difficulty: Beginner, Intermediate, or Advanced

Rules:
Each project must describe a real application the student could build.
Use the student's current skills where useful.
Include missing skills where appropriate.
Use only Beginner, Intermediate, or Advanced for Difficulty.
Do not copy these instructions.
""".strip()


    try:

     generated = generate_text(
        prompt,
        max_new_tokens=220
    )

    except Exception:

     return build_project_fallback(
        target_role=target_role,
        missing_skills=missing_skills
    )


    bad_phrases = [
        "a portfolio project",
        "a description of the project",
        "technologies to learn",
        "the missing skills",
        "for each project provide",
        "create 3 concrete"
    ]


    if ( is_bad_generation(generated, minimum_words=35, forbidden_phrases=bad_phrases)
                         or
                         not is_valid_project_generation(generated)
    ):

        return build_project_fallback(
            target_role=target_role,
            missing_skills=missing_skills
        )


    projects = parse_project_generation(generated, missing_skills)

    if len(projects) != 3:

         return build_project_fallback(target_role=target_role, missing_skills=missing_skills)

    return projects
    
def build_project_fallback(target_role: str, missing_skills: list[str]) -> list[dict]:

    skills = missing_skills or []

    role_templates = {

        "Backend Developer": [
            {
                "title":
                    "Task Management REST API",

                "description":
                    "Build a backend service where users can create, "
                    "update, assign, and track tasks.",

                "technologies":
                    [
                        "FastAPI",
                        "PostgreSQL",
                        "Docker"
                    ]
            },

            {
                "title":
                    "Student Course Registration API",

                "description":
                    "Create an API for students, courses, enrollment, "
                    "authentication, and database persistence.",

                "technologies":
                    [
                        "Spring Boot",
                        "PostgreSQL",
                        "REST API"
                    ]
            },

            {
                "title":
                    "Inventory Management Service",

                "description":
                    "Develop a backend application for products, stock "
                    "changes, users, and transaction history.",

                "technologies":
                    [
                        "FastAPI",
                        "SQL",
                        "Docker"
                    ]
            }
        ],

        "Frontend Developer": [
            {
                "title":
                    "Developer Portfolio Dashboard",

                "description":
                    "Build a responsive dashboard that presents projects, "
                    "skills, statistics, and API-driven content.",

                "technologies":
                    [
                        "React",
                        "TypeScript",
                        "CSS"
                    ]
            },

            {
                "title":
                    "Job Application Tracker",

                "description":
                    "Create an interactive interface for tracking applications, "
                    "status changes, deadlines, and notes.",

                "technologies":
                    [
                        "React",
                        "TypeScript",
                        "REST API"
                    ]
            },

            {
                "title":
                    "Analytics Dashboard",

                "description":
                    "Build reusable charts, filters, tables, and responsive "
                    "components for displaying application data.",

                "technologies":
                    [
                        "React",
                        "JavaScript",
                        "CSS"
                    ]
            }
        ],

        "Machine Learning Engineer": [
            {
                "title":
                    "Resume Role Classification API",

                "description":
                    "Train and evaluate a text classifier that predicts "
                    "career-role categories from resume text.",

                "technologies":
                    [
                        "Python",
                        "scikit-learn",
                        "FastAPI"
                    ]
            },

            {
                "title":
                    "Support Ticket Classifier",

                "description":
                    "Build an NLP model that categorizes support tickets "
                    "and expose predictions through an API.",

                "technologies":
                    [
                        "Python",
                        "PyTorch",
                        "NLP"
                    ]
            },

            {
                "title":
                    "Model Evaluation Dashboard",

                "description":
                    "Train several models and compare their predictions, "
                    "metrics, and error cases.",

                "technologies":
                    [
                        "Python",
                        "pandas",
                        "scikit-learn"
                    ]
            }
        ]
    }


    projects = role_templates.get( target_role)


    if projects is None:

        primary_skills = (
            skills[:3]
            if skills
            else ["Git"]
        )

        secondary_skills = (
            skills[1:4]
            if len(skills) > 1
            else primary_skills
        )

        focused_skills = (
            skills[-3:]
            if skills
            else ["Git"]
        )

        focused_text = ", ".join(
            focused_skills
        )

        projects = [
            {
                "title":
                    f"{target_role} Portfolio Project",

                "description":
                    (
                        f"Build a practical project that demonstrates "
                        f"the core responsibilities of a "
                        f"{target_role}."
                    ),

                "technologies":
                    primary_skills
            },

            {
                "title":
                    f"End-to-End {target_role} Project",

                "description":
                    (
                        f"Complete an end-to-end project relevant to "
                        f"{target_role}, including planning, "
                        f"implementation, testing and documentation."
                    ),

                "technologies":
                    secondary_skills
            },

            {
                "title":
                    "Focused Skill Practice Project",

                "description":
                    (
                        f"Create a smaller practical project that "
                        f"uses {focused_text} in a realistic "
                        f"{target_role} scenario."
                    ),

                "technologies":
                    focused_skills
            }
        ]


    output = []

    for index, project in enumerate(
        projects,
        start=1
    ):

        technologies = project["technologies"]

        practiced = []

        missing_lookup = {
            normalize_skill_name(skill): skill
            for skill in skills
        }

        for technology in technologies:

            normalized_technology = normalize_skill_name(technology)

            if normalized_technology in missing_lookup:

                original_skill = missing_lookup[ normalized_technology]

                if original_skill not in practiced:

                    practiced.append(original_skill)

        # If the technologies didn't directly
        # overlap with the gap, distribute a
        # few missing skills to the project.
        if not practiced:

            practiced = skills[
                (index - 1) * 2:
                (index - 1) * 2 + 2
            ]

        output.append(
            build_project_suggestion(
                title=project["title"],

                description=project[ "description"],

                technologies=technologies,

                skills_targeted=practiced,

                difficulty="Intermediate"
            )
        )

    return output

def is_valid_project_generation(text: str) -> bool:

    if not text:
        return False

    lower = text.lower().strip()


    # ---------------------------------
    # Reject common prompt echoes
    # ---------------------------------

    prompt_echo_markers = [
        "create 3 portfolio project ideas",
        "create 3 concrete portfolio",
        "skills the student already has",
        "skills the student should develop",
        "a specific project title",
        "a one-sentence description",
        "which missing skills",
        "for each project provide",
        "the project helps practice"
    ]

    if any(
        marker in lower
        for marker in prompt_echo_markers
    ):
        return False


    # ---------------------------------
    # Must be substantial enough
    # ---------------------------------

    if len(text.split()) < 40:
        return False


    # ---------------------------------
    # Require three project entries
    # ---------------------------------

    project_numbers = re.findall(
        r"(?:^|\n)\s*[123][\.\)]\s+",
        text
    )

    if len(project_numbers) < 3:
        return False


    return True