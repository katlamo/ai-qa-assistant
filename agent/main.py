"""Run from the project root:
    python -m agent.main analyze  task.txt                                  # only requirements analysis
    python -m agent.main generate task.txt                                  # only test cases
    python -m agent.main generate task.txt --analysis results/analysis.json # test cases using a saved analysis
    python -m agent.main full     task.txt                                  # analysis + test cases + one report

The task can also be passed through stdin:  cat task.txt | python -m agent.main analyze
All output files are saved to the results/ folder.
Requires ANTHROPIC_API_KEY in the environment.
"""
import argparse
import sys
from pathlib import Path

from features.report import (
    build_analysis_report,
    build_report,
    build_test_cases_report,
)
from features.requirements_analysis import RequirementsAnalysis
from agent.qa_agent import QAAgent

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def read_task(path: str | None) -> str:
    if path:
        with open(path, encoding="utf-8") as file:
            return file.read()
    return sys.stdin.read()


def save(name: str, text: str):
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / name
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Saved to {path}")


def run_analyze(args):
    task = read_task(args.task_file)

    analysis = QAAgent().analyze_requirements(task)

    report = build_analysis_report(analysis)
    print(report)
    save("analysis.json", analysis.model_dump_json(indent=2))
    save("qa_analysis.md", report)


def run_generate(args):
    task = read_task(args.task_file)

    analysis = None
    if args.analysis:
        with open(args.analysis, encoding="utf-8") as file:
            analysis = RequirementsAnalysis.model_validate_json(file.read())

    suite = QAAgent().generate_test_cases(task, analysis)

    report = build_test_cases_report(suite)
    print(report)
    save("test_cases.json", suite.model_dump_json(indent=2))
    save("qa_test_cases.md", report)


def run_full(args):
    task = read_task(args.task_file)

    analysis, suite = QAAgent().run(task)

    report = build_report(analysis, suite)
    print(report)
    save("qa_report.md", report)


def main():
    parser = argparse.ArgumentParser(description="AI Requirements & Test Design Assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="analyze requirements only")
    analyze.add_argument("task_file", nargs="?", help="task text file (or use stdin)")
    analyze.set_defaults(func=run_analyze)

    generate = subparsers.add_parser("generate", help="generate test cases only")
    generate.add_argument("task_file", nargs="?", help="task text file (or use stdin)")
    generate.add_argument("--analysis", help="analysis.json saved by the analyze command (in results/)")
    generate.set_defaults(func=run_generate)

    full = subparsers.add_parser("full", help="analysis + test cases + one report")
    full.add_argument("task_file", nargs="?", help="task text file (or use stdin)")
    full.set_defaults(func=run_full)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
