"""Week 0: Python Fundamentals Bootcamp — Beginner Practice Tasks."""

import csv
import json
from typing import Dict, List, Tuple, Any


def evaluate_attendance_status(attended: int, total: int) -> str:
    """Return 'ELIGIBLE' (>=75%), 'WARNING' (65% to <75%), or 'SHORTAGE' (<65%).

    If total <= 0, return 'NO_SESSIONS'.
    """
    if total <= 0:
        return "NO_SESSIONS"
    pct = (attended / total) * 100
    if pct >= 75.0:
        return "ELIGIBLE"
    elif pct >= 65.0:
        return "WARNING"
    else:
        return "SHORTAGE"


def safe_parse_float(raw_value: Any, default: float = 0.0) -> float:
    """Convert raw_value to float safely using try/except. Return default on failure."""
    try:
        return float(raw_value)
    except (ValueError, TypeError):
        return default


def analyze_pod_scores(records: List[Tuple[str, str, float]]) -> Dict[str, Any]:
    """Analyze (usn, pod_name, score) tuples using sets, dicts, and comprehensions.

    Returns a dictionary with keys:
      - 'unique_student_count': int (number of unique USNs via set)
      - 'high_scorers': List[str] (USNs with score >= 80 using a list comprehension)
      - 'pod_averages': Dict[str, float] (average score per pod rounded to 2 decimals)
    """
    unique_student_count = len({record[0] for record in records})
    high_scorers = [record[0] for record in records if record[2] >= 80.0]

    pod_scores: Dict[str, List[float]] = {}
    for _, pod_name, score in records:
        if pod_name not in pod_scores:
            pod_scores[pod_name] = []
        pod_scores[pod_name].append(score)

    pod_averages = {
        pod: round(sum(scores) / len(scores), 2)
        for pod, scores in pod_scores.items()
    }

    return {
        "unique_student_count": unique_student_count,
        "high_scorers": high_scorers,
        "pod_averages": pod_averages,
    }


def summarize_csv_to_json(csv_path: str, json_path: str) -> Dict[str, Any]:
    """Read cohort CSV using built-in csv module and export summary JSON.

    Summary dictionary must contain:
      - 'total_students': int
      - 'branches': List[str] (sorted unique branch codes)
      - 'average_score': float (rounded to 2 decimals)
    """
    total_students = 0
    branches = set()
    total_score = 0.0

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_students += 1
            if "branch" in row and row["branch"]:
                branches.add(row["branch"])
            if "score" in row and row["score"]:
                total_score += float(row["score"])

    avg_score = round(total_score / total_students, 2) if total_students > 0 else 0.0

    summary = {
        "total_students": total_students,
        "branches": sorted(list(branches)),
        "average_score": avg_score,
    }

    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary


class StudentRecord:
    """Tracks weekly evaluation scores for a single DSC recruit."""

    def __init__(self, usn: str, name: str):
        """Initialize record with uppercase USN, name, and empty scores list."""
        self.usn = usn.upper()
        self.name = name
        self.scores: List[float] = []

    def add_score(self, score: float) -> None:
        """Append a score (must be between 0 and 100; raise ValueError otherwise)."""
        if not (0.0 <= score <= 100.0):
            raise ValueError(f"Score must be between 0 and 100, got {score}")
        self.scores.append(float(score))

    def average(self) -> float:
        """Return average score rounded to 2 decimals, or 0.0 if no scores exist."""
        if not self.scores:
            return 0.0
        return round(sum(self.scores) / len(self.scores), 2)

    def is_passing(self, threshold: float = 50.0) -> bool:
        """Return True if average() >= threshold, else False."""
        return self.average() >= threshold
