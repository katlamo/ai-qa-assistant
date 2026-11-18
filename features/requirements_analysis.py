from pydantic import BaseModel, Field

REQUIREMENTS_ANALYSIS_PROMPT = """
You are a senior QA engineer reviewing requirements before test design.
Your findings feed test-case generation and a QA report, so they must be specific and actionable.

Analyze the complete task description provided in the input. 

The input may contain a complete task or text, including title, description, user story, acceptance criteria, and additional notes.

First, identify and understand the structure of the input. 
Do not assume that all sections are present.
Analyze the entire task, regardless of its format.

Your tasks:

1. Identify whether the requirements are clear and understandable.
2. Identify missing information, including non-functional aspects: security, input validation, error handling, limits and timeouts, performance, concurrency, accessibility, localization.
3. Find ambiguous or inconsistent requirements.
4. Identify questions that should be clarified with the Product Owner.

Analyze the entire task description, regardless of its format.
Do not assume that all requirement sections are present.
Do not invent requirements or make assumptions.

"""


class RequirementsAnalysis(BaseModel):
    general_assessment: str = Field(
        min_length=1,
        description="A two-sentence assessment of whether the requirements are clear and understandable",
    )
    missing_information: list[str] = Field(
        description="Missing details, most important first; empty list if none"
    )
    ambiguities: list[str] = Field(
        description="Unclear or ambiguous statements, quoting the text; empty list if none"
    )
    inconsistencies: list[str] = Field(
        description="Conflicting requirements, quoting both sides; empty list if none"
    )
    questions: list[str] = Field(
        description="Questions to clarify with the Product Owner; empty list if none"
    )


def build_analysis_message(task_description: str) -> str:
    if not task_description.strip():
        raise ValueError("Task description cannot be empty")

    return f"""
<task_description>
{task_description.strip()}
</task_description>
"""


def format_list(title: str, items: list[str]) -> str:
    if not items:
        return f"{title}: none"

    lines = [f"{title}:"]
    for item in items:
        lines.append(f"- {item}")
    return "\n".join(lines)


def format_analysis(analysis: RequirementsAnalysis) -> str:
    """Turn the analysis object into plain text for the next prompt."""
    parts = [
        f"General assessment: {analysis.general_assessment}",
        format_list("Missing information", analysis.missing_information),
        format_list("Ambiguities", analysis.ambiguities),
        format_list("Inconsistencies", analysis.inconsistencies),
        format_list("Questions for Product Owner", analysis.questions),
    ]
    return "\n\n".join(parts)
