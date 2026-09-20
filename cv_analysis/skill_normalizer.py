import re


# =========================================================
# CANONICAL SKILL VOCABULARY
#
# Key   = value stored everywhere inside Growvia
# Value = accepted spellings / aliases that may appear in CVs
# =========================================================

SKILL_ALIASES = {

    # -----------------------------------------------------
    # Programming languages
    # -----------------------------------------------------

    "python": ["python", "python3"],

    "java": ["java"],

    "c": ["c"],

    "c++": ["c++","cpp"],

    "c#": ["c#", "c sharp","c-sharp"],

    "javascript": ["javascript","java script","js"],

    "typescript": ["typescript","type script","ts"],


    # -----------------------------------------------------
    # Web
    # -----------------------------------------------------

    "html": ["html", "html5"],

    "css": ["css", "css3"],

    "react": ["react", "react.js", "reactjs"],

    "angular": [  "angular", "angular.js", "angularjs"],

    "vue": [ "vue", "vue.js", "vuejs"],


    # -----------------------------------------------------
    # Backend frameworks
    # -----------------------------------------------------

    "spring": [ "spring", "spring framework"],

    "spring boot": [ "spring boot",  "springboot"],

    "django": ["django"],

    "flask": ["flask"],

    "fastapi": [ "fastapi", "fast api"],

    "node.js": [ "node.js", "nodejs", "node js"],

    "express": [ "express", "express.js","expressjs"],

    ".net": [ ".net",  "dotnet"],

    "asp.net": [ "asp.net", "asp net"],


    # -----------------------------------------------------
    # Databases
    # -----------------------------------------------------

    "sql": [ "sql"],

    "mysql": [ "mysql", "my sql"],

    "postgresql": ["postgresql", "postgres", "postgre sql"],

    "mongodb": [ "mongodb", "mongo db"],

    "sqlite": [ "sqlite","sqlite3"],


    # -----------------------------------------------------
    # DevOps / tools
    # -----------------------------------------------------

    "docker": [  "docker"],

    "kubernetes": [ "kubernetes", "k8s"],

    # For Growvia's skill-matching purposes we normalize
    # GitHub references to the canonical "git" skill.
    "git": [ "git", "github", "git hub"],


    # -----------------------------------------------------
    # Cloud
    # -----------------------------------------------------

    "aws": [ "aws",  "amazon web services"],

    "azure": [ "azure", "microsoft azure"],

    "gcp": [ "gcp", "google cloud",  "google cloud platform"],


    # -----------------------------------------------------
    # AI / Data
    # -----------------------------------------------------

    "machine learning": [ "machine learning", "ml"],

    "deep learning": [ "deep learning"],

    "tensorflow": [  "tensorflow",  "tensor flow"],

    "pytorch": [ "pytorch", "py torch"],

    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],

    "pandas": [ "pandas"],

    "numpy": [ "numpy","num py"],


    # -----------------------------------------------------
    # APIs
    # -----------------------------------------------------

    "rest api": [ "rest api", "rest apis", "restful api", "restful apis","restful services"],

    "graphql": [ "graphql","graph ql"],


    # -----------------------------------------------------
    # General software engineering
    # -----------------------------------------------------

    "linux": [ "linux"],

    "uml": [ "uml"],

    "oop": [ "oop",  "object oriented programming", "object-oriented programming"],


    # -----------------------------------------------------
    # Embedded
    # -----------------------------------------------------

    "arduino": [ "arduino"],

    "esp32": [  "esp32",  "esp-32"],


    # -----------------------------------------------------
    # Design
    # -----------------------------------------------------

    "figma": [ "figma"],
    # =========================================================
# MOBILE DEVELOPMENT
# =========================================================

"kotlin": [
    "kotlin"
],

"swift": [
    "swift"
],

"android": [
    "android",
    "android sdk"
],

"ios": [
    "ios",
    "ios development"
],

"flutter": [
    "flutter"
],

"react native": [
    "react native",
    "react-native"
],


# =========================================================
# CYBERSECURITY
# =========================================================

"network security": [
    "network security"
],

