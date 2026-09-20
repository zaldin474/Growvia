import re # a library to support regular expressions

from datetime import date

from .skill_normalizer import extract_skills

# =========================================================
# PROJECT EXTRACTION
# =========================================================

_PROJECT_ACTION_VERBS = {
    "built",
    "developed",
    "implemented",
    "designed",
    "created",
    "used",
    "integrated",
    "deployed",
    "trained",
    "analyzed",
    "worked",
    "configured",
    "tested"
}

# =========================================================
# CV SECTION HEADINGS
# =========================================================

SECTION_HEADINGS = {
    "education": {
        "education",
        "academic background",
        "academic history",
        "academic qualifications"
    },

    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "employment"
    },

    "projects": {
        "projects",
        "project experience",
        "academic projects",
        "personal projects"
    },

    "skills": {
        "skills",
        "technical skills",
        "technical skills and tools",
        "technologies"
    },

    "certifications": {
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "licenses and certifications"
    },

    "languages": {
        "languages",
        "language",
        "language skills",
        "spoken languages"
    },

    "interests": {
        "interests",
        "interests and activities"
    }
}

# =========================================================
# EDUCATION PATTERNS
# =========================================================

DEGREE_PATTERN = re.compile(
    r"\b("
    r"bachelor(?:'s|’s)?|"
    r"b\.?\s?s\.?|"
    r"bsc|"
    r"master(?:'s|’s)?|"
    r"m\.?\s?s\.?|"
    r"msc|"
    r"ph\.?d\.?|"
    r"doctorate|"
    r"associate(?:'s|’s)?"
    r")\b",
    re.IGNORECASE
)


INSTITUTION_PATTERN = re.compile(
    r"\b("
    r"university|"
    r"college|"
    r"institute|"
    r"academy"
    r")\b",
    re.IGNORECASE
)


YEAR_PATTERN = re.compile(
    r"\b(?:19|20)\d{2}"
    r"\s*(?:-|–|—|to)\s*"
    r"(?:(?:19|20)\d{2}|present|current|ongoing|active)\b",
    re.IGNORECASE
)


GPA_PATTERN = re.compile(
    r"\b(gpa|cgpa)\b",
    re.IGNORECASE
)


FIELD_OF_STUDY_TERMS = {
    "computer engineering",
    "software engineering",
    "computer science",
    "information systems",
    "information technology",
    "electrical engineering",
    "electronics engineering",
    "data science",
    "artificial intelligence",
    "machine learning"
}


EDUCATION_KEYWORDS = [
    "university",
    "bachelor",
    "master",
    "phd",
    "computer engineering",
    "software engineering",
    "computer science",
    "information systems"
]



def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()

