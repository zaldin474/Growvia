# run 
# activate .venv 
# python -m evaluation.inspect_embedding_roles
'''Results 
==================================================
Backend
==================================================
Extracted skills: ['docker', 'fastapi', 'git', 'postgresql', 'python', 'rest api']

1. Backend Developer              0.6861
2. Full Stack Developer           0.5556
3. Frontend Developer             0.4478
4. DevOps Engineer                0.4249
5. Machine Learning Engineer      0.4201

==================================================
Machine Learning
==================================================
Extracted skills: ['python', 'pytorch', 'scikit-learn']

1. Machine Learning Engineer      0.6960
2. Data Scientist                 0.6233
3. Software Engineer              0.4974
4. Cybersecurity Engineer         0.4791
5. Embedded Systems Engineer      0.4251

==================================================
Frontend
==================================================
Extracted skills: ['css', 'html', 'javascript', 'react', 'typescript']

1. Frontend Developer             0.6121
2. Full Stack Developer           0.5668
3. Software Engineer              0.4863
4. Embedded Systems Engineer      0.4731
5. Machine Learning Engineer      0.4579

==================================================
Cybersecurity
==================================================
Extracted skills: ['linux']

1. Cybersecurity Engineer         0.6620
2. Embedded Systems Engineer      0.5297
3. Software Engineer              0.4968
4. Machine Learning Engineer      0.4827
5. Backend Developer              0.4587
'''


from cv_analysis.role_embedding_similarity import ( calculate_role_similarity)

from cv_analysis.skill_normalizer import ( extract_skills)


CASES = {

    "Backend": """
    Built REST APIs using Python and FastAPI.
    Worked with PostgreSQL, authentication,
    Docker, Git and server-side systems.
    """,

    "Machine Learning": """
    Built classification models using Python,
    scikit-learn and PyTorch.
    Performed feature engineering,
    model evaluation and NLP experiments.
    """,

    "Frontend": """
    Developed responsive interfaces with
    React, TypeScript, JavaScript,
    HTML and CSS.
    """,

    "Cybersecurity": """
    Performed vulnerability assessments,
    penetration testing, network security
    analysis and incident response.
    Worked extensively with Linux systems.
    """
}


for name, text in CASES.items():

    skills = extract_skills(text)

    results = calculate_role_similarity(
        cv_text=text,
        extracted_skills=skills,
        top_k=5
    )

    print()
    print("=" * 50)
    print(name)
    print("=" * 50)

    print("Extracted skills:", skills)

    print()

    for index, result in enumerate( results, start=1):

        print(
            f"{index}. "
            f"{result['role']:<30} "
            f"{result['embedding_score']:.4f}"
        )