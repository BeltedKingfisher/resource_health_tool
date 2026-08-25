from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

class PhoneNumbersHaveDescription(Rule):
    name = "phone_numbers_have_description"
    weight = 1.0

    def evaluate(self, entry):
        total_phone_numbers = len(entry.phone_numbers)
        if total_phone_numbers == 0:
            return RuleResult(severity=0.0, reason="No phone numbers to check", applicable=False)
        
        description_missing = [number.number for number in entry.phone_numbers if not number.description]        
        severity = len(description_missing) / total_phone_numbers
        
        reason_text = f"These numbers need descriptions {description_missing}"
        return RuleResult(severity=severity, reason=reason_text)