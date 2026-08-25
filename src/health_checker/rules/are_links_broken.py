from health_checker.models import Entry
from health_checker.rules.base import Rule, RuleResult


class AreLinksBroken(Rule):
    name = "are_links_broken"
    weight = 4.0

    def __init__(self, broken_links: dict):
        self.broken_links = broken_links

    def evaluate(self, entry: Entry) -> RuleResult:
        total_links = len(entry.websites)
        if total_links == 0:
            return RuleResult(severity=0.0, reason="No links to check", applicable=False)
        
        broken_for_entry = {
            site.url: self.broken_links[site.url]
            for site in entry.websites
            if site.url in self.broken_links
            and self.broken_links[site.url]["status"] == 404
        }
        severity = len(broken_for_entry) / total_links

        details = "; ".join(
        f"{url} (status={info['status']}, error={info['error']})"
        for url, info in broken_for_entry.items()
        )

        reason = (
        f"entry has {len(broken_for_entry)} non-working links: {details}"
        if broken_for_entry
        else "entry has 0 non-working links"
        )
        
        
        return RuleResult(severity=severity, reason=reason)