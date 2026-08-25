from dataclasses import dataclass
from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

@dataclass
class EntryScore:
    entry_id: str
    entry_name: str
    total_score: int
    rule_result: list[RuleResult]

def describe_rules(rules: list[Rule]) -> list[dict]:
    total_weight = sum(r.weight for r in rules)
    return [
        {
            "name": rule.name,
            "weight": rule.weight,
            "max_deduction": round((rule.weight / total_weight) * 100, 1)
        }
        for rule in rules
    ]

def score_entry(rules: list[Rule], entry: Entry) -> EntryScore:
    total_weight = sum(r.weight for r in rules)
    rule_results = [rule.evaluate(entry) for rule in rules]
    
    total_deduction = 0
    for rule, result in zip(rules, rule_results):
        if result.applicable:
            max_deduction = (rule.weight / total_weight) * 100
            total_deduction += max_deduction * result.severity

    total_score = max(0, 100-total_deduction)
    ...

    return EntryScore(
        entry_id=entry.id,
        entry_name=entry.name,
        total_score=total_score,
        rule_result=rule_results,
    )

def score_entries(entries: list[Entry], rules: list[Rule]) -> list[EntryScore]:
    return [score_entry(rules, entry) for entry in entries]

