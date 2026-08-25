import re
from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

def normalize_string(text: str) -> str:
    string = re.sub(r"^\d+\.\d+\s", "", text)
    return string

def extract_category_number(text: str) -> str | None:
    match = re.match(r"^\d+\.\d+", text)
    return match.group() if match else None

class DescriptionContainsNoCategoryName(Rule):
    name = "description_contains_no_category_name"
    weight = 1.0

    def evaluate(self, entry: Entry):
        category_names = [category.name for category in entry.categories]
        category_numbers = [extract_category_number(category.name) for category in entry.categories]
        category_numbers = [num for num in category_numbers if num is not None]
        normalized_description = normalize_string(entry.description or "")
        found_categories = [num for num in category_numbers if num in entry.description]
        total_category_names = len(category_names)

        severity = len(found_categories) / total_category_names
        
        return RuleResult(severity=severity, reason=f"description contains category names {found_categories}")