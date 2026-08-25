import json
import asyncio
from health_checker.models import Entry
from datetime import datetime, timezone

from health_checker.client import build_entries
from health_checker.create_broken_link_batch_list import check_batch_urls

OUTPUT_PATH = "data/broken_link_lookup.json"

def load_export(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
    
def collect_urls(entries: list[Entry]) -> list[str]:
    urls = {site.url for entry in entries for site in entry.websites}
    return list(urls)

def main(): 
    data = load_export("data/export.json")
    entries = build_entries(data)
    now = datetime.now(timezone.utc).isoformat()

    urls = collect_urls(entries)
    broken_link_lookup = asyncio.run(check_batch_urls(urls))

    output = {
        "check_at": now,
        "broken_links": broken_link_lookup
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Checked {len(urls)} URLs, found {len(broken_link_lookup)} broken. Saved to {OUTPUT_PATH} at {now}")

if __name__ == "__main__":
    main()