# python -m evaluation.evaluate_role_classifier
from cv_analysis.step03_role_classifier import classify_roles


# =========================================================
# EVALUATION DATASET
#
# IMPORTANT:
# These profiles deliberately avoid directly stating
# the expected job title.
# =========================================================

EVALUATION_CASES = [

    {
        "name": "backend_1",
        "expected_roles": {
            "Backend Developer",
            "Software Engineer",
            "Full Stack Developer"
        },
        "text": """
        Computer engineering student with experience building
        REST APIs using Python and FastAPI.

        Worked with PostgreSQL and SQL for database design,
        implemented authentication systems, CRUD operations,
        server-side business logic, and API testing.

        Familiar with Docker, Git, and Linux.
        """
    },

    {
        "name": "backend_2",
        "expected_roles": {
            "Backend Developer",
            "Software Engineer",
            "Full Stack Developer"
        },
        "text": """
        Developed server-side applications using Java and Spring Boot.

        Designed relational database schemas using PostgreSQL,
        implemented REST endpoints, JWT authentication,
        error handling, and database queries.

        Used Git and Docker during development.
        """
    },

    {
        "name": "ml_1",
        "expected_roles": {
            "Machine Learning Engineer",
            "Data Scientist"
        },
        "text": """
        Experienced with Python, pandas, NumPy and scikit-learn.

        Built classification and regression models,
        performed feature engineering and model evaluation,
        compared precision, recall and F1 scores,
        and deployed trained models through FastAPI.

        Also experimented with transformers and NLP.
        """
    },

    {
        "name": "ml_2",
        "expected_roles": {
            "Machine Learning Engineer",
            "Data Scientist"
        },
        "text": """
        Built text classification systems using TF-IDF,
        Logistic Regression and transformer models.

        Worked with preprocessing, model training,
        hyperparameter tuning, confusion matrices,
        ROC-AUC evaluation and model serialization.

        Used Python, PyTorch and Hugging Face Transformers.
        """
    },

    {
        "name": "frontend_1",
        "expected_roles": {
            "Frontend Developer",
            "Full Stack Developer"
        },
        "text": """
        Built responsive web interfaces using React,
        JavaScript, TypeScript, HTML and CSS.

        Created reusable UI components,
        handled client-side state,
        consumed REST APIs,
        and implemented responsive layouts.

        Focused heavily on usability and browser interfaces.
        """
    },

    {
        "name": "frontend_2",
        "expected_roles": {
            "Frontend Developer",
            "Full Stack Developer"
        },
        "text": """
        Developed interactive websites using React and TypeScript.

        Worked with component-based architecture,
        forms, routing, state management,
        responsive layouts and API integration.

        Familiar with HTML, CSS and modern JavaScript.
        """
    },

    {
        "name": "devops_1",
        "expected_roles": {
            "DevOps Engineer"
        },
        "text": """
        Worked with Linux servers, Docker containers,
        Kubernetes, GitHub Actions and automated deployment.

        Created CI/CD pipelines,
        configured monitoring,
        automated infrastructure tasks
        and managed containerized applications.
        """
    },

    {
        "name": "devops_2",
        "expected_roles": {
            "DevOps Engineer"
        },
        "text": """
        Experience automating build, test and deployment workflows.

        Used Docker, Kubernetes, Linux,
        CI pipelines and cloud infrastructure.

        Worked on application monitoring,
        deployment reliability and infrastructure automation.
        """
    },

    {
        "name": "security_1",
        "expected_roles": {
            "Cybersecurity Engineer"
        },
        "text": """
        Performed vulnerability assessments,
        penetration testing and network security analysis.

        Worked with firewalls, threat monitoring,
        incident response and security auditing.

        Familiar with common attack vectors
        and defensive security practices.
        """
    },

    {
        "name": "security_2",
        "expected_roles": {
            "Cybersecurity Engineer"
        },
        "text": """
        Analyzed network traffic and system vulnerabilities.

        Performed security assessments,
        investigated suspicious activity,
        tested application security
        and documented remediation recommendations.
        """
    }
]


# =========================================================
# EVALUATION
# =========================================================

def evaluate():

    top1_correct = 0
    top3_correct = 0
    top5_correct = 0

    total = len(EVALUATION_CASES)

    print("\n==========================================")
    print("GROWVIA ROLE CLASSIFIER EVALUATION")
    print("==========================================\n")

    for case in EVALUATION_CASES:

        results = classify_roles( case["text"], top_k=5)

        predicted_roles = [ result["role"] for result in results]

        expected = case["expected_roles"]

        top1 = set(predicted_roles[:1])
        top3 = set(predicted_roles[:3])
        top5 = set(predicted_roles[:5])

        is_top1_correct = bool( top1 & expected)

        is_top3_correct = bool( top3 & expected)

        is_top5_correct = bool( top5 & expected)

        if is_top1_correct:
            top1_correct += 1

        if is_top3_correct:
            top3_correct += 1

        if is_top5_correct:
            top5_correct += 1

        print("------------------------------------------")
        print("Case:", case["name"])
        print("Expected:" , ", ".join(sorted(expected)))

        print("\nPredictions:")

        for index, result in enumerate( results,  start=1):
            print(
                f"{index}. "
                f"{result['role']} "
                f"({result['score']:.4f})"
            )

        print(
            "\nTop-1:",
            "PASS" if is_top1_correct else "FAIL"
        )

        print(
            "Top-3:",
            "PASS" if is_top3_correct else "FAIL"
        )

        print(
            "Top-5:",
            "PASS" if is_top5_correct else "FAIL"
        )

        print()

    top1_accuracy = ( top1_correct / total) * 100

    top3_accuracy = ( top3_correct / total) * 100

    top5_accuracy = ( top5_correct / total) * 100

    print("\n==========================================")
    print("FINAL RESULTS")
    print("==========================================")

    print(f"Total profiles: {total}")

    print(
        f"Top-1 Accuracy: "
        f"{top1_accuracy:.2f}% "
        f"({top1_correct}/{total})"
    )

    print(
        f"Top-3 Accuracy: "
        f"{top3_accuracy:.2f}% "
        f"({top3_correct}/{total})"
    )

    print(
        f"Top-5 Accuracy: "
        f"{top5_accuracy:.2f}% "
        f"({top5_correct}/{total})"
    )


if __name__ == "__main__":
    evaluate()