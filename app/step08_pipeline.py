# This class connects everything into a pipepline.
import time

from cv_analysis.step02_profile_extractor import (extract_profile)
# from cv_analysis.step03_role_classifier import (classify_roles) 
# replaced with 
from cv_analysis.hybrid_role_recommender import recommend_roles_hybrid

from cv_analysis.step04_skill_gap_analyzer import ( analyze_skill_gap)
from cv_analysis.step05_cv_suggester import ( generate_cv_suggestions)
from cv_analysis.step06_project_suggester import ( generate_project_suggestions)
from cv_analysis.role_profiles import ROLE_PROFILES

def run_cv_analysis(
    cv_text: str,
    target_role: str | None = None
) -> dict:

    total_start = time.time()

    # ---------------------------------
    # Validation before running anything
    # ---------------------------------

    if not cv_text or not cv_text.strip():
        raise ValueError(
            "CV text cannot be empty."
        )

    if target_role is not None:
        target_role = target_role.strip()

        if not target_role:
            target_role = None

    if (
        target_role is not None
        and target_role not in ROLE_PROFILES
    ):

        supported_roles = ", ".join(
            ROLE_PROFILES.keys()
        )

        raise ValueError(
            f"Unsupported target role: {target_role}. "
            f"Supported roles: {supported_roles}"
        )

    # ---------------------------------
    # Step 1: Structured extraction
    # ---------------------------------

    stage = time.time()

    print(
        "1. Extracting profile...",
        flush=True
    )

    profile = extract_profile(
        cv_text
    )

    print(
        f"Profile finished: "
        f"{time.time() - stage:.2f}s",
        flush=True
    )

    # ---------------------------------
    # Step 2: Role classification
    # ---------------------------------

    stage = time.time()

    print(
        "2. Running role recommendations...",
        flush=True
    )

    roles = recommend_roles_hybrid(
        cv_text,
        top_k=5
    )

    print(
        f"Role recommendations finished: "
        f"{time.time() - stage:.2f}s",
        flush=True
    )

    # ---------------------------------
    # Step 3: Choose target role
    # ---------------------------------

    stage = time.time()

    print(
        "3. Selecting target role...",
        flush=True
    )

    if target_role:
        selected_role = target_role

    elif roles:
        selected_role = roles[0]["role"]

    else:
        selected_role = "Software Engineer"

    print(
        f"Target role selected: "
        f"{selected_role} "
        f"({time.time() - stage:.2f}s)",
        flush=True
    )

    # ---------------------------------
    # Step 4: Skill gap
    # ---------------------------------

    stage = time.time()

    print(
        "4. Running skill gap analysis...",
        flush=True
    )

    skill_gap = analyze_skill_gap(
        current_skills=profile["skills"],
        target_role=selected_role
    )

    print(
        f"Skill gap finished: "
        f"{time.time() - stage:.2f}s",
        flush=True
    )

    # ---------------------------------
    # Step 5: CV suggestions
    # ---------------------------------

    stage = time.time()

    print(
        "5. Generating CV suggestions...",
        flush=True
    )

    suggestions = generate_cv_suggestions(
        cv_text=cv_text,
        profile=profile,
        target_role=selected_role,
        missing_skills=(
            skill_gap["missing_skills"]
        )
    )

    print(
        f"CV suggestions finished: "
        f"{time.time() - stage:.2f}s",
        flush=True
    )

    # ---------------------------------
    # Step 6: Project suggestions
    # ---------------------------------

    stage = time.time()

    print(
        "6. Generating project suggestions...",
        flush=True
    )

    projects = generate_project_suggestions(
        current_skills=profile["skills"],
        missing_skills=(
            skill_gap["missing_skills"]
        ),
        target_role=selected_role
    )

    print(
        f"Project suggestions finished: "
        f"{time.time() - stage:.2f}s",
        flush=True
    )

    # ---------------------------------
    # Total timing
    # ---------------------------------

    print(
        f"TOTAL ANALYSIS TIME: "
        f"{time.time() - total_start:.2f}s",
        flush=True
    )

    # ---------------------------------
    # Final result
    # ---------------------------------

    return {
        "profile": profile,

        "recommended_roles": roles,

        "selected_target_role":
            selected_role,

        "skill_gap":
            skill_gap,

        "cv_suggestions":
            suggestions,

        "project_suggestions":
            projects
    }