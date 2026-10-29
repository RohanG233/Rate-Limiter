from limiter import check_request

domain = "homeops"

descriptors = [
    {"key": "rule", "value": "login"},
    {"key": "browser_id", "value": "browser_A"}
]

result = check_request(domain, descriptors)
print(result)