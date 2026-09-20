from cv_analysis.step03_role_classifier import (
    classify_roles,
    ROLE_LABELS
)

from cv_analysis.role_embedding_similarity import (
    calculate_role_similarity
)

from cv_analysis.role_profiles import (
    get_role_skills
)

from cv_analysis.skill_normalizer import (
    extract_skills
)
import math

# =========================================================
# DEFAULT WEIGHTS
#
# These are starting weights only.
# We will evaluate them before treating them as final.
# =========================================================

DEFAULT_WEIGHTS = {
    "deberta": 0.35,
    "embedding": 0.45,
    "skills": 0.20
}


# =========================================================
# NORMALIZE RELATIVE SCORES
# =========================================================

def normalize_scores(scores: dict[str, float]) -> dict[str, float]:

    if not scores:
        return {}

    values = list(scores.values())

    if not all(math.isfinite( float(value)) for value in values):
        
        raise ValueError("Scores must contain only finite values.")
        
    minimum = min(values)
    maximum = max(values)

    # If every role received exactly
    # the same score, make the signal neutral.
    if maximum == minimum:

        return {role: 0.5 for role in scores}

    return {role: (score - minimum) / (maximum - minimum) 
                  for role, score in scores.items()}


# =========================================================
# SKILL EVIDENCE
# =========================================================

def calculate_skill_evidence( candidate_skills: list[str], role: str) -> dict:

    required_skills = set( get_role_skills(role))

    candidate_set = set( candidate_skills)

    if (
        not required_skills
        or
        not candidate_set
    ):
        return {
            "score": 0.0,
            "candidate_coverage": 0.0,
            "role_coverage": 0.0,
            "matched": [],
            "required": sorted(
                required_skills
            )
        }


    matched = ( candidate_set & required_skills)


    # =====================================================
    # RECOMMENDATION SCORE
    #
    # How much of the candidate's technical evidence
    # is explained by this role?
    # =====================================================

    candidate_coverage = ( len(matched) / len(candidate_set))


    # =====================================================
    # ROLE COVERAGE
    #
    # Useful for debugging, but NOT used as the main
    # recommendation signal.
    # =====================================================

    role_coverage = ( len(matched)  / len(required_skills))


    return {
        "score": candidate_coverage,

        "candidate_coverage":  candidate_coverage,

        "role_coverage":  role_coverage,

        "matched":  sorted(matched),

        "required": sorted(required_skills)
    }


# =========================================================
# HYBRID RECOMMENDATION
# =========================================================

def recommend_roles_hybrid( cv_text: str,
                           top_k: int = 5,
                           weights: dict[str, float] | None = None,
                           include_components: bool = False
                           ) -> list[dict]:

    if not cv_text:
        return []

    if not cv_text.strip():
        return []

    if weights is None:
        weights = DEFAULT_WEIGHTS.copy()

    # -----------------------------------------------------
    # Validate / normalize weights
    # -----------------------------------------------------

    required_weight_names = {
        "deberta",
        "embedding",
        "skills"
    }

    if set(weights.keys()) != required_weight_names:

        raise ValueError(
            "Weights must contain exactly: "
            "deberta, embedding, skills"
        )

    validated_weights = {}

    for name, value in weights.items():

        if ( isinstance(value, bool)
        or
        not isinstance(value,(int, float))  ):
            
            raise ValueError(f"Weight '{name}' must be a number.")

        value = float(value)

        if not math.isfinite(value):
            
            raise ValueError(f"Weight '{name}' must be finite.")

        if value < 0:
            raise ValueError(f"Weight '{name}' cannot be negative.")

        validated_weights[name] = value


    total_weight = sum(validated_weights.values())

    if total_weight <= 0:

        raise ValueError(
        "Total recommendation weight "
        "must be greater than zero.")


    normalized_weights = {
        name: value / total_weight
        for name, value
        in validated_weights.items()
}

    # -----------------------------------------------------
    # Extract candidate skills
    # -----------------------------------------------------

    candidate_skills = extract_skills(cv_text)


    # -----------------------------------------------------
    # SIGNAL 1:
    # DeBERTa zero-shot classification
    # -----------------------------------------------------

    deberta_results = classify_roles( cv_text,  top_k=len(ROLE_LABELS))

    deberta_raw = { result["role"]: float(result["score"])
                    for result in deberta_results}

    # -----------------------------------------------------
    # SIGNAL 2:
    # Semantic embedding similarity
    # -----------------------------------------------------

    embedding_results = (calculate_role_similarity(
                                                    cv_text=cv_text,
                                                    extracted_skills=candidate_skills,
                                                    top_k=None
                                                    )
                         )

    embedding_raw = {result["role"]: float( result["embedding_score"])
                     for result in embedding_results}


    # -----------------------------------------------------
    # Normalize model scores
    #
    # The raw DeBERTa and MiniLM scales
    # are different, so directly adding
    # them would be misleading.
    # -----------------------------------------------------

    deberta_normalized = ( normalize_scores( deberta_raw))

    embedding_normalized = ( normalize_scores( embedding_raw ))


    # -----------------------------------------------------
    # SIGNAL 3:
    # Skill evidence
    # -----------------------------------------------------

    skill_results = {}

    for role in ROLE_LABELS:

        skill_results[role] = ( calculate_skill_evidence(candidate_skills,role )  )

    # -----------------------------------------------------
    # FINAL HYBRID SCORE
    # -----------------------------------------------------

    results = []

    for role in ROLE_LABELS:

        deberta_score = ( deberta_raw.get(role,  0.0 ))  # raw scores 

        embedding_score = ( embedding_normalized.get(role, 0.0) )
        
        skill_score = ( skill_results[role]["score"] )

        final_score = ( 
                       normalized_weights["deberta"] * deberta_score 
                    +
                       normalized_weights["embedding"] * embedding_score
                    +
                       normalized_weights["skills" ] * skill_score
                        )

        result = {
            "role": role,
            "score": float (final_score)
        }

        # Only expose internal scores
        # during testing/debugging.
        if include_components:

            result.update(
                {
                    "deberta_score": float( deberta_raw.get(   role,0.0  ) ),

                    "deberta_normalized": float(deberta_normalized.get(role, 0.0) ),

                    "embedding_score": float( embedding_raw.get(  role, 0.0 ) ),

                    "embedding_normalized": float(embedding_score),

                    "skill_score": float( skill_score),
                    
                    "skill_candidate_coverage": float(skill_results[role]["candidate_coverage"]),

                    "skill_role_coverage":float(skill_results[ role]["role_coverage"]),
            
                    "matched_skills": skill_results[role ]["matched"]
                }
                
                )

        results.append(
            result
        )


    # -----------------------------------------------------
    # SORT
    # -----------------------------------------------------

    results.sort(key=lambda item: item["score"],  reverse=True)


    # -----------------------------------------------------
    # TOP K SAFETY
    # -----------------------------------------------------

    top_k = max(1, min(top_k, len(results) ))

    return results[:top_k]