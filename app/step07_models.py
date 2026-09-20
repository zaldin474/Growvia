# Pydantic schemas for the final output.

from pydantic import BaseModel,  Field
from typing import Optional


class RolePrediction(BaseModel):
    role: str
    score: float


class SkillGapResult(BaseModel):
    target_role: str
    matched_skills: list[str]
    missing_skills: list[str]
    skill_coverage: float


class CVSuggestions(BaseModel):
    rule_based: list[str]
    ai_feedback: str

class ProjectEntry(BaseModel):
    title: Optional[str] = None
    description: str = ""
    technologies: list[str] = Field(
        default_factory=list
    )

class ProjectSuggestion(BaseModel):
    title: str

    description: str = ""

    technologies: list[str] = Field(  default_factory=list)

    skills_targeted: list[str] = Field( default_factory=list)

    difficulty: str = "Intermediate"
    
    
class CandidateProfile(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None

    skills: list[str]

    education: list[str]

    years_of_experience : Optional[float] = None

    projects: list[ProjectEntry] = Field(default_factory=list)
    
    certifications: list[str] = Field(default_factory=list)

    languages: list[str] = Field(default_factory=list)
    
    sections: dict

    word_count: int


class CVAnalysisResult(BaseModel):
    
    profile : CandidateProfile

    recommended_roles : list[RolePrediction]

    selected_target_role : str

    skill_gap : SkillGapResult

    cv_suggestions : CVSuggestions

    project_suggestions :  list[ProjectSuggestion] = Field (default_factory=list)