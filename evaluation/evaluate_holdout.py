from cv_analysis.step03_role_classifier import (
    classify_roles
)

from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)

from evaluation.role_holdout_data import (
    HOLDOUT_CASES
)


def evaluate(
    name,
    recommender
):
    top1 = 0
    top3 = 0
    top5 = 0

    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    for case in HOLDOUT_CASES:

        results = recommender(
            case["text"]
        )

        roles = [
            result["role"]
            for result in results
        ]

        expected = case[
            "expected_roles"
        ]

        top1_ok = bool(
            set(roles[:1])
            & expected
        )

        top3_ok = bool(
            set(roles[:3])
            & expected
        )

        top5_ok = bool(
            set(roles[:5])
            & expected
        )

        top1 += int(top1_ok)
        top3 += int(top3_ok)
        top5 += int(top5_ok)

        marker = (
            "PASS"
            if top1_ok
            else "MISS"
        )

        print()
        print(
            f"{marker} | "
            f"{case['name']}"
        )

        print(
            "Expected:",
            expected
        )

        print(
            "Top 5:",
            roles[:5]
        )

    total = len(
        HOLDOUT_CASES
    )

    print()
    print("-" * 70)

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

    return {
        "top1": top1,
        "top3": top3,
        "top5": top5,
        "total": total
    }


def old_recommender(text):

    return classify_roles(
        text,
        top_k=5
    )


def hybrid_recommender(text):

    return recommend_roles_hybrid(
        text,
        top_k=5
    )


old = evaluate(
    "HOLDOUT — DeBERTa only",
    old_recommender
)

new = evaluate(
    "HOLDOUT — Hybrid",
    hybrid_recommender
)


print()
print("=" * 70)
print("HOLDOUT COMPARISON")
print("=" * 70)

print(
    f"Top-1: "
    f"{old['top1'] / old['total'] * 100:.2f}%"
    f" -> "
    f"{new['top1'] / new['total'] * 100:.2f}%"
)

print(
    f"Top-3: "
    f"{old['top3'] / old['total'] * 100:.2f}%"
    f" -> "
    f"{new['top3'] / new['total'] * 100:.2f}%"
)