from typing import TypeVar

import anthropic
from pydantic import BaseModel

from features.requirements_analysis import (
    REQUIREMENTS_ANALYSIS_PROMPT,
    RequirementsAnalysis,
    build_analysis_message,
    format_analysis,
)
from features.test_case_generation import (
    TEST_CASE_GENERATION_PROMPT,
    QATestSuite,
    build_test_generation_message,
)

MODEL = "claude-haiku-5-5"

T = TypeVar("T", bound=BaseModel)


class QAAgent:
    def __init__(self, client: anthropic.Anthropic | None = None):
        self.client = client or anthropic.Anthropic()

    def _run(self, system: str, user_message: str, schema: type[T]) -> T:
        response = self.client.messages.parse(
            model=MODEL,
            max_tokens=6000,
            output_config={"effort": "low"},
            system=system,
            messages=[{"role": "user", "content": user_message}],
            output_format=schema,
        )

        if response.stop_reason == "refusal":
            raise RuntimeError(f"Request was declined: {response.stop_details}")
        if response.stop_reason == "max_tokens":
            raise RuntimeError("Response was truncated (max_tokens reached).")

        return response.parsed_output

    def analyze_requirements(self, task_description: str) -> RequirementsAnalysis:
        return self._run(
            REQUIREMENTS_ANALYSIS_PROMPT,
            build_analysis_message(task_description),
            RequirementsAnalysis,
        )

    def generate_test_cases(
        self,
        task_description: str,
        analysis: RequirementsAnalysis | None = None,
    ) -> QATestSuite:
        analysis_text = ""
        if analysis is not None:
            analysis_text = format_analysis(analysis)

        return self._run(
            TEST_CASE_GENERATION_PROMPT,
            build_test_generation_message(task_description, analysis_text),
            QATestSuite,
        )

    def run(self, task_description: str) -> tuple[RequirementsAnalysis, QATestSuite]:
        """Full pipeline: analyze requirements, then generate test cases."""
        analysis = self.analyze_requirements(task_description)
        suite = self.generate_test_cases(task_description, analysis)
        return analysis, suite
