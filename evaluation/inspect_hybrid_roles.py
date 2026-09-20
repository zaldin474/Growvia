# run
# activate .venv
# python -m evaluation.inspect_hybrid_roles
'''Results
==========================================================================================
Backend
==========================================================================================
1. Backend Developer            Final=0.6664 | DeBERTa=0.2374 | Embedding=1.0000 | Skills=0.6667
   Matched: ['docker', 'fastapi', 'git', 'postgresql', 'python', 'rest api']
2. DevOps Engineer              Final=0.5240 | DeBERTa=1.0000 | Embedding=0.2597 | Skills=0.2857
   Matched: ['docker', 'git']
3. Software Engineer            Final=0.4503 | DeBERTa=0.8271 | Embedding=0.2461 | Skills=0.2500
   Matched: ['git', 'python']
4. Full Stack Developer         Final=0.3917 | DeBERTa=0.1001 | Embedding=0.6309 | Skills=0.3636
   Matched: ['docker', 'git', 'python', 'rest api']
5. Frontend Developer           Final=0.2780 | DeBERTa=0.2101 | Embedding=0.3275 | Skills=0.2857
   Matched: ['git', 'rest api']

==========================================================================================
Machine Learning
==========================================================================================
1. Machine Learning Engineer    Final=0.6840 | DeBERTa=0.4973 | Embedding=1.0000 | Skills=0.3000
   Matched: ['python', 'pytorch', 'scikit-learn']
2. Software Engineer            Final=0.5654 | DeBERTa=1.0000 | Embedding=0.4232 | Skills=0.1250
   Matched: ['python']
3. Data Scientist               Final=0.5638 | DeBERTa=0.4130 | Embedding=0.7836 | Skills=0.3333
   Matched: ['python', 'scikit-learn']
4. Data Analyst                 Final=0.3959 | DeBERTa=0.7731 | Embedding=0.1673 | Skills=0.2500
   Matched: ['python']
5. Cybersecurity Engineer       Final=0.2697 | DeBERTa=0.0367 | Embedding=0.4226 | Skills=0.3333
   Matched: ['python']

==========================================================================================
Frontend
==========================================================================================
1. Frontend Developer           Final=0.9429 | DeBERTa=1.0000 | Embedding=1.0000 | Skills=0.7143
   Matched: ['css', 'html', 'javascript', 'react', 'typescript']
2. Full Stack Developer         Final=0.5019 | DeBERTa=0.0480 | Embedding=0.8760 | Skills=0.4545
   Matched: ['css', 'html', 'javascript', 'react', 'typescript']
3. Software Engineer            Final=0.4961 | DeBERTa=0.6134 | Embedding=0.6254 | Skills=0.0000
   Matched: []
4. Backend Developer            Final=0.2681 | DeBERTa=0.0890 | Embedding=0.5266 | Skills=0.0000
   Matched: []
5. Embedded Systems Engineer    Final=0.2566 | DeBERTa=0.0000 | Embedding=0.5702 | Skills=0.0000
   Matched: []

==========================================================================================
Cybersecurity
==========================================================================================
1. Cybersecurity Engineer       Final=0.8667 | DeBERTa=1.0000 | Embedding=1.0000 | Skills=0.3333
   Matched: ['linux']
2. QA Engineer                  Final=0.4241 | DeBERTa=0.7390 | Embedding=0.3677 | Skills=0.0000
   Matched: []
3. Embedded Systems Engineer    Final=0.3864 | DeBERTa=0.2675 | Embedding=0.5766 | Skills=0.1667
   Matched: ['linux']
4. Software Engineer            Final=0.3693 | DeBERTa=0.3969 | Embedding=0.5119 | Skills=0.0000
   Matched: []
5. Data Analyst                 Final=0.2725 | DeBERTa=0.7785 | Embedding=0.0000 | Skills=0.0000
   Matched: []
   
   '''

from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)


CASES = {

    "Backend": """
    Built REST APIs using Python and FastAPI.
    Worked with PostgreSQL,
    Docker, Git, authentication
    and server-side systems.
    """,

    "Machine Learning": """
    Built classification systems
    using Python, scikit-learn,
    PyTorch and transformer models.

    Performed feature engineering,
    evaluation and NLP experiments.
    """,

    "Frontend": """
    Built responsive interfaces
    with React, TypeScript,
    JavaScript, HTML and CSS.
    """,

    "Cybersecurity": """
    Performed vulnerability assessments,
    penetration testing,
    network security analysis,
    security auditing and incident response.

    Worked with Linux systems.
    """
}


for name, text in CASES.items():

    results = recommend_roles_hybrid(cv_text=text, top_k=5, include_components=True)

    print()
    print("=" * 90)
    print(name)
    print("=" * 90)

    for index, result in enumerate( results, start=1):

        print(
            f"{index}. "
            f"{result['role']:<28} "
            f"Final={result['score']:.4f} | "
            f"DeBERTa={result['deberta_normalized']:.4f} | "
            f"Embedding={result['embedding_normalized']:.4f} | "
            f"Skills={result['skill_score']:.4f}"
        )

        print( "   Matched:", result["matched_skills"])