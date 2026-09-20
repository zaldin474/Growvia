from transformers import pipeline

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


def classify_roles(cv_text: str ,  top_k: int = 5) -> list[dict]:

    classifier = get_classifier()

    # Prevent extremely long CVs from slowing
    # CPU inference.
    text = cv_text[:6000]

    result = classifier(text, candidate_labels=ROLE_LABELS, multi_label=True)

    roles = []

    for label, score in zip(result["labels"], result["scores"]): 
        
        roles.append(
            {
            "role": label,
            "score": round(float(score),4)
            }
        )

    return roles[:top_k]