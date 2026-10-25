
import json
from main import lambda_handler

with open("event.json") as file:
    event = json.load(file)

response = lambda_handler(event, None)

print("Status:", response["statusCode"])
print("Response:")

print(json.dumps(
    json.loads(response["body"]),
    indent=4,
    ensure_ascii=False
))
