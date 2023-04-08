import json
import os

with open("services.json", "r") as f:
    services = json.load(f)

SERVICES: list[str] = [service["domain"] for service in services]
FALLBACK_INSTANCES = {
    service["domain"]: service["fallback"] for service in services
}
TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]
