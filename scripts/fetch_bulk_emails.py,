"""
Holt die letzten Bulk Email Actions aus Close CRM per API und schreibt sie als JSON.
Nutzt CLOSE_API_KEY aus den Umgebungsvariablen (kommt aus Github Secret).
"""

import os
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime, timezone

CLOSE_API_KEY = os.environ.get("CLOSE_API_KEY")
if not CLOSE_API_KEY:
    raise SystemExit("CLOSE_API_KEY fehlt. Als Github Secret gesetzt?")

BASE_URL = "https://api.close.com/api/v1"
AUTH_HEADER = "Basic " + base64.b64encode(f"{CLOSE_API_KEY}:".encode()).decode()

MAX_RESULTS = 100


def close_get(path, params=None):
    url = f"{BASE_URL}{path}"
    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        if query:
            url = f"{url}?{query}"
    req = urllib.request.Request(url, headers={"Authorization": AUTH_HEADER})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise SystemExit(f"Close API Fehler {e.code}: {body}")


def fetch_bulk_emails(limit=MAX_RESULTS):
    all_items = []
    skip = 0
    page_size = 100
    while len(all_items) < limit:
        data = close_get("/bulk_action/email/", {"_skip": skip, "_limit": page_size})
        batch = data.get("data", [])
        all_items.extend(batch)
        if not data.get("has_more") or not batch:
            break
        skip += page_size
    return all_items[:limit]


def fetch_users():
    data = close_get("/user/", {"_fields": "id,first_name,last_name,email"})
    return {u["id"]: u for u in data.get("data", [])}


def fetch_email_templates():
    data = close_get("/email_template/", {"_fields": "id,name"})
    return {t["id"]: t for t in data.get("data", [])}


def main():
    bulk_emails = fetch_bulk_emails(MAX_RESULTS)
    users = fetch_users()
    templates = fetch_email_templates()

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(bulk_emails),
        "users": users,
        "templates": templates,
        "bulk_emails": bulk_emails,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/bulk_emails.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"{len(bulk_emails)} Bulk Email Actions geschrieben.")


if __name__ == "__main__":
    main()
