from typing import Literal

from pydantic import BaseModel, Field

from features.requirements_analysis import RequirementsAnalysis

TEST_CASE_GENERATION_PROMPT = """
You are a senior QA Engineer responsible for test design.

Generate test cases based on the provided task description and requirements analysis.

Design test cases that cover:
1. Generate positive test cases for valid scenarios.
2. Generate negative test cases for invalid scenarios.
3. Identify boundary and edge cases.
4. Cover the identified requirements and risks.
5. Avoid duplicate test cases.
6. Do not invent expected behavior that is not supported by the requirements.

Each test case should include:
- A clear title.
- Preconditions, if needed.
- Test steps.
- Expected result.
- Priority (High, Medium, Low).

Use the requirements analysis to identify areas that need additional testing.
Generate up to 12 relevant test cases.

Prioritize test coverage over quantity.
Avoid duplicate or low-value test cases.

If some behavior is unclear, mark the related test cases as requiring clarification instead of making assumptions.
"""

class QATestCase(BaseModel):
    title: str = Field(description="Short and descriptive test case title")
    test_type: Literal["Positive", "Negative", "Boundary", "Edge Case"]
    preconditions: list[str] = Field(
        description="Conditions required before test execution; empty list if none"
    )
    steps: list[str] = Field(description="Clear and ordered test execution steps")
    expected_result: str = Field(
        description="Expected behavior according to the requirements"
    )
    priority: Literal["High", "Medium", "Low"]
    requires_clarification: bool = Field(
        description="True if expected behavior is unclear or requires confirmation"
    )


class QATestSuite(BaseModel):
    test_cases: list[QATestCase] = Field(description="List of generated test cases")


def build_test_generation_message(task_description: str, analysis_text: str = "") -> str:
    if not task_description.strip():
        raise ValueError("Task description cannot be empty")

    if not analysis_text.strip():
        analysis_text = "Not provided."

    return f"""
<task_description>
{task_description.strip()}
</task_description>

<requirements_analysis>
{analysis_text.strip()}
</requirements_analysis>
"""
