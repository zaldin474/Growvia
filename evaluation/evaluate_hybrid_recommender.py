# run
# activate .venv
# python -m evaluation.evaluate_hybrid_recommender

from collections import defaultdict

from cv_analysis.step03_role_classifier import (
    classify_roles
)

from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)

from evaluation.role_evaluation_data import ( # uses it for Test cases 
    EXPANDED_EVALUATION_CASES
)


def evaluate( recommender,name: str):

    total = 0

    top1 = 0
    top3 = 0
    top5 = 0

    difficulty_stats = defaultdict(
        lambda: {
            "total": 0,
            "top1": 0,
            "top3": 0,
            "top5": 0
        }
    )

    failures = []


    for case in EXPANDED_EVALUATION_CASES:

        predictions = recommender( case["text"])

        roles = [result["role"] for result in predictions]

        expected = case[ "expected_roles"]

        difficulty = case["difficulty"]


        top1_ok = bool(set(roles[:1])& expected)

        top3_ok = bool( set(roles[:3])& expected)

        top5_ok = bool( set(roles[:5]) & expected)


        total += 1

        top1 += int(top1_ok)
        top3 += int(top3_ok)
        top5 += int(top5_ok)


        stats = difficulty_stats[
            difficulty
        ]

        stats["total"] += 1

        stats["top1"] += int(  top1_ok)

        stats["top3"] += int( top3_ok)

        stats["top5"] += int( top5_ok)


        if not top1_ok:

            failures.append(
                {
                    "name": case["name"],
                    "difficulty":
                        difficulty,
                    "expected":
                        expected,
                    "predicted":
                        roles[:5]
                }
            )


    return {
        "name": name,
        "total": total,

        "top1": top1,
        "top3": top3,
        "top5": top5,

        "difficulty_stats":
            difficulty_stats,

        "failures":
            failures
    }


def print_results(
    result
):

    total = result["total"]

    print()
    print("=" * 70)
    print(result["name"])
    print("=" * 70)

    print(
        f"Profiles: {total}"
    )

    print(
        f"Top-1: "
        f"{result['top1']}/{total} "
        f"({result['top1'] / total * 100:.2f}%)"
    )

    print(
        f"Top-3: "
        f"{result['top3']}/{total} "
        f"({result['top3'] / total * 100:.2f}%)"
    )

    print(
        f"Top-5: "
        f"{result['top5']}/{total} "
        f"({result['top5'] / total * 100:.2f}%)"
    )


    print()
    print("By difficulty:")

    for difficulty in [
        "clear",
        "noisy",
        "ambiguous"
    ]:

        stats = result[
            "difficulty_stats"
        ][difficulty]

        n = stats["total"]

        print()

        print(
            f"{difficulty.upper()}:"
        )

        print(
            f"  Top-1: "
            f"{stats['top1']}/{n} "
            f"({stats['top1'] / n * 100:.2f}%)"
        )

        print(
            f"  Top-3: "
            f"{stats['top3']}/{n} "
            f"({stats['top3'] / n * 100:.2f}%)"
        )

        print(
            f"  Top-5: "
            f"{stats['top5']}/{n} "
            f"({stats['top5'] / n * 100:.2f}%)"
        )


    print()
    print("Top-1 failures:")

    if not result["failures"]:

        print(
            "  None"
        )

    for failure in result[
        "failures"
    ]:

        print()

        print(
            f"  {failure['name']} "
            f"[{failure['difficulty']}]"
        )

        print(
            f"  Expected: "
            f"{failure['expected']}"
        )

        print(
            f"  Predicted: "
            f"{failure['predicted']}"
        )


def old_recommender(
    text
):

    return classify_roles(
        text,
        top_k=5
    )


def new_recommender(
    text
):

    return recommend_roles_hybrid(
        text,
        top_k=5
    )


old_result = evaluate(
    old_recommender,
    "OLD — DeBERTa only"
)

new_result = evaluate(
    new_recommender,
    "NEW — Hybrid recommender"
)


print_results(
    old_result
)

print_results(
    new_result
)


print()
print("=" * 70)
print("IMPROVEMENT")
print("=" * 70)

old_top1 = (
    old_result["top1"]
    / old_result["total"]
    * 100
)

new_top1 = (
    new_result["top1"]
    / new_result["total"]
    * 100
)

old_top3 = (
    old_result["top3"]
    / old_result["total"]
    * 100
)

new_top3 = (
    new_result["top3"]
    / new_result["total"]
    * 100
)

print(
    f"Top-1: "
    f"{old_top1:.2f}% "
    f"-> "
    f"{new_top1:.2f}%"
)

print(
    f"Top-3: "
    f"{old_top3:.2f}% "
    f"-> "
    f"{new_top3:.2f}%"
)