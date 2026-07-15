"""
Holt alle Opportunities aus Close CRM per API und schreibt sie als JSON.
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


def fetch_all_opportunities():
    all_opps = []
    skip = 0
    limit = 100
    while True:
        data = close_get("/opportunity/", {"_skip": skip, "_limit": limit, "_fields": "id,lead_id,lead_name,contact_id,contact_name,user_id,user_name,status_id,status_label,status_type,pipeline_id,value,value_period,value_formatted,note,close_date,date_created,date_updated,date_won,confidence,custom"})
        batch = data.get("data", [])
        all_opps.extend(batch)
        if not data.get("has_more"):
            break
        skip += limit
    return all_opps


def fetch_pipelines():
    data = close_get("/pipeline/")
    return data.get("data", [])


def fetch_leads_for_opportunities(opportunities):
    """Holt Lead-Namen fuer alle beteiligten lead_ids in Bulk, wo moeglich."""
    lead_ids = sorted({o["lead_id"] for o in opportunities if o.get("lead_id")})
    leads = {}
    for lead_id in lead_ids:
        try:
            lead = close_get(f"/lead/{lead_id}/", {"_fields": "id,name,contacts,status_label"})
            leads[lead_id] = lead
        except SystemExit:
            continue
    return leads


def main():
    opportunities = fetch_all_opportunities()
    pipelines = fetch_pipelines()
    leads = fetch_leads_for_opportunities(opportunities)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(opportunities),
        "pipelines": pipelines,
        "leads": leads,
        "opportunities": opportunities,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/opportunities.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"{len(opportunities)} Opportunities geschrieben.")


if __name__ == "__main__":
    main()
