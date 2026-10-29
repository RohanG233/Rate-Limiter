from limiter import check_rate_limit, user_counts, get_window
import time

while True:
    rule = None
    browser_id = None
    
    browser_id = input("\nEnter your name (or 0 to exit): ").strip()
    if browser_id == "0":
        break

    if not browser_id:
        print("Name cannot be empty.")
        continue

    rule = input("Enter a rule: ").strip()

    if rule == "0":
        break

    domain = input("Enter the domain: ").strip()

    browser_id = browser_id.lower()
    result = check_rate_limit(browser_id, rule, domain)
    print(result)

    key = (browser_id, rule)

    if key in user_counts:
        print(f"Request count: {user_counts[key]['count']}")
        window = get_window(rule)
        remaining = window - (time.time() - user_counts[key]["first_seen"])
        print(f"Time remaining in map: {max(0, remaining):.1f} seconds")

print("\nFinal map:")
print(user_counts)