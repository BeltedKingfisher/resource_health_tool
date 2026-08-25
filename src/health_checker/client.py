import json
from health_checker.models import Website, Entry, Category, PhoneNumber
from datetime import datetime
from pprint import pprint

with open("data/export.json") as f:
    data = json.load(f)

def filter_resources(data: dict, content_type: str) -> list[dict] :
    return [
        entry for entry in data["entries"]
        if entry["sys"]["contentType"]["sys"]["id"] == content_type
    ]

def filter_entries_by_status(entries: list[Entry], excluded_statuses: list[str]) -> list[Entry]:
    return [
        entry for entry in entries if entry.in_operation not in excluded_statuses
    ]

def build_id_lookup(data: dict) -> dict:
    return {
        entry["sys"]["id"]: entry
        for entry in data["entries"]
    }

def build_websites(resource: dict, entries_by_id: dict) -> list[Website] :
    website_links = resource["fields"].get("websites", {}).get("en-US", [])
    resolved_websites = [
        entries_by_id[link["sys"]["id"]]
        for link in website_links
        if link["sys"]["id" ] in entries_by_id
    ]
    return [
        Website(
            id=site["sys"]["id"],
            url=site["fields"].get("url", {}).get("en-US"),
            description=site["fields"].get("description", {}).get("en-US")
        )
        for site in resolved_websites
    ]

def build_categories(resource: dict, entries_by_id: dict) -> list[Category] :
    categories = resource["fields"].get("categories", {}).get("en-US", [])
    resolved_categories = [
        entries_by_id[category["sys"]["id"]]
        for category in categories
        if category["sys"]["id"] in entries_by_id
    ]
    return [
        Category(
            id=category["sys"]["id"],
            name=category["fields"].get("name", {}).get("en-US"),
            description=category["fields"].get("description", {}).get("en-US"),
            sortNumber=category["fields"].get("sortNumber", {}).get("en-US")
        )
        for category in resolved_categories
    ]

def build_phone_numbers(resource: dict, entries_by_id: dict) -> list[PhoneNumber] :
    phone_numbers = resource["fields"].get("phoneNumbers", {}).get("en-US", [])
    resolved_phone_numbers = [
        entries_by_id[phone_number["sys"]["id"]]
        for phone_number in phone_numbers
        if phone_number["sys"]["id"] in entries_by_id
    ]
    return [
        PhoneNumber(
            id =phone_number["sys"]["id"],
            number=phone_number["fields"].get("number", {}).get("en-US"),
            extension=phone_number["fields"].get("extension", {}).get("en-US"),
            description=phone_number["fields"].get("description", {}).get("en-US")
        )
        for phone_number in resolved_phone_numbers
    ]

def build_entry(resource: dict, entries_by_id: dict) -> Entry :
    fields = resource["fields"]
    last_verified_raw = fields.get("lastVerifiedOn", {}).get("en-US")   

    return Entry(
        id=resource["sys"]["id"],
        name=fields.get("name", {}).get("en-US"),
        description=fields.get("description", {}).get("en-US"),
        search_description=fields.get("searchDescription", {}).get("en-US"),
        url_slug=fields.get("urlSlug", {}).get("en-US"),
        in_operation=fields.get("inOperation", {}).get("en-US"),
        hours=fields.get("hours", {}).get("en-US"),
        claimed_by_owner=fields.get("claimedByOwner", {}).get("en-US"),
        verified_for_accurate_info=fields.get("verifiedForAccurateInfo", {}).get("en-US"),
        last_verified_on=datetime.fromisoformat(last_verified_raw) if last_verified_raw else None,
        updated_at=datetime.fromisoformat(resource["sys"]["updatedAt"]),
        created_at=datetime.fromisoformat(resource["sys"]["createdAt"]),
        websites=build_websites(resource, entries_by_id),
        categories=build_categories(resource, entries_by_id),
        phone_numbers=build_phone_numbers(resource, entries_by_id)
    )

def build_entries(data: dict) -> list[Entry]:
    resources = filter_resources(data, "resource")
    entries_by_id = build_id_lookup(data)

    return [
        build_entry(resource, entries_by_id)
        for resource in resources
    ]
