import time
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

DOMAIN = config["domain"]
DESCRIPTORS = config["descriptors"]

user_counts = {}



def get_limit(rule_name):
    for descriptor in DESCRIPTORS:
        if descriptor["key"] == "rule" and descriptor["value"] == rule_name:
            return descriptor["rate_limit"]["requests_per_unit"]

    return None

def get_window(rule_name):
    for descriptor in DESCRIPTORS:
        if descriptor["key"] == "rule" and descriptor["value"] == rule_name:
            unit = descriptor["rate_limit"]["unit"]

            if unit == "second":
                return 1
            elif unit == "minute":
                return 60
            elif unit == "hour":
                return 3600

    return None

def check_rate_limit(browser_id, rule, domain):
    if domain != DOMAIN:
        return {"status": "INVALID_DOMAIN"}
    
    if browser_id is None:
        return {"status" : "MISSING_BROWSER_ID"}

    if not rule:
        return {"status": "MISSING_RULE"}
    
    current_time = time.time()

    limit = get_limit(rule)

    if limit is None:
        return {"status": "INVALID_RULE"}

    key = (browser_id, rule)
    window = get_window(rule)

    # Remove the browser_id if its storage time has expired
    if key in user_counts:
        elapsed = current_time - user_counts[key]["first_seen"]

        if elapsed >= window:
            del user_counts[key]

    # If the browser_id doesn't exist, add it with a timer
    if key not in user_counts:
        user_counts[key] = {
            "count": 0,
            "first_seen": current_time
        }

    # Check rate limit
    if user_counts[key]["count"] >= limit:
        return {"status" : "OVER_LIMIT"}

    user_counts[key]["count"] += 1
    return {"status" : "OK"}


def check_request(domain, descriptors):
    rule = None
    browser_id = None

    for descriptor in descriptors:
        if descriptor["key"] == "rule":
            rule = descriptor["value"]

        elif descriptor["key"] == "browser_id":
            browser_id = descriptor["value"]

    return check_rate_limit(browser_id, rule, domain)