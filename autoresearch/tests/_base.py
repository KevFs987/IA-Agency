"""
Base utilities shared across all autoresearch test scripts.
"""
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional


@dataclass
class Assertion:
    id: str
    name: str
    weight: str  # CRITIQUE / HAUTE / MOYENNE / BASSE
    fn: Callable[[str], bool]
    reason: str = ""


@dataclass
class AssertionResult:
    id: str
    name: str
    weight: str
    passed: bool
    reason: str = ""


@dataclass
class FileResult:
    file: str
    results: List[AssertionResult]

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total else 0.0


def count_words(text: str) -> int:
    return len(text.split())


def run_batch(assertions: List[Assertion], directory: str, pattern: str = "*.md") -> dict:
    """Run all assertions against all matching files in directory."""
    path = Path(directory)
    files = list(path.glob(pattern))

    if not files:
        print(f"[autoresearch] No files found in {directory} matching {pattern}", file=sys.stderr)
        return {"files": [], "pass_rate": 0.0, "passed": 0, "total": 0, "failed_assertions": []}

    file_results: List[FileResult] = []
    all_failed: dict[str, int] = {}

    for f in sorted(files):
        content = f.read_text(encoding="utf-8")
        results = []
        for assertion in assertions:
            passed = False
            reason = ""
            try:
                passed = assertion.fn(content)
            except Exception as e:
                reason = str(e)
            result = AssertionResult(
                id=assertion.id,
                name=assertion.name,
                weight=assertion.weight,
                passed=passed,
                reason=reason if not passed else "",
            )
            results.append(result)
            if not passed:
                all_failed[assertion.id] = all_failed.get(assertion.id, 0) + 1

        file_results.append(FileResult(file=str(f), results=results))

    total_assertions = sum(fr.total for fr in file_results)
    total_passed = sum(fr.passed for fr in file_results)
    pass_rate = total_passed / total_assertions if total_assertions else 0.0

    # Sort failed assertions by frequency
    failed_sorted = sorted(all_failed.items(), key=lambda x: x[1], reverse=True)

    return {
        "files": [
            {
                "file": fr.file,
                "passed": fr.passed,
                "total": fr.total,
                "pass_rate": round(fr.pass_rate, 3),
                "results": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "weight": r.weight,
                        "passed": r.passed,
                        "reason": r.reason,
                    }
                    for r in fr.results
                ],
            }
            for fr in file_results
        ],
        "pass_rate": round(pass_rate, 3),
        "passed": total_passed,
        "total": total_assertions,
        "failed_assertions": [
            {"id": aid, "count": cnt, "rate": round(cnt / len(file_results), 3)}
            for aid, cnt in failed_sorted
        ],
    }


def main(assertions: List[Assertion], skill_name: str):
    """Parse CLI args and run the test suite."""
    args = sys.argv[1:]

    batch_dir = None
    output_json = False
    pattern = "*.md"

    i = 0
    while i < len(args):
        if args[i] == "--batch" and i + 1 < len(args):
            batch_dir = args[i + 1]
            i += 2
        elif args[i] == "--json":
            output_json = True
            i += 1
        elif args[i] == "--pattern" and i + 1 < len(args):
            pattern = args[i + 1]
            i += 2
        else:
            i += 1

    if batch_dir is None:
        # Default: look for examples in the standard location
        batch_dir = f"autoresearch/examples/{skill_name}"

    result = run_batch(assertions, batch_dir, pattern)
    result["skill"] = skill_name
    result["threshold"] = 0.85

    if output_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Human-readable summary
        pct = result["pass_rate"] * 100
        status = "PASS ✅" if result["pass_rate"] >= 0.85 else "FAIL ❌"
        print(f"\n[{skill_name}] {result['passed']}/{result['total']} assertions — {pct:.0f}% — {status}")
        if result["failed_assertions"]:
            print("\nTop failing assertions:")
            for fa in result["failed_assertions"][:3]:
                print(f"  {fa['id']} — failed {fa['count']}x ({fa['rate']*100:.0f}% of files)")
        print()

    return result
