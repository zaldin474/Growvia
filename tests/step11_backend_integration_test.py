from pathlib import Path
import requests
import json


# ============================================
# AI SERVICE CONFIGURATION
# ============================================

AI_BASE_URL = "http://127.0.0.1:8001" # URL of Ai service

HEALTH_URL = f"{AI_BASE_URL}/health"

ANALYZE_URL = f"{AI_BASE_URL}/analyze-cv"


# Use test CV already inside Growvia
BASE_DIR = Path(__file__).resolve().parent

CV_PATH = BASE_DIR / "test_cv.pdf" # local cv 


# ============================================
# 1. HEALTH CHECK
# ============================================

def test_health():

    response = requests.get( HEALTH_URL, timeout=10)

    print("\n==============================")
    print("AI HEALTH CHECK")
    print("==============================")

    print("Status code:", response.status_code)
    print("Response:", response.json())

    response.raise_for_status()


# ============================================
# 2. SIMULATE BACKEND -> AI REQUEST
# ============================================

def analyze_cv_from_backend(cv_path: Path,  target_role: str | None = None):

    with cv_path.open("rb") as file: # opens the PDF in binary mode.

        files = {  "cv" : (cv_path.name, file, "application/pdf") }

        data = {}

        if target_role:
            data["target_role"] = target_role

        response = requests.post( # requests.post converts the request into somthing like  POST /analyze-cv
            ANALYZE_URL, 
            files=files,
            data=data,
            timeout=300
        )

    print("\n==============================")
    print("BACKEND -> AI RESPONSE")
    print("==============================")

    print("Status code:", response.status_code)

    if response.status_code != 200:

        print("Error response:")
        print(response.text)

        response.raise_for_status()

    result = response.json()

    print( json.dumps(result,   indent=4,  ensure_ascii=False) )

    return result


# ============================================
# 3. VERIFY RESPONSE CONTRACT
# ============================================

def validate_response(result: dict): # Answers "Did my AI API return what the backend expects?""

    required_fields = [
        "profile",
        "recommended_roles",
        "selected_target_role",
        "skill_gap",
        "cv_suggestions",
        "project_suggestions"
    ]

    print("\n==============================")
    print("RESPONSE CONTRACT TEST")
    print("==============================")

    for field in required_fields:

        assert field in result, (  f"Missing required field: {field}")

        print(f"✓ {field}")

    print("\nAll required fields are present.")


# ============================================
# MAIN
# ============================================

def main():

    if not CV_PATH.exists():
        
        raise FileNotFoundError(f"Test CV was not found: {CV_PATH}" )

    # Check whether AI service is alive
    test_health()

    # Simulate backend sending CV to AI
    result = analyze_cv_from_backend(CV_PATH,  target_role="Backend Developer")

    # Make sure JSON contract is correct
    validate_response(result)

    print("\n==============================")
    print("INTEGRATION TEST PASSED")
    print("==============================")


if __name__ == "__main__":
    main()