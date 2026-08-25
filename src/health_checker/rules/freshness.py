from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult
from datetime import datetime, timezone

class Freshness(Rule):
    name = "freshness"
    weight = 3.0

    def evaluate(self, entry):  
        cutoff = datetime(2025, 1, 1, tzinfo=timezone.utc)                     
        severity = 1.0 if entry.updated_at < cutoff else 0
        reason_text = "last updated before 2025" if severity > 0 else "has been updated since 2025"

        return RuleResult(severity=severity, reason=f"resource {reason_text} - updated {entry.updated_at.date()}")