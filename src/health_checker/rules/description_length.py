import re
from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

class DescriptionLength(Rule):
    name = "description_length"
    weight = 3.0

    def evaluate(self, entry: Entry):
        word_count = len((entry.description or "").split())
        desired_length = 50
        
        severity = 1.0 if word_count < desired_length else 0
        return RuleResult(severity=severity, reason=f"Description word count: {word_count}")