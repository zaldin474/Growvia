# run 
# activate .venv
# python -m pytest tests/test_role_embeddings.py -v -s
'''Results 
tests/test_role_embeddings.py::test_role_text PASSED
tests/test_role_embeddings.py::test_candidate_text PASSED
tests/test_role_embeddings.py::test_embedding_output_structure Loading role embedding model...
modules.json: 100%|█████████████████████████████████████████████████████████████████████████████████| 349/349 [00:00<00:00, 2.15MB/s]
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
config_sentence_transformers.json: 100%|█████████████████████████████████████████████████████████████| 116/116 [00:00<00:00, 322kB/s]
README.md: 100%|████████████████████████████████████████████████████████████████████████████████| 10.5k/10.5k [00:00<00:00, 25.6MB/s]
sentence_bert_config.json: 100%|███████████████████████████████████████████████████████████████████| 53.0/53.0 [00:00<00:00, 300kB/s]
config.json: 100%|██████████████████████████████████████████████████████████████████████████████████| 612/612 [00:00<00:00, 2.01MB/s]
model.safetensors: downloading bytes: ███████████████████████████████████████████████████████████████████████████| 85.0MB, 7.17MB/s  
model.safetensors: reconstructing file: 100%|███████████████████████████████████████████████████████████| 90.9MB / 90.9MB, 8.26MB/s  
Loading weights: 100%|███████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 3392.94it/s]
tokenizer_config.json: 100%|████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 1.32MB/s]
vocab.txt: 100%|██████████████████████████████████████████████████████████████████████████████████| 232k/232k [00:00<00:00, 7.46MB/s]
tokenizer.json: 100%|█████████████████████████████████████████████████████████████████████████████| 466k/466k [00:00<00:00, 21.5MB/s]
special_tokens_map.json: 100%|███████████████████████████████████████████████████████████████████████| 112/112 [00:00<00:00, 232kB/s]
config.json: 100%|███████████████████████████████████████████████████████████████████████████████████| 190/190 [00:00<00:00, 463kB/s]
PASSED
tests/test_role_embeddings.py::test_embedding_scores_sorted PASSED
tests/test_role_embeddings.py::test_backend_embedding_top3 PASSED
tests/test_role_embeddings.py::test_ml_embedding_top3 PASSED
tests/test_role_embeddings.py::test_frontend_embedding_top3 PASSED
tests/test_role_embeddings.py::test_security_embedding_top3 PASSED
tests/test_role_embeddings.py::test_empty_cv PASSED
9 passed
'''

from cv_analysis.role_embedding_similarity import (
                                                    calculate_role_similarity,
                                                    build_role_text,
                                                    build_candidate_text
                                                )


# =========================================================
# SAMPLE PROFILES
# =========================================================

BACKEND_CV = """
Built REST APIs using Python and FastAPI.

Designed PostgreSQL databases,
implemented authentication,
CRUD operations and server-side
business logic.

Worked with Docker and Git.
"""


ML_CV = """
Used Python, pandas, NumPy,
scikit-learn and PyTorch.

Built classification models,
performed feature engineering,
model evaluation and NLP experiments.

Worked with transformer models
and machine learning pipelines.
"""


FRONTEND_CV = """
Created responsive web interfaces
with React, TypeScript,
JavaScript, HTML and CSS.

Built reusable UI components,
handled frontend state
and integrated REST APIs.
"""


SECURITY_CV = """
Performed vulnerability assessments,
network security analysis,
penetration testing and security auditing.

Worked with Linux systems,
threat detection
and incident response.
"""


# =========================================================
# ROLE TEXT
# =========================================================

def test_role_text():

    text = build_role_text("Backend Developer")

    assert "Backend Developer" in text

    assert "server" in text.lower()

    assert "rest api" in text.lower()


# =========================================================
# CANDIDATE TEXT
# =========================================================

def test_candidate_text():

    result = build_candidate_text(
        cv_text="Built backend APIs.",
        extracted_skills=[ "python", "fastapi"]
    )

    assert "python" in result
    assert "fastapi" in result
    assert "Built backend APIs." in result


# =========================================================
# OUTPUT STRUCTURE
# =========================================================

def test_embedding_output_structure():

    results = calculate_role_similarity(
        BACKEND_CV,
        extracted_skills=[
            "python",
            "fastapi",
            "postgresql",
            "rest api",
            "docker",
            "git"
        ],
        top_k=5
    )

    assert len(results) == 5

    for result in results:

        assert "role" in result

        assert ( "embedding_score" in result)

        assert isinstance( result["embedding_score"], float)


# =========================================================
# SORTING
# =========================================================

def test_embedding_scores_sorted():

    results = calculate_role_similarity(
        BACKEND_CV,
        extracted_skills=[
            "python",
            "fastapi",
            "postgresql",
            "rest api"
        ],
        top_k=5
    )

    scores = [ result["embedding_score"]  for result in results]

    assert scores == sorted(  scores, reverse=True)


# =========================================================
# BACKEND QUALITY
# =========================================================

def test_backend_embedding_top3():

    results = calculate_role_similarity(
        BACKEND_CV,
        extracted_skills=[
            "python",
            "fastapi",
            "postgresql",
            "rest api",
            "docker"
        ],
        top_k=3
    )

    predicted = { result["role"] for result in results}

    expected = {
        "Backend Developer",
        "Software Engineer",
        "Full Stack Developer"
    }

    assert predicted & expected


# =========================================================
# ML QUALITY
# =========================================================

def test_ml_embedding_top3():

    results = calculate_role_similarity(
        ML_CV,
        extracted_skills=[
            "python",
            "pandas",
            "numpy",
            "scikit-learn",
            "pytorch",
            "machine learning"
        ],
        top_k=3
    )

    predicted = { result["role"] for result in results}

    expected = {
        "Machine Learning Engineer",
        "Data Scientist"
    }

    assert predicted & expected


# =========================================================
# FRONTEND QUALITY
# =========================================================

def test_frontend_embedding_top3():

    results = calculate_role_similarity(
        FRONTEND_CV,
        extracted_skills=[
            "javascript",
            "typescript",
            "react",
            "html",
            "css"
        ],
        top_k=3
    )

    predicted = {  result["role"]  for result in results
    }

    expected = {
        "Frontend Developer",
        "Full Stack Developer"
    }

    assert predicted & expected


# =========================================================
# SECURITY QUALITY
# =========================================================

def test_security_embedding_top3():

    results = calculate_role_similarity(
        SECURITY_CV,
        extracted_skills=[
            "linux",
            "python"
        ],
        top_k=3
    )

    predicted = { result["role"]  for result in results}

    assert (  "Cybersecurity Engineer"  in predicted)


# =========================================================
# EMPTY INPUT
# =========================================================

def test_empty_cv():

    assert calculate_role_similarity(
        "",
        extracted_skills=[]
    ) == []

    assert calculate_role_similarity(
        "     ",
        extracted_skills=[]
    ) == []