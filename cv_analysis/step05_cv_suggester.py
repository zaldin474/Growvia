from transformers import ( AutoTokenizer, AutoModelForSeq2SeqLM )
from .generation_utils import ( generate_text, is_bad_generation)
import re

MODEL_NAME = "google/flan-t5-base"


_tokenizer = None
_model = None


def get_model():
    global _tokenizer
    global _model

    if _model is None:

        print("Loading CV suggestion model...")

        _tokenizer = (AutoTokenizer.from_pretrained(MODEL_NAME))

        _model = (AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME) )

    return _tokenizer, _model

def is_valid_feedback_generation(text: str) -> bool:

    if not text:
        return False

    lower = text.lower()

    prompt_echo_markers = [
        "write exactly 3",
        "target career role",
        "detected technical skills",
        "missing cv sections",
        "requirements:"
    ]

    if any(
        marker in lower
        for marker
        in prompt_echo_markers
    ):
        return False


    # We expect suggestions 1, 2 and 3.
    for number in (
        1,
        2,
        3
    ):

        pattern = (
            rf"(?:^|\n|\s)"
            rf"{number}[\.\)]\s+"
        )

        if not re.search(
            pattern,
            text
        ):
            return False


    if len(
        text.split()
    ) < 18:
        return False

    return True


# determenistic fall back in case ai fails
def build_feedback_fallback( profile: dict, target_role: str,  missing_skills: list[str]) -> str:

    suggestions = []

    sections = profile.get(
        "sections",
        {}
    )


    skills = profile.get(
        "skills",
        []
    )

    word_count = profile.get(
        "word_count",
        0
    )


    if not sections.get(
        "experience",
        False
    ):

        suggestions.append(
            "Add an Experience section if you have internships, "
            "freelance work, volunteering, or other relevant technical work."
        )


    if word_count < 250:

        suggestions.append(
            "Expand the project descriptions with your contribution, "
            "the technologies used, and measurable or concrete outcomes."
        )


    if missing_skills:

        important_missing = ", ".join(
            missing_skills[:3]
        )

        suggestions.append(
            f"For a {target_role} path, consider building projects "
            f"that demonstrate {important_missing}; only add these "
            f"skills to the CV after you have actually used them."
        )


    if skills:

        suggestions.append(
            "Strengthen the Technical Skills section by grouping "
            "languages, frameworks, databases, and tools into clear categories."
        )


    if not sections.get(
        "certifications",
        False
    ):

        suggestions.append(
            "If you have completed relevant certifications or technical "
            "courses, add a Certifications section with the provider and date."
        )


    # Ensure exactly three useful suggestions.
    suggestions = suggestions[:3]

    while len(suggestions) < 3:

        suggestions.append(
            "Use achievement-focused project bullets that explain "
            "what you built, how you built it, and what problem it solved."
        )


    return "\n".join(
        f"{index}. {suggestion}"
        for index, suggestion
        in enumerate(
            suggestions,
            start=1
        )
    )


def generate_ai_feedback(
    profile: dict,
    target_role: str,
    missing_skills: list[str]
) -> str:

    skills = profile.get(
        "skills",
        []
    )

    sections = profile.get(
        "sections",
        {}
    )

    word_count = profile.get(
        "word_count",
        0
    )

    existing_skills = (
        ", ".join(skills)
        if skills
        else "none detected"
    )

    missing_text = (
        ", ".join(missing_skills)
        if missing_skills
        else "none"
    )

    missing_sections = [
        section
        for section, exists
        in sections.items()
        if not exists
    ]

    missing_sections_text = (
        ", ".join(missing_sections)
        if missing_sections
        else "none"
    )


    prompt = f"""
You are reviewing a student's CV.

Target career role:
{target_role}

Detected technical skills:
{existing_skills}

Skills useful for the target role but not detected:
{missing_text}

Missing CV sections:
{missing_sections_text}

CV word count:
{word_count}

Write exactly 3 short, specific and actionable CV improvement suggestions.

Requirements:
- Refer to the candidate's actual skills or missing skills.
- Do not invent experience.
- Do not tell the candidate to lie or claim skills they do not have.
- Explain what should be improved.
- Each suggestion must be useful on its own.
- Do not repeat these instructions.
- Do not write headings.
""".strip()


    try:

     generated = generate_text(
        prompt,
        max_new_tokens=140
    )

    except Exception:

     return build_feedback_fallback(
        profile=profile,
        target_role=target_role,
        missing_skills=missing_skills
        )

    bad_phrases = [
        "be specific",
        "a cv improvement suggestion",
        "write exactly",
        "requirements:",
        "detected technical skills"
    ]


    if (is_bad_generation(generated, minimum_words=18,forbidden_phrases= bad_phrases) 
        or 
        not is_valid_feedback_generation(generated)
    ):
       return build_feedback_fallback(
                                        profile=profile,
                                        target_role=target_role,
                                        missing_skills=missing_skills
                                    )

    return generated


def rule_based_suggestions(profile: dict) -> list[str]:

    suggestions = []

    sections = profile.get("sections", {})

    if not sections.get("projects"):
        suggestions.append("Add a dedicated Projects section.")

    if not sections.get("skills"):
        suggestions.append("Add a dedicated Technical Skills section.")

    if not sections.get("experience"):
        suggestions.append(
            "If you have internships, volunteer work, "
            "or relevant technical experience, add an "
            "Experience section."
        )

    if not sections.get("certifications"):
        suggestions.append(
            "Consider listing relevant certifications "
            "if you have completed any."
        )

    word_count = profile.get("word_count",  0)

    if word_count < 200:
        suggestions.append(
            "The CV appears very short. Add more detail "
            "about projects, responsibilities, and "
            "technical achievements."
        )

    if word_count > 1200:
        suggestions.append(
            "The CV may be too long. Consider shortening "
            "less relevant descriptions."
        )

    return suggestions


def generate_ai_suggestions(cv_text: str,  target_role: str,   missing_skills: list[str]) -> str:

    tokenizer, model = get_model()

    short_cv = cv_text[:2500]

    missing = (
        ", ".join(missing_skills)
        if missing_skills
        else "No major skill gaps detected"
    )

    prompt = f"""
Review this CV for a candidate targeting a {target_role} position.

CV:
{short_cv}

Missing technical skills:
{missing}

Give exactly 5 short CV improvement suggestions.

Each suggestion must:
- be specific
- be based on the CV
- not invent experience
- help the candidate become more competitive for {target_role}

Write only the 5 suggestions.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        num_beams=5,
        early_stopping=True,
        repetition_penalty=1.2
    )

    result = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()

    if not result:
        return (
            "No AI-generated suggestions were produced. "
            "Use the rule-based suggestions."
        )

    return result


def generate_cv_suggestions(cv_text: str, profile: dict, target_role: str,  missing_skills: list[str]) -> dict:

    rules = rule_based_suggestions(profile)

    # ai_advice = generate_ai_suggestions( cv_text, target_role, missing_skills)

    ai_advice = generate_ai_feedback(
                                        profile=profile,
                                        target_role=target_role,
                                        missing_skills=missing_skills
                                        )
                                        
    return {
        "rule_based": rules,
        "ai_feedback": ai_advice
    }