from features.requirements_analysis import RequirementsAnalysis
from features.test_case_generation import QATestSuite

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def escape_cell(text: str) -> str:
    """Make text safe for a Markdown table cell."""
    return text.replace("|", "\\|").replace("\n", " ")


def sorted_cases(suite: QATestSuite) -> list:
    return sorted(suite.test_cases, key=lambda c: PRIORITY_ORDER[c.priority])


def summary_section(
    analysis: RequirementsAnalysis | None = None,
    suite: QATestSuite | None = None,
) -> str:
    lines = ["## Summary", ""]

    if analysis is not None:
        lines.append(f"- Missing information: {len(analysis.missing_information)}")
        lines.append(f"- Ambiguities: {len(analysis.ambiguities)}")
        lines.append(f"- Inconsistencies: {len(analysis.inconsistencies)}")
        lines.append(f"- Questions for Product Owner: {len(analysis.questions)}")

    if suite is not None:
        counts = {"High": 0, "Medium": 0, "Low": 0}
        need_clarification = 0
        for case in suite.test_cases:
            counts[case.priority] += 1
            if case.requires_clarification:
                need_clarification += 1

        lines.append(f"- Test cases: {len(suite.test_cases)}")
        lines.append(f"  - High: {counts['High']}")
        lines.append(f"  - Medium: {counts['Medium']}")
        lines.append(f"  - Low: {counts['Low']}")
        lines.append(f"- Need clarification: {need_clarification}")

    return "\n".join(lines) + "\n"


def findings_block(title: str, prefix: str, items: list[str], checkbox: bool = False) -> str:
    lines = [f"### {title} ({len(items)})", ""]

    if not items:
        lines.append("None.")
        return "\n".join(lines) + "\n"

    for number, item in enumerate(items, start=1):
        marker = "- [ ]" if checkbox else "-"
        lines.append(f"{marker} **{prefix}{number}.** {item}")

    return "\n".join(lines) + "\n"


def analysis_section(analysis: RequirementsAnalysis) -> str:
    parts = [
        "## Requirements Analysis",
        "",
        analysis.general_assessment.strip(),
        "",
        findings_block("Missing information", "M", analysis.missing_information),
        findings_block("Ambiguities", "A", analysis.ambiguities),
        findings_block("Inconsistencies", "I", analysis.inconsistencies),
        findings_block("Questions for Product Owner", "Q", analysis.questions, checkbox=True),
    ]
    return "\n".join(parts)


def test_case_details(number: int, case) -> str:
    lines = [f"### TC-{number:02d}: {case.title}", ""]
    lines.append(f"- Type: {case.test_type}")
    lines.append(f"- Priority: {case.priority}")
    if case.requires_clarification:
        lines.append("- Requires clarification with the Product Owner")
    lines.append("")

    if case.preconditions:
        lines.append("**Preconditions**")
        lines.append("")
        for item in case.preconditions:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("**Steps**")
    lines.append("")
    for index, step in enumerate(case.steps, start=1):
        lines.append(f"{index}. {step}")
    lines.append("")

    lines.append(f"**Expected result:** {case.expected_result}")
    lines.append("")
    return "\n".join(lines)


def test_cases_section(suite: QATestSuite) -> str:
    cases = sorted_cases(suite)

    lines = ["## Test Cases", "", "### Overview", ""]
    lines.append("| ID | Title | Type | Priority | Need clarification |")
    lines.append("|---|---|---|---|---|")
    for number, case in enumerate(cases, start=1):
        clarification = "Yes" if case.requires_clarification else "No"
        lines.append(
            f"| TC-{number:02d} | {escape_cell(case.title)} | {case.test_type} "
            f"| {case.priority} | {clarification} |"
        )

    lines.append("")
    lines.append("### Details")
    lines.append("")
    for number, case in enumerate(cases, start=1):
        lines.append(test_case_details(number, case))

    return "\n".join(lines)


def build_analysis_report(analysis: RequirementsAnalysis) -> str:
    parts = [
        "# Requirements Analysis Report",
        "",
        summary_section(analysis=analysis),
        analysis_section(analysis),
    ]
    return "\n".join(parts)


def build_test_cases_report(suite: QATestSuite) -> str:
    parts = [
        "# Test Cases Report",
        "",
        summary_section(suite=suite),
        test_cases_section(suite),
    ]
    return "\n".join(parts)


def build_report(
    analysis: RequirementsAnalysis,
    suite: QATestSuite,
) -> str:
    parts = [
        "# QA Report",
        "",
        summary_section(analysis=analysis, suite=suite),
        analysis_section(analysis),
        test_cases_section(suite),
    ]
    return "\n".join(parts)
