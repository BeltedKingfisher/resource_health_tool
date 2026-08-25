import json
import argparse
from pprint import pprint

from health_checker.client import build_entries, filter_entries_by_status
from health_checker.rules import STATELESS_RULES
from health_checker.rules.are_links_broken import AreLinksBroken
from health_checker.scoring import score_entries, describe_rules
from health_checker.rules.base import Rule
from health_checker.reporting import write_csv_report

#run this in main to print out directory of rules with weights / deductions:
def print_rule_directory(rules: list[Rule]) -> None:
    for rule_info in describe_rules(rules):
        print(f"{rule_info['name']} (weight {rule_info['weight']}): up to -{rule_info['max_deduction']} pts")

def load_export(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
    
def parse_args():
    parser = argparse.ArgumentParser(description="Run Contentful health checks")
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of entries to print (default: 5)"
    )
    parser.add_argument(
         "--exclude-status",
         nargs="+",
         default=[],
         help="Exclude entries with this in_operation status. No default exclusions."
    )
    return parser.parse_args()

def main():
    args = parse_args()

    data = load_export("data/export.json")
    entries = build_entries(data)  
    entries = filter_entries_by_status(entries, args.exclude_status)  
    broken_link_lookup = load_export("data/broken_link_lookup.json")
    broken_links = broken_link_lookup["broken_links"]
    all_rules = STATELESS_RULES + [AreLinksBroken(broken_links)]

    scores = score_entries(entries, all_rules)
    low_scores = [s for s in scores if s.total_score < 80]
    sorted_scores = sorted(scores, key=lambda s: s.total_score)

    write_csv_report(sorted_scores, "data/outputs/health_report.csv")
    print(f"wrote {len(sorted_scores)} scored reports to data/outputs/health_report.csv")

    for i, score in enumerate(low_scores[:args.limit], start=1):
            print(f"{i}. {score.entry_name}, score: {score.total_score}. Reasons: ")
            deductions = [r for r in score.rule_result if r.severity > 0]
            for r in deductions:
                 print(f"{r.reason}")
                 


if __name__ == "__main__":
    main()


