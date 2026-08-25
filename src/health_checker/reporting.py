import csv
from pathlib import Path

from health_checker.scoring import EntryScore

def write_csv_report(scores: list[EntryScore], path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "entry_name", "total_score", "reasons"])

        for rank, score in enumerate(scores, start=1):            
            breakdown = "; ".join(
                r.reason for r in score.rule_result if r.applicable and r.severity > 0
            )
            writer.writerow([rank, score.entry_name, score.total_score, breakdown])