from transformers import pipeline
import time
'''
We are using zero-shot classification model,
meaning no training dataset is required initially.
'''

ROLE_LABELS = [
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Software Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "DevOps Engineer",
    "Mobile Developer",
    "Cybersecurity Engineer",
    "Embedded Systems Engineer",
    "QA Engineer"
]

MODEL_NAME =  (
    "MoritzLaurer/"
    "DeBERTa-v3-xsmall-mnli-fever-anli-ling-binary"
)

_classifier = None


def get_classifier():
    global _classifier

    if _classifier is None: # creates a classifier if none exists.
        print("Loading role classification model...")

        _classifier = pipeline( task="zero-shot-classification"
                                ,
                                model=MODEL_NAME
                                ,
                                device=-1
                                 )

    return _classifier


def classify_roles( cv_text: str, top_k: int = 5, candidate_labels: list[str] | None = None) -> list[dict]:

    classifier = get_classifier()

    # If no shortlist was supplied, preserve
    # the original behavior and evaluate all roles.
    labels = (
        candidate_labels
        if candidate_labels is not None
        else ROLE_LABELS
    )

    if not labels:
        return []

    # Safety: only allow roles that actually exist
    # in Growvia's role list.
    invalid_labels = [
        role
        for role in labels
        if role not in ROLE_LABELS
    ]

    if invalid_labels:
        raise ValueError(
            f"Unsupported candidate roles: "
            f"{invalid_labels}"
        )

    # Prevent extremely long CVs from slowing
    # CPU inference.
    text = cv_text[:6000]

    inference_start = time.time()

    print(
        f"Starting DeBERTa inference for "
        f"{len(labels)} candidate roles...",
        flush=True
    )

    result = classifier(
        text,
        candidate_labels=labels,
        multi_label=True
    )

    print(
        f"DeBERTa inference completed in "
        f"{time.time() - inference_start:.2f}s",
        flush=True
    )

    roles = []

    for label, score in zip( result["labels"], result["scores"]):

        roles.append(
            {
                "role": label,
                "score": round( float(score), 4)
                }
        )

    top_k = max(1, min( top_k,len(roles)))

    return roles[:top_k]