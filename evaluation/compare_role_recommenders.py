# run 
# activate .venv
# python -m evaluation.compare_role_recommenders
'''Results

============================================================
OLD DEBERTA RECOMMENDER
============================================================
Profiles: 10
Top-1: 50.00%
Top-3: 100.00%
Top-5: 100.00%

Top-1 failures:

backend_2
Expected: {'Full Stack Developer', 'Backend Developer', 'Software Engineer'}
Predicted: ['DevOps Engineer', 'Software Engineer', 'Backend Developer', 'Frontend Developer', 'Data Analyst']

ml_1
Expected: {'Data Scientist', 'Machine Learning Engineer'}
Predicted: ['Data Analyst', 'Software Engineer', 'Machine Learning Engineer', 'Data Scientist', 'QA Engineer']

ml_2
Expected: {'Data Scientist', 'Machine Learning Engineer'}
Predicted: ['Data Analyst', 'Machine Learning Engineer', 'Data Scientist', 'Software Engineer', 'Full Stack Developer']

security_1
Expected: {'Cybersecurity Engineer'}
Predicted: ['Data Analyst', 'Cybersecurity Engineer', 'QA Engineer', 'Data Scientist', 'Embedded Systems Engineer']

security_2
Expected: {'Cybersecurity Engineer'}
Predicted: ['Data Analyst', 'Cybersecurity Engineer', 'QA Engineer', 'Data Scientist', 'Software Engineer']

============================================================
NEW HYBRID RECOMMENDER
============================================================
Profiles: 10
Top-1: 100.00%
Top-3: 100.00%
Top-5: 100.00%

Top-1 failures:

============================================================
COMPARISON
============================================================
Top-1: 50.00% -> 100.00%
Top-3: 100.00% -> 100.00%
Top-5: 100.00% -> 100.00%

'''

from cv_analysis.step03_role_classifier import (
    classify_roles
)

from cv_analysis.hybrid_role_recommender import (
    recommend_roles_hybrid
)

from evaluation.evaluate_role_classifier import (
    EVALUATION_CASES
)


def calculate_metrics( prediction_function):

    top1_correct = 0
    top3_correct = 0
    top5_correct = 0

    failures = []

    for case in EVALUATION_CASES:

        results = prediction_function( case["text"])

        roles = [ result["role"]  for result in results]

        expected = ( case["expected_roles"])

        top1_ok = bool( set(roles[:1]) & expected)

        top3_ok = bool( set(roles[:3]) & expected)

        top5_ok = bool ( set(roles[:5])& expected)

        top1_correct += int( top1_ok)

        top3_correct += int( top3_ok)

        top5_correct += int( top5_ok)

        if not top1_ok:

            failures.append(
                {
                    "name": case["name"],
                    "expected": expected,
                    "predicted": roles[:5]
                }
            )

    total = len(EVALUATION_CASES)

    return {
        "total": total,

        "top1": ( top1_correct / total * 100),

        "top3": ( top3_correct / total * 100),

        "top5": ( top5_correct  / total  * 100),

        "failures": failures
    }


def old_recommender(text):

    return classify_roles( text,top_k=5)


def hybrid_recommender(text):

    return recommend_roles_hybrid( text, top_k=5)


def print_metrics(name, metrics):

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Profiles: "f"{metrics['total']}")

    print( f"Top-1: "f"{metrics['top1']:.2f}%")

    print(f"Top-3: "f"{metrics['top3']:.2f}%")

    print( f"Top-5: "f"{metrics['top5']:.2f}%")

    print()
    
    print("Top-1 failures:")

    for failure in metrics["failures"]:

        print()
        print( failure["name"])

        print( "Expected:", failure["expected"] )

        print( "Predicted:", failure["predicted"])


old_metrics = calculate_metrics(old_recommender)

hybrid_metrics = calculate_metrics( hybrid_recommender)


print_metrics( "OLD DEBERTA RECOMMENDER", old_metrics)

print_metrics( "NEW HYBRID RECOMMENDER", hybrid_metrics)


print()
print("=" * 60)
print("COMPARISON")
print("=" * 60)

print(
    f"Top-1: "
    f"{old_metrics['top1']:.2f}%"
    f" -> "
    f"{hybrid_metrics['top1']:.2f}%"
)

print(
    f"Top-3: "
    f"{old_metrics['top3']:.2f}%"
    f" -> "
    f"{hybrid_metrics['top3']:.2f}%"
)

print(
    f"Top-5: "
    f"{old_metrics['top5']:.2f}%"
    f" -> "
    f"{hybrid_metrics['top5']:.2f}%"
)