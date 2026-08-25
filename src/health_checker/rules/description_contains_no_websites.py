import re
from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult

def normalize_url(text: str) -> str:
    url = re.sub(r"^https?://", "", text)
    url = re.sub(r"/$", "", text)
    return url

class DescriptionContainsNoWebsites(Rule):
    name = "description_contains_no_websites"
    weight = 1.0

    def evaluate(self, entry: Entry):
        urls = [normalize_url(website.url) for website in entry.websites]        
        found_urls = [url for url in urls if url in entry.description]
        total_urls = len(urls)
        if total_urls == 0:
            return RuleResult(severity=0.0, reason="No links to check", applicable=False)
        
        severity= len(found_urls) /total_urls
        
        return RuleResult(severity=severity, reason=f"description contains websites {found_urls}")