def _normalize_heading(line: str) -> str:

    text = line.strip().lower()

    # Remove common heading punctuation:
    #
    # EDUCATION:
    # --- EDUCATION ---
    # EDUCATION
    #
    text = re.sub(
        r"^[\s\-–—:|]+|[\s\-–—:|]+$",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text

def _detect_section_headings( line: str) -> list[str]:

    normalized = _normalize_heading(
        line
    )

    if not normalized:
        return []

    # Section-heading lines should remain short.
    # This prevents normal prose from being interpreted
    # as a group of headings.
    if len(normalized) > 70:
        return []

    if len(normalized.split()) > 8:
        return []

    matches = []

    # Work on a copy so we can remove recognized headings
    # and verify that nothing except separators remains.
    remaining = normalized

    heading_candidates = []

    for (
        section_name,
        headings
    ) in SECTION_HEADINGS.items():

        for heading in headings:

            heading_candidates.append(
                (
                    section_name,
                    heading
                )
            )

    # Longest phrases first:
    # "technical skills" before "skills"
    heading_candidates.sort(
        key=lambda item:
            len(item[1]),
        reverse=True
    )

    for (
        section_name,
        heading
    ) in heading_candidates:

        pattern = (
            r"(?<!\w)"
            + re.escape(heading)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            remaining,
            flags=re.IGNORECASE
        ):

            remaining = re.sub(
                pattern,
                " ",
                remaining,
                count=1,
                flags=re.IGNORECASE
            )

            if section_name not in matches:

                matches.append(
                    section_name
                )

    # Allow separators/connectors commonly found
    # between headings in multi-column PDFs.
    remaining = re.sub(
        r"\band\b",
        " ",
        remaining,
        flags=re.IGNORECASE
    )

    remaining = re.sub(
        r"[\s|/&,:;\-–—]+",
        " ",
        remaining
    ).strip()

    # If ordinary words remain, this was not purely
    # a section-heading line.
    if remaining:
        return []

    return matches

def _detect_section_heading( line: str) -> str | None:

    headings = _detect_section_headings(
        line
    )

    # split_cv_sections should only choose a current
    # section when exactly one heading is present.
    #
    # For a multi-column line like:
    #
    # EDUCATION LANGUAGES
    #
    # assigning all following interleaved lines to
    # either one would be incorrect.
    if len(headings) != 1:
        return None

    return headings[0]

def _deduplicate_preserve_order( items: list[str]) -> list[str]:
    """
    Remove duplicate strings while preserving their
    original order.

    Comparison is case-insensitive.
    """

    result = []
    seen = set()

    for item in items:

        cleaned = item.strip()

        if not cleaned:
            continue

        key = cleaned.lower()

        if key in seen:
            continue

        seen.add(key)
        result.append(cleaned)

    return result

def split_cv_sections( cv_text: str) -> dict[str, list[str]]:

    sections = {
        section: []
        for section in SECTION_HEADINGS
    }

    current_section = None

    for raw_line in cv_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        detected_section = ( _detect_section_heading(line))

        if detected_section:

            current_section = (
                detected_section
            )

            continue

        if current_section:

            sections[
                current_section
            ].append(line)

    return sections

def extract_email(cv_text: str) -> str | None:
    
    match = re.search( r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",  cv_text)

    return match.group(0) if match else None

def extract_phone( cv_text: str) -> str | None:

    candidates = re.finditer(
        r"(?<!\d)"
        r"(?:\+?\d[\d\s\-().]{7,}\d)"
        r"(?!\d)",
        cv_text
    )

    for match in candidates:

        candidate = match.group(0).strip()

        digits = re.sub(
            r"\D",
            "",
            candidate
        )

        # Normal international phone numbers
        # generally contain 10-15 digits.
        #
        # This also prevents year ranges such as:
        # 2023-2027
        # from being interpreted as phone numbers.
        if 10 <= len(digits) <= 15:

            return candidate

    return None

def extract_certifications( cv_text: str) -> list[str]:
    """
    Extract certifications from the Certifications section.

    The extractor keeps the original certification wording
    instead of trying to infer certificate names or providers.
    """

    lines = _extract_section_lines_with_blanks(
        cv_text,
        "certifications"
    )

    if not lines:
        return []

    certifications = []

    for line in lines:

        cleaned = _clean_project_line(
            line
        ).strip()

        if not cleaned:
            continue

        # Some CVs put multiple certificates on one line
        # separated by semicolons.
        parts = re.split(
            r"\s*[;|]\s*",
            cleaned
        )

        for part in parts:

            part = part.strip()

            if part:
                certifications.append(
                    part
                )

    return _deduplicate_preserve_order(
        certifications
    )

def extract_languages( cv_text: str) -> list[str]:
    """
    Extract languages from the Languages section.

    Proficiency information is preserved when present.

    Examples:
        English - C1
        Turkish (B1)
        Arabic - Native
    """

    lines = _extract_section_lines_with_blanks(
        cv_text,
        "languages"
    )

    if not lines:
        return []

    languages = []

    for line in lines:

        cleaned = _clean_project_line(
            line
        ).strip()

        if not cleaned:
            continue

        # Languages are commonly written either one per line:
        #
        # English - C1
        # Turkish - B1
        #
        # or in one line:
        #
        # English, Turkish, Arabic
        #
        # so commas are safe/useful separators here.
        parts = re.split(
            r"\s*[,;|]\s*",
            cleaned
        )

        for part in parts:

            part = part.strip()

            if part:
                languages.append(
                    part
                )

    return _deduplicate_preserve_order(
        languages
    )
    
def extract_education(cv_text: str) -> list[str]:

    sections = split_cv_sections( cv_text)

    education_section = sections.get( "education",  [])

    results = []


    # =====================================================
    # CASE 1:
    # CV has a proper Education section
    # =====================================================

    if education_section:

        for line in education_section:

            lower_line = line.lower()

            looks_like_education = (
                DEGREE_PATTERN.search(line)
                or
                INSTITUTION_PATTERN.search(line)
                or
                YEAR_PATTERN.search(line)
                or
                GPA_PATTERN.search(line)
                or
                any(
                    field
                    in lower_line
                    for field
                    in FIELD_OF_STUDY_TERMS
                )
            )

            if looks_like_education:

                cleaned = line.strip()

                if (
                    cleaned
                    and
                    cleaned not in results
                ):
                    results.append(
                        cleaned
                    )


        if results:
            return results


    # =====================================================
    # CASE 2:
    # No recognizable Education section.
    #
    # Use a STRICT fallback.
    # =====================================================

    for raw_line in cv_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # Outside a dedicated education section,
        # only strong evidence is accepted.
        #
        # We deliberately DO NOT accept something
        # merely because it contains
        # "Computer Engineering".
        strong_education_evidence = (
            DEGREE_PATTERN.search(line)
            or
            INSTITUTION_PATTERN.search(line)
        )

        if not strong_education_evidence:
            continue


        # Avoid obvious project descriptions.
        lower_line = line.lower()

        project_indicators = (
            " project",
            "team project",
            "developed ",
            "built ",
            "implemented ",
            "srs",
            "uml"
        )

        if any(
            indicator in lower_line
            for indicator
            in project_indicators
        ):
            continue


        if line not in results:

            results.append(
                line
            )


    return results

def _extract_section_lines_with_blanks(
    cv_text: str,
    target_section: str
) -> list[str]:
    """
    Extract one CV section while preserving blank lines.

    split_cv_sections() is good for simple section content,
    but project extraction needs blank lines because they can
    separate individual projects.
    """

    lines = []
    inside_target = False
    found_target = False

    for raw_line in cv_text.splitlines():

        stripped = raw_line.strip()

        detected_section = None

        if stripped:
            detected_section = _detect_section_heading(
                stripped
            )

        if detected_section:

            if inside_target:
                # Another recognized section started,
                # therefore the target section has ended.
                break

            if detected_section == target_section:
                inside_target = True
                found_target = True

            continue

        if inside_target:
            lines.append(stripped)

    if not found_target:
        return []

    # Remove unnecessary blank lines from the
    # beginning and end.
    while lines and not lines[0]:
        lines.pop(0)

    while lines and not lines[-1]:
        lines.pop()

    return lines

def _clean_project_line(line: str) -> str:
    """
    Remove common CV bullet characters from the beginning
    of a project description line.
    """

    return re.sub(
        r"^[\s•●▪◦*\-–—]+\s*",
        "",
        line
    ).strip()

def _looks_like_project_title(line: str) -> bool:
    """
    Conservative heuristic for deciding whether a line is
    probably a project title.

    It intentionally avoids guessing when the first line
    looks like a normal project-description sentence.
    """

    original = line.strip()

    if not original:
        return False

    # Bullet points are normally descriptions,
    # not project titles.
    if re.match(
        r"^[•●▪◦*\-–—]",
        original
    ):
        return False

    cleaned = _clean_project_line(
        original
    )

    if not cleaned:
        return False

    # Long lines are more likely descriptions.
    if len(cleaned) > 120:
        return False

    if len(cleaned.split()) > 15:
        return False

    # Normal sentences usually end with punctuation.
    if cleaned.endswith((".", ";")):
        return False

    first_word = (
        cleaned
        .split()[0]
        .lower()
        .rstrip(":")
    )

    # A line such as
    #
    # "Developed a REST API using FastAPI"
    #
    # should be treated as a description,
    # not as the project title.
    if first_word in _PROJECT_ACTION_VERBS:
        return False

    return True

def _split_project_blocks(lines: list[str]) -> list[list[str]]:
    """
    Split a Projects section into individual project blocks.

    A blank line followed by something that looks like a new
    project title starts a new project.

    This is intentionally conservative so that description
    paragraphs are not accidentally turned into separate
    projects.
    """

    blocks = []

    current_block = []

    blank_seen = False

    for line in lines:

        if not line:
            blank_seen = True
            continue

        if (
            current_block
            and
            blank_seen
            and
            _looks_like_project_title(line)
        ):
            blocks.append(
                current_block
            )

            current_block = [
                line
            ]

        else:
            current_block.append(
                line
            )

        blank_seen = False

    if current_block:
        blocks.append(
            current_block
        )

    return blocks

def extract_projects( cv_text: str) -> list[dict]:
    """
    Extract structured projects from the Projects section.

    Each project contains:

        title
        description
        technologies

    The title may be None when the CV only contains project
    descriptions and does not provide a clear project name.
    """

    section_lines = (
        _extract_section_lines_with_blanks(
            cv_text,
            "projects"
        )
    )

    if not section_lines:
        return []

    blocks = _split_project_blocks(
        section_lines
    )

    projects = []

    for block in blocks:

        if not block:
            continue

        cleaned_lines = [
            _clean_project_line(line)
            for line in block
            if line.strip()
        ]

        cleaned_lines = [
            line
            for line in cleaned_lines
            if line
        ]

        if not cleaned_lines:
            continue

        first_raw_line = block[0]

        if _looks_like_project_title(
            first_raw_line
        ):

            title = (
                cleaned_lines[0]
                .rstrip(":")
                .strip()
            )

            description_lines = (
                cleaned_lines[1:]
            )

        else:

            # Do not invent a project name.
            title = None

            description_lines = (
                cleaned_lines
            )

        description = " ".join(
            description_lines
        ).strip()

        project_text = " ".join(
            cleaned_lines
        )

        technologies = extract_skills(
            project_text
        )

        projects.append({
            "title": title,
            "description": description,
            "technologies": technologies
        })

    return projects

def extract_years_of_experience(cv_text: str):
    """
    Estimate total professional experience in years.

    Supports:
    - Explicit statements such as "3 years of experience"
    - Date ranges such as "2021 - 2024"
    - Open-ended ranges such as "2024 - Present"

    Education dates are intentionally excluded.
    """

    text = cv_text or ""

    # ---------------------------------------------------------
    # 1. Look for an explicit experience statement
    # ---------------------------------------------------------
    explicit_pattern = re.compile(
        r"\b(\d+(?:\.\d+)?)\s*\+?\s*years?\s+"
        r"(?:of\s+)?(?:professional\s+)?experience\b",
        re.IGNORECASE,
    )

    explicit_matches = explicit_pattern.findall(text)

    if explicit_matches:
        return max(float(value) for value in explicit_matches)

    # ---------------------------------------------------------
    # 2. Isolate the Experience section
    # ---------------------------------------------------------
    experience_match = re.search(
        r"(?is)"
        r"(?:^|\n)\s*"
        r"(experience|work experience|professional experience|employment)"
        r"\s*:?\s*\n"
        r"(.*?)(?=\n\s*(education|projects?|skills?|certifications?|languages?|"
        r"technical skills|achievements?|awards?)\s*:?\s*\n|\Z)",
        text,
    )

    if not experience_match:
        return None

    experience_text = experience_match.group(2)

    # ---------------------------------------------------------
    # 3. Extract year ranges from Experience only
    # ---------------------------------------------------------
    year_range_pattern = re.compile(
        r"\b(19\d{2}|20\d{2})\s*[-–—]\s*"
        r"(19\d{2}|20\d{2}|present|current|now)\b",
        re.IGNORECASE,
    )

    ranges = year_range_pattern.findall(experience_text)

    if not ranges:
        return None

    current_year = date.today().year
    intervals = []

    for start, end in ranges:
        start_year = int(start)

        if end.lower() in {"present", "current", "now"}:
            end_year = current_year
        else:
            end_year = int(end)

        # Ignore invalid ranges.
        if end_year < start_year:
            continue

        intervals.append((start_year, end_year))

    if not intervals:
        return None

    # ---------------------------------------------------------
    # 4. Merge overlapping employment periods
    # ---------------------------------------------------------
    intervals.sort()

    merged = []

    for start, end in intervals:
        if not merged:
            merged.append([start, end])
            continue

        previous_start, previous_end = merged[-1]

        if start <= previous_end:
            merged[-1][1] = max(previous_end, end)
        else:
            merged.append([start, end])

    total_years = sum(
        end - start
        for start, end in merged
    )

    return round(float(total_years), 2)

# def extract_years_of_experience( cv_text: str) -> float | None:

#     patterns = [
#         r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
#         r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience"
#     ]

#     lower = cv_text.lower()

#     for pattern in patterns:
#         match = re.search(pattern, lower)

#         if match:
#             return float(match.group(1))

#     return None


def extract_sections( cv_text: str) -> dict:

    found = {
        "education": False,
        "experience": False,
        "projects": False,
        "skills": False,
        "certifications": False,
        "languages": False
    }

    for raw_line in cv_text.splitlines():

        detected_sections = (
            _detect_section_headings(
                raw_line
            )
        )

        for section in detected_sections:

            if section in found:

                found[
                    section
                ] = True

    return found


def extract_profile(cv_text: str) -> dict:
    cv_text = clean_text(cv_text)

    return {
        "email": extract_email(cv_text),
        
        "phone": extract_phone(cv_text),

        "skills": extract_skills(cv_text),

        "education": extract_education(cv_text),

        "years_of_experience": extract_years_of_experience( cv_text),

        "projects": extract_projects(cv_text),
        
        "certifications":extract_certifications( cv_text),

        "languages": extract_languages( cv_text),
        
        "sections": extract_sections(cv_text),

        "word_count": len(cv_text.split())
    }