# LOCAL TEST

# this class is to test it with a local pdf
# run python step10_test_pipeline.py with .venv active

from Growvia.cv_analysis.step01_cv_parser import (extract_cv_text) # parse cv
from Growvia.app.step08_pipeline import (run_cv_analysis) # do all the other work
import json


CV_PATH = "test_cv.pdf"


def main():

    with open(CV_PATH, "rb") as file:

        file_bytes = file.read()

    cv_text = extract_cv_text(file_bytes, CV_PATH)

    print("\n")
    print("=" * 60)
    print("EXTRACTED CV")
    print("=" * 60)

    print(cv_text[:1000])

    result = run_cv_analysis( cv_text=cv_text, target_role=( "Backend Developer" ))

    print("\n")
    print("=" * 60)
    print("CV ANALYSIS")
    print("=" * 60)

    print( json.dumps(result, indent=4,  ensure_ascii=False) )


if __name__ == "__main__":
    main()
    
    
    
    
