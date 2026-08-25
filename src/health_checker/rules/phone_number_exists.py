from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

class PhoneNumberExists(Rule):
    name = "phone_number_exists"
    weight = 2.0

    def evaluate(self, entry):
        length = len(entry.phone_numbers)              
        severity = 1.0 if length == 0 else 0
        
        reason_text = f"No phone numbers associated with resource"
        return RuleResult(severity=severity, reason=reason_text)