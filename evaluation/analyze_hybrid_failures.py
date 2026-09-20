from evaluation.role_evaluation_data import (
    EXPANDED_EVALUATION_CASES
)

from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)


for case in EXPANDED_EVALUATION_CASES:

    results = recommend_roles_hybrid(
        cv_text=case["text"],
        top_k=5,
        include_components=True
    )

    predicted_top1 = results[0]["role"]

    expected = case[
        "expected_roles"
    ]

    if predicted_top1 in expected:
        continue


    print()
    print("=" * 100)

    print(
        f"{case['name']} "
        f"[{case['difficulty']}]"
    )

    print(
        "Expected:",
        expected
    )

    print("=" * 100)


    for index, result in enumerate(
        results,
        start=1
    ):

        print()

        print(
            f"{index}. "
            f"{result['role']}"
        )

        print(
            f"   Final:       "
            f"{result['score']:.4f}"
        )

        print(
            f"   DeBERTa raw: "
            f"{result['deberta_score']:.4f}"
        )

        print(
            f"   DeBERTa norm:"
            f" {result['deberta_normalized']:.4f}"
        )

        print(
            f"   Embedding:   "
            f"{result['embedding_score']:.4f}"
        )

        print(
            f"   Embed norm:  "
            f"{result['embedding_normalized']:.4f}"
        )

        print(
            f"   Skill score: "
            f"{result['skill_score']:.4f}"
        )

        print(
            "   Matched:",
            result["matched_skills"]
        )