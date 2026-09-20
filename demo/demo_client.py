import argparse
import json
from pathlib import Path

import requests


API_URL = (
    "http://127.0.0.1:8001"
    "/analyze-cv"
)


def print_title(
    title: str
):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def analyze_cv(
    cv_path: Path,
    target_role: str | None
):

    if not cv_path.exists():

        raise FileNotFoundError(
            f"CV not found: {cv_path}"
        )


    with cv_path.open(
        "rb"
    ) as cv_file:

        files = {
            "cv": (
                cv_path.name,
                cv_file
            )
        }

        data = {}

        if target_role:

            data[
                "target_role"
            ] = target_role


        response = requests.post(
            API_URL,
            files=files,
            data=data,
            timeout=300
        )


    print_title(
        "HTTP RESPONSE"
    )

    print(
        "Status:",
        response.status_code
    )


    if response.status_code != 200:

        print(
            response.text
        )

        return


    result = response.json()


    # =====================================================
    # PROFILE
    # =====================================================

    print_title(
        "1. EXTRACTED PROFILE"
    )

    profile = result[
        "profile"
    ]

    print(
        "Skills:"
    )

    for skill in profile[
        "skills"
    ]:

        print(
            f"  - {skill}"
        )


    print()

    print(
        "Education:"
    )

    for education in profile[
        "education"
    ]:

        print(
            f"  - {education}"
        )


    # =====================================================
    # RECOMMENDED ROLES
    # =====================================================

    print_title(
        "2. CAREER RECOMMENDATIONS"
    )

    for index, role in enumerate(
        result[
            "recommended_roles"
        ],
        start=1
    ):

        print(
            f"{index}. "
            f"{role['role']}"
            f" — "
            f"{role['score']:.3f}"
        )


    # =====================================================
    # TARGET ROLE
    # =====================================================

    print_title(
        "3. SELECTED TARGET ROLE"
    )

    print(
        result[
            "selected_target_role"
        ]
    )


    # =====================================================
    # SKILL GAP
    # =====================================================

    print_title("4. CAREER SKILL GAP")

    gap = result["skill_gap"]

    print("Coverage:",f"{gap['skill_coverage']}%")

    print()

    print("Matched skills:")

    for skill in gap["matched_skills"]:

        print( f"  ✓ {skill}")


    print()

    print("Missing skills:")

    for skill in gap[ "missing_skills"]:

        print( f"  → {skill}")


    # =====================================================
    # CV FEEDBACK
    # =====================================================

    print_title("5. CV IMPROVEMENT FEEDBACK")

    suggestions = result["cv_suggestions"]

    print("Rule-based:")

    for suggestion in suggestions["rule_based"]:

        print( f"  - {suggestion}")


    print()

    print("AI feedback:")

    print(suggestions[ "ai_feedback" ])


    # =====================================================
    # PROJECT IDEAS
    # =====================================================

    print_title("6. PORTFOLIO PROJECT IDEAS")

    project_suggestions = result.get( "project_suggestions", [])

    for index, project in enumerate(project_suggestions, start=1):
        
        print( f"{index}. {project['title']}")

        print(  f"Description: " f"{project['description']}")

        technologies = ", ".join( project.get( "technologies",  [] ))

        print( f"Technologies: {technologies}")

        targeted = ", ".join( project.get( "skills_targeted",[]))

        print(f"Skills targeted: {targeted}")

        print(f"Difficulty: "f"{project.get('difficulty', 'N/A')}")

        print()

    # =====================================================
    # RAW JSON
    # =====================================================

    print_title(
        "7. RAW API RESPONSE"
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Growvia AI Demo Client"
        )
    )

    parser.add_argument(
        "cv",
        type=Path,
        help="Path to CV file"
    )

    parser.add_argument(
        "--target-role",
        default=None,
        help=(
            "Optional career target role"
        )
    )

    args = parser.parse_args()


    analyze_cv(
        cv_path=args.cv,
        target_role=args.target_role
    )


if __name__ == "__main__":

    main()  