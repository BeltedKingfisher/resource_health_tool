from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

class LinksHaveDescription(Rule):
    name = "links_have_description"
    weight = 1.0

    def evaluate(self, entry):        
        description_missing = [site.url for site in entry.websites if not site.description]
        total_urls = len(entry.websites)
        if total_urls == 0:
            return RuleResult(severity=0.0, reason="No links to check", applicable=False)
        
        severity = len(description_missing) / total_urls
        reason_text = f"These sites need description {description_missing}"
        return RuleResult(severity=severity, reason=reason_text)