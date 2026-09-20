# This class connects everything into a pipepline.

from cv_analysis.step02_profile_extractor import (extract_profile)
# from cv_analysis.step03_role_classifier import (classify_roles) 
# replaced with 
from cv_analysis.hybrid_role_recommender import recommend_roles_hybrid

from cv_analysis.step04_skill_gap_analyzer import ( analyze_skill_gap)
from cv_analysis.step05_cv_suggester import ( generate_cv_suggestions)
from cv_analysis.step06_project_suggester import ( generate_project_suggestions)
from cv_analysis.role_profiles import ROLE_PROFILES

def run_cv_analysis(cv_text: str, target_role: str | None = None) -> dict:

    #----------------------------------
    # Validation before running anything
    #----------------------------------
    if not cv_text or not cv_text.strip():
        raise ValueError( "CV text cannot be empty.")

    if target_role is not None:
        target_role = target_role.strip()

        if not target_role:
            target_role = None

    if ( target_role is not None   and target_role not in ROLE_PROFILES):
        
        supported_roles = ", ".join( ROLE_PROFILES.keys())

        raise ValueError(
            f"Unsupported target role: {target_role}. "
            f"Supported roles: {supported_roles}"
        )
        
        
    # ---------------------------------
    # Step 1: Structured extraction
    # ---------------------------------

    profile = extract_profile(cv_text)

    # ---------------------------------
    # Step 2: Role classification
    # ---------------------------------

    roles = recommend_roles_hybrid(cv_text, top_k=5)

    # ---------------------------------
    # Step 3: Choose target role
    # ---------------------------------

    if target_role:
        selected_role = target_role

    elif roles:
        selected_role = (roles[0]["role"])

    else:
        selected_role = ("Software Engineer")

    # ---------------------------------
    # Step 4: Skill gap
    # ---------------------------------

    skill_gap = analyze_skill_gap(current_skills= profile["skills"],  target_role= selected_role)

    # ---------------------------------
    # Step 5: CV suggestions
    # ---------------------------------

    suggestions = (
        generate_cv_suggestions(
            
            cv_text= cv_text,
            
            profile= profile,
            
            target_role= selected_role,
            
            missing_skills= (skill_gap["missing_skills"])
        )
    )

    # ---------------------------------
    # Step 6: Project suggestions
    # ---------------------------------

    projects = (
        generate_project_suggestions(
            current_skills= (profile["skills"]),

            missing_skills= (skill_gap["missing_skills"]),

            target_role= selected_role
        )
    )

    # ---------------------------------
    # Final result
    # ---------------------------------

    return {
        "profile": profile,

        "recommended_roles": roles,

        "selected_target_role":
            selected_role,

        "skill_gap": skill_gap,

        "cv_suggestions":
            suggestions,

        "project_suggestions":
            projects
    }