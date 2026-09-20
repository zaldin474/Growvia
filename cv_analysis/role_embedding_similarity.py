from sentence_transformers import SentenceTransformer
import numpy as np

from .role_profiles import ROLE_PROFILES


# =========================================================
# MODEL
# =========================================================

EMBEDDING_MODEL_NAME = ("sentence-transformers/all-MiniLM-L6-v2")

_embedding_model = None

_role_embeddings = None
_role_names = None


# =========================================================
# LOAD MODEL
# =========================================================

def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        print("Loading role embedding model...")

        _embedding_model = ( SentenceTransformer(EMBEDDING_MODEL_NAME))

    return _embedding_model


# =========================================================
# ROLE TEXT
# =========================================================

def build_role_text(role: str) -> str:

    profile = ROLE_PROFILES[role]

    description = profile["description"]

    skills = ", ".join(profile["skills"])

    return (
        f"Role: {role}. "
        f"{description} "
        f"Relevant technical skills: {skills}."
    )


# =========================================================
# CANDIDATE TEXT
# =========================================================

def build_candidate_text(cv_text: str, extracted_skills: list[str] | None = None) -> str:

    parts = []

    if extracted_skills:

        skills = ", ".join(extracted_skills)

        parts.append(f"Technical skills: {skills}.")

    parts.append(f"Candidate CV: {cv_text}")

    return "\n".join(parts)


# =========================================================
# CACHE ROLE EMBEDDINGS
# =========================================================

def get_role_embeddings():

    global _role_embeddings
    global _role_names

    if ( _role_embeddings is not None   and   _role_names is not None):
        
        return ( _role_names, _role_embeddings)

    model = get_embedding_model()

    _role_names = list(ROLE_PROFILES.keys())

    role_texts = [build_role_text(role) for  role in _role_names]

    _role_embeddings = model.encode(role_texts,  convert_to_numpy=True, normalize_embeddings=True)

    return (_role_names, _role_embeddings)


# =========================================================
# SEMANTIC ROLE SIMILARITY
# =========================================================

def calculate_role_similarity( cv_text: str, extracted_skills: list[str] | None = None, top_k: int | None = None) -> list[dict]:

    if not cv_text:
        return []

    if not cv_text.strip():
        return []

    model = get_embedding_model()

    candidate_text = build_candidate_text( cv_text= cv_text, extracted_skills= extracted_skills)

    candidate_embedding = model.encode(
                                        candidate_text,
                                        convert_to_numpy=True,
                                        normalize_embeddings=True
                                    )

    role_names, role_embeddings = ( get_role_embeddings())

    # Because all vectors are normalized,
    # dot product == cosine similarity.
    similarities = np.dot(role_embeddings, candidate_embedding)

    results = []

    for role, similarity in zip( role_names,  similarities):

        score = float(similarity)

        results.append(
            {
                "role": role,
                "embedding_score": score
            }
        )

    results.sort( key= lambda item: item[ "embedding_score"],
                 reverse=True )

    if top_k is not None:

        top_k = max( 1,  min( top_k,len(results) ))

        results = results[:top_k]

    return results