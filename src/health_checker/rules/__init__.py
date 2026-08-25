# rules/__init__.py

from health_checker.rules.phone_number_exists import PhoneNumberExists
from health_checker.rules.phone_numbers_have_description import PhoneNumbersHaveDescription
from health_checker.rules.has_been_updated import HasBeenUpdated
from health_checker.rules.freshness import Freshness
from health_checker.rules.links_exist import LinksExist
from health_checker.rules.links_have_description import LinksHaveDescription
from health_checker.rules.description_contains_no_phone_numbers import DescriptionContainsNoPhoneNumber
from health_checker.rules.description_contains_no_websites import DescriptionContainsNoWebsites
from health_checker.rules.all_caps_check import AllCapsCheck
from health_checker.rules.description_length import DescriptionLength
# NOTE: archive_description_contains_no_category_name intentionally excluded — rule is partially useful, but needs more use cases
# from health_checker.rules.are_links_broken import AreLinksBroken  -- special case, see below

STATELESS_RULES = [
    PhoneNumberExists(),
    PhoneNumbersHaveDescription(),
    HasBeenUpdated(),
    Freshness(),
    LinksExist(),
    LinksHaveDescription(),
    DescriptionContainsNoPhoneNumber(),
    DescriptionContainsNoWebsites(),
    AllCapsCheck(),
    DescriptionLength(),
]