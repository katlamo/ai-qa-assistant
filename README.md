# AI Requirements & Test Design Assistant

An AI-powered QA assistant that helps analyze requirements, identify gaps, and generate test cases.

The project uses an AI agent to support QA engineers during the requirements analysis and test design stages.

## Features

- **Requirements Analysis** - analyzes user stories and acceptance criteria.
- **Gap Detection** - identifies missing information, unclear requirements, and potential inconsistencies.
- **Test Case Generation** - generates positive, negative, boundary, and edge case scenarios (up to 12 test cases per run).
- **Report Generation** - exports the results into a Markdown report.
- **Independent steps** - analysis and test case generation can be run separately or together.

## How It Works

1. The user provides a user story or task description (a plain text file or stdin).
2. The AI agent analyzes the input and identifies unclear or missing requirements.
3. Ambiguities, inconsistencies, and open questions for the Product Owner are highlighted.
4. Test cases are generated based on the available requirements and the analysis.
5. A final QA report is created.

If requirements are unclear, the agent does not guess: it lists questions for the Product Owner and marks the affected test cases as "requires clarification" instead of making assumptions.

## Tech Stack

- Python 3.10+
- Claude API (`anthropic` SDK, model `claude-haiku-5-5`)
- Pydantic (structured output schemas)

## Project Structure

```text
ai-qa-assistant/
│
├── agent/
│   ├── __init__.py
│   ├── main.py                   # CLI entry point
│   └── qa_agent.py               # QAAgent: calls the Claude API and runs the pipeline
├── features/
│   ├── __init__.py
│   ├── requirements_analysis.py  # prompt and RequirementsAnalysis schema
│   ├── test_case_generation.py   # prompt and QATestSuite / QATestCase schemas
│   └── report.py                 # Markdown report builder
├── results/                      # all generated output (git-ignored)
├── requirements.txt              # Python dependencies
├── sample.txt                    # example task input
├── .gitignore
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-api-key"   # Windows PowerShell: $env:ANTHROPIC_API_KEY="your-api-key"
```

## Usage

Run all commands from the project root. The task is a plain text file (or stdin). Analysis and test case generation can be run independently or together.

| Command | What it does | Saves |
|---|---|---|
| `python -m agent.main analyze task.txt` | Requirements analysis only | `results/analysis.json`, `results/qa_analysis.md` |
| `python -m agent.main generate task.txt` | Test cases only, without a prior analysis | `results/test_cases.json`, `results/qa_test_cases.md` |
| `python -m agent.main generate task.txt --analysis results/analysis.json` | Test cases that use a saved analysis | `results/test_cases.json`, `results/qa_test_cases.md` |
| `python -m agent.main full task.txt` | Analysis + test cases in one report | `results/qa_report.md` |

A typical two-step flow: run `analyze`, review (or edit) `results/analysis.json`, then run `generate --analysis results/analysis.json`.

The task can also be passed through stdin:

```bash
cat task.txt | python -m agent.main analyze
```

Results are printed to the console and saved to the files listed above.

## Example Input

User Story:

As a registered user, I want to reset my password using my email address so that I can regain access to my account.

## Example Output

The full report (`results/qa_report.md`) contains the analysis and the test cases; `analyze` and `generate` save only their own part. The report contains:

- Summary with counts of findings, and test cases by priority
- Requirements analysis (general assessment)
- Missing information
- Ambiguities and inconsistencies
- Questions for the Product Owner (as a checklist, with IDs M1, A1, I1, Q1 for easy reference)
- Test cases overview table, then details for each case, sorted by priority. Each test case has a type (Positive, Negative, Boundary, Edge Case), preconditions, steps, an expected result, a priority, and a "requires clarification" flag

## Limitations

- The agent generates up to 12 test cases per run and prioritizes coverage over quantity.
- Expected results are based only on the provided requirements. Unclear behavior is flagged, not invented.
- The quality of the result depends on the quality of the input.

## Possible Extensions

- Jira integration
- Confluence integration
- Automated test code generation
- Pytest integration
- Interactive mode: the agent asks follow-up questions and continues with the answers

> ⚠️ This is an experimental portfolio project, not a replacement for manual QA analysis. All results should be checked.
