import re
from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

def normalize_digits(text: str) -> str:
    digits = re.sub(r"\D", "", text)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits

class DescriptionContainsNoPhoneNumber(Rule):
    name = "description_contains_no_phone_number"
    weight = 1.0

    def evaluate(self, entry: Entry):
        phone_numbers = [phone_number.number for phone_number in entry.phone_numbers]
        normalized_description = normalize_digits(entry.description or "")
        found_numbers = [number for number in phone_numbers if normalize_digits(number) in normalized_description]
        total_phone_numbers = len(phone_numbers)
        if total_phone_numbers == 0:
            return RuleResult(severity=0.0, reason="No numbers to check", applicable=False)
        
        severity = len(found_numbers) / total_phone_numbers
        
        return RuleResult(severity=severity, reason=f"description contains phone numbers {found_numbers}")