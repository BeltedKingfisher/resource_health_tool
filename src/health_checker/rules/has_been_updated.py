from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult
from datetime import datetime

class HasBeenUpdated(Rule):
    name = "has_been_updated"
    weight = 4.0

    def evaluate(self, entry):                       
        severity = 1.0 if entry.created_at.date() == entry.updated_at.date() else 0.0
        reason_text = "has never been updated" if severity > 0 else "has been updated at least once"

        return RuleResult(severity=severity, reason=f"resource {reason_text} - created {entry.created_at.date()}, updated {entry.updated_at.date()}")