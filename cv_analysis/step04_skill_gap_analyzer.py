'''
- This class compares extracted skills with skills typically required by a role.

Deterministic skill-gap calculations are more reliable for the moment.
'''
# *For later* (collect real job database instead of manully specifing).
# collect 100 job offers --> collect common requirments --> real skill distribution 


from .role_profiles import get_role_skills
from .skill_normalizer import normalize_skill_list



def analyze_skill_gap(current_skills: list[str]  ,  target_role: str) -> dict:

    # Normalize candidate skills first.
    candidate_skills = set( normalize_skill_list(current_skills) )

    required_skills = set( get_role_skills(target_role) )

    # -----------------------------------------
    # Unsupported role
    # -----------------------------------------

    if not required_skills:

        return {
            "target_role": target_role,
            "matched_skills": [],
            "missing_skills": [],
            "skill_coverage": 0.0
        }


    # -----------------------------------------
    # Compare candidate vs role
    # -----------------------------------------

    matched_skills = sorted( candidate_skills & required_skills)

    missing_skills = sorted( required_skills - candidate_skills)


    # -----------------------------------------
    # Coverage
    # -----------------------------------------

    coverage = ( len(matched_skills) / len(required_skills)) * 100


    return {
        "target_role": target_role,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_coverage": round( coverage,  2)
    }