"penetration testing": [
    "penetration testing",
    "pen testing",
    "pentesting"
],

"vulnerability assessment": [
    "vulnerability assessment",
    "vulnerability assessments"
],

"incident response": [
    "incident response"
],

"siem": [
    "siem"
],

"wireshark": [
    "wireshark"
],

"nmap": [
    "nmap"
],

"burp suite": [
    "burp suite",
    "burpsuite"
],


# =========================================================
# QA / TESTING
# =========================================================

"selenium": [
    "selenium"
],

"pytest": [
    "pytest"
],

"junit": [
    "junit"
],

"postman": [
    "postman"
],

"test automation": [
    "test automation",
    "automated testing",
    "automation testing"
],

"regression testing": [
    "regression testing",
    "regression tests"
],

"api testing": [
    "api testing",
    "api tests"
],


# =========================================================
# DEVOPS
# =========================================================

"ci/cd": [
    "ci/cd",
    "ci cd",
    "cicd",
    "continuous integration",
    "continuous delivery",
    "continuous deployment"
],

"github actions": [
    "github actions"
],

"jenkins": [
    "jenkins"
],

"terraform": [
    "terraform"
]
}


# =========================================================
# CREATE REVERSE LOOKUP
# alias -> canonical skill
# =========================================================

ALIAS_TO_CANONICAL = {}

for canonical, aliases in SKILL_ALIASES.items():

    for alias in aliases:

        ALIAS_TO_CANONICAL[alias.lower().strip()] = canonical


# =========================================================
# REGEX
# =========================================================

def _build_skill_pattern(alias: str) -> str:
    """
    Build a safe regex for a skill alias.

    We do not use \\b because it does not behave correctly
    for skills containing punctuation such as C++, C# and .NET.
    """

    escaped = re.escape(alias)

    # Special protection for the C language.
    #
    # Without this, "C" could accidentally match:
    # C++
    # C#
    #
    if alias.lower() == "c":

        return (
            r"(?<![A-Za-z0-9])"
            r"c"
            r"(?![A-Za-z0-9+#])"
        )

    return (
        rf"(?<![A-Za-z0-9])"
        rf"{escaped}"
        rf"(?![A-Za-z0-9])"
    )


# =========================================================
# NORMALIZE ONE SKILL
# =========================================================

def normalize_skill_name(skill: str) -> str:

    normalized = " ".join(  skill.lower().strip().split())

    return ALIAS_TO_CANONICAL.get( normalized, normalized)


# =========================================================
# NORMALIZE A LIST
# =========================================================

def normalize_skill_list( skills: list[str]) -> list[str]:

    normalized = {
        normalize_skill_name(skill)
        for skill in skills
        if skill and skill.strip()
    }

    return sorted(normalized)


# =========================================================
# EXTRACT SKILLS FROM CV TEXT
# =========================================================

def extract_skills( cv_text: str) -> list[str]:

    lower_text = cv_text.lower()

    found_skills = set()

    # -----------------------------------------------------
    # Longer aliases first.
    #
    # Example:
    #
    # "Spring Boot"
    #
    # should match:
    # spring boot
    #
    # before:
    # spring
    # -----------------------------------------------------

    alias_entries = []

    for canonical, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            alias_entries.append( ( alias,  canonical))

    alias_entries.sort( key=lambda item: len(item[0]), reverse=True)


    # Tracks locations already used by a more-specific alias.
    #
    # Example:
    #
    # "Spring Boot"
    #
    # will not later also count "Spring"
    # from the exact same text span.
    occupied_spans = []


    for alias, canonical in alias_entries:

        pattern = _build_skill_pattern(alias)

        matches = re.finditer( pattern, lower_text, flags= re.IGNORECASE)

        for match in matches:

            start, end = match.span()

            overlaps = any(
                start < existing_end
                and
                end > existing_start

                for (
                    existing_start,
                    existing_end
                )
                in occupied_spans
            )

            if overlaps:
                continue

            found_skills.add(
                canonical
            )

            occupied_spans.append(
                (
                    start,
                    end
                )
            )

            # Finding the same skill many times
            # does not change the final result.
            break


    return sorted(found_skills)