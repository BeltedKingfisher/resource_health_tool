from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

class LinksExist(Rule):
    name = "links_exist"
    weight = 2.0

    def evaluate(self, entry):
        length = len(entry.websites)        
        severity = 1.0 if length == 0 else 0
        
        reason_text = f"No websites associated with resource"
        return RuleResult(severity=severity, reason=reason_text)