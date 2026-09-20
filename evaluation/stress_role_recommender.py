from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)


STRESS_CASES = [

    {
        "name": "backend_natural",
        "expected": "Backend Developer",
        "text": """
        Implemented account authentication,
        database persistence and HTTP endpoints.

        Worked with Python, FastAPI,
        PostgreSQL and Docker.

        Added request validation,
        error handling and server-side logic.
        """
    },

    {
        "name": "frontend_natural",
        "expected": "Frontend Developer",
        "text": """
        Created responsive browser interfaces
        with React and TypeScript.

        Built reusable components,
        forms and layouts using HTML and CSS
        and consumed REST endpoints.
        """
    },

    {
        "name": "fullstack_natural",
        "expected": "Full Stack Developer",
        "text": """
        Created a complete web application.

        Built React pages on the client side
        and Python API endpoints on the server.

        Used SQL for persistence,
        REST communication and Docker.
        """
    },

    {
        "name": "software_natural",
        "expected": "Software Engineer",
        "text": """
        Developed Java and C++ programs
        using object-oriented principles.

        Designed classes with UML,
        applied design patterns
        and maintained the code with Git.
        """
    },

    {
        "name": "ml_natural",
        "expected": "Machine Learning Engineer",
        "text": """
        Trained classification models
        using Python and PyTorch.

        Built preprocessing pipelines,
        evaluated model performance
        and experimented with deep learning.
        """
    },

    {
        "name": "datascience_natural",
        "expected": "Data Scientist",
        "text": """
        Explored datasets using Python,
        pandas and NumPy.

        Performed feature engineering,
        statistical experimentation
        and trained prediction models
        with scikit-learn.
        """
    },

    {
        "name": "analyst_natural",
        "expected": "Data Analyst",
        "text": """
        Queried business information
        using SQL.

        Cleaned datasets with Python
        and pandas and prepared recurring
        reports about business trends
        and performance metrics.
        """
    },

    {
        "name": "devops_natural",
        "expected": "DevOps Engineer",
        "text": """
        Automated application deployment
        with Jenkins and GitHub Actions.

        Worked with Docker,
        Kubernetes and Linux
        and provisioned infrastructure
        using Terraform.
        """
    },

    {
        "name": "mobile_natural",
        "expected": "Mobile Developer",
        "text": """
        Developed Android applications
        with Kotlin and Android SDK.

        Also created a Flutter prototype
        and integrated remote REST services.
        """
    },

    {
        "name": "security_natural",
        "expected": "Cybersecurity Engineer",
        "text": """
        Assessed network vulnerabilities
        and investigated suspicious traffic.

        Performed penetration testing
        using Nmap, Wireshark
        and Burp Suite on Linux systems.
        """
    },

    {
        "name": "embedded_natural",
        "expected": "Embedded Systems Engineer",
        "text": """
        Programmed ESP32 boards
        using C and C++.

        Connected sensors and actuators,
        implemented firmware logic
        and debugged hardware communication.
        """
    },

    {
        "name": "qa_natural",
        "expected": "QA Engineer",
        "text": """
        Automated browser tests
        using Selenium and pytest.

        Tested REST endpoints with Postman,
        created regression suites
        and documented reproducible defects.
        """
    }
]

def run_stress_test():

    top1 = 0
    top3 = 0
    top5 = 0

    failures = []


    print()
    print("=" * 78)
    print("GROWVIA AI — 12 ROLE STRESS TEST")
    print("=" * 78)


    for case in STRESS_CASES:

        results = (
            recommend_roles_hybrid(
                case["text"],
                top_k=5,
                include_components=True
            )
        )

        roles = [
            result["role"]
            for result in results
        ]

        expected = case[
            "expected"
        ]


        rank = None

        if expected in roles:

            rank = (
                roles.index(
                    expected
                )
                + 1
            )


        top1_ok = (
            rank == 1
        )

        top3_ok = (
            rank is not None
            and rank <= 3
        )

        top5_ok = (
            rank is not None
            and rank <= 5
        )


        top1 += int(
            top1_ok
        )

        top3 += int(
            top3_ok
        )

        top5 += int(
            top5_ok
        )


        status = (
            "PASS"
            if top1_ok
            else "CHECK"
        )


        print()

        print(
            f"{status} | "
            f"{case['name']}"
        )

        print(
            f"Expected: "
            f"{expected}"
        )

        print(
            f"Top 5: "
            f"{roles}"
        )


        if not top1_ok:

            failures.append(
                {
                    "case":
                        case,

                    "results":
                        results
                }
            )


    total = len(
        STRESS_CASES
    )


    print()
    print("=" * 78)
    print("RESULTS")
    print("=" * 78)

    print(
        f"Top-1: "
        f"{top1}/{total} "
        f"({top1 / total * 100:.2f}%)"
    )

    print(
        f"Top-3: "
        f"{top3}/{total} "
        f"({top3 / total * 100:.2f}%)"
    )

    print(
        f"Top-5: "
        f"{top5}/{total} "
        f"({top5 / total * 100:.2f}%)"
    )


    if failures:

        print()
        print("=" * 78)
        print("TOP-1 CASES TO REVIEW")
        print("=" * 78)


        for failure in failures:

            case = failure[
                "case"
            ]

            results = failure[
                "results"
            ]


            print()
            print(
                case["name"]
            )

            print(
                "Expected:",
                case["expected"]
            )


            for index, result in enumerate(
                results,
                start=1
            ):

                print(
                    f"{index}. "
                    f"{result['role']} | "
                    f"final="
                    f"{result['score']:.4f} | "
                    f"deberta="
                    f"{result['deberta_score']:.4f} | "
                    f"embedding="
                    f"{result['embedding_normalized']:.4f} | "
                    f"skills="
                    f"{result['skill_score']:.4f}"
                )

                print(
                    "   matched:",
                    result[
                        "matched_skills"
                    ]
                )


if __name__ == "__main__":

    run_stress_test()