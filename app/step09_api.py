# run it using
# uvicorn step09_api:app --reload
# with .venv active.

from fastapi import ( FastAPI, UploadFile, File, Form, HTTPException)

from cv_analysis.step01_cv_parser import (extract_cv_text)
from app.step08_pipeline import (run_cv_analysis)
from app.step07_models import (CVAnalysisResult)
import logging


logger = logging.getLogger(__name__)

app = FastAPI(
    title="CV Analysis AI Service",
    
    description=(
        "Transformer-based CV analysis, "
        "skill-gap detection and "
        "project recommendation service."
    ),
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "service":
            "CV Analysis AI",

        "status":
            "running"
    }


@app.get("/health")

def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze-cv",
          response_model= CVAnalysisResult
)

async def analyze_cv(cv: UploadFile = File(...), target_role: str | None = Form(None)):

    try:

        file_bytes = await cv.read()

        cv_text = extract_cv_text(file_bytes, cv.filename)

        result = run_cv_analysis(cv_text=cv_text, target_role=target_role)

        return result
    

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:

        logger.exception(
        "Unhandled error during CV analysis."
        )

        raise HTTPException(
        status_code=500,
        detail="AI analysis failed."
        )