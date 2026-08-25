import re
from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

class AllCapsCheck(Rule):
    name = "all_caps_check"
    weight = 2.0

    def evaluate(self, entry: Entry):
        name_in_caps = entry.name.upper()
        
        severity = 1.0 if entry.name == name_in_caps else 0
        return RuleResult(severity=severity, reason=f"Name in all caps - {entry.name}")