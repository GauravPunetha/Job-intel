
import requests
from typing import List, Dict, Any
import urllib3

# Suppress SSL warnings (development only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_lever_jobs(company_shortname: str) -> List[Dict[str, Any]]:
    url = f"https://api.lever.co/v0/postings/{company_shortname}"
    r = requests.get(url, params={"mode": "json"}, timeout=30, verify=False)
    r.raise_for_status()
    jobs = r.json()
    out: List[Dict[str, Any]] = []
    for j in jobs:
        out.append({
            "source": "lever",
            "company": company_shortname,
            "job_id": j.get("id"),
            "title": j.get("text"),
            "location": (j.get("categories") or {}).get("location", ""),
            "department": (j.get("categories") or {}).get("department", ""),
            "work_type": (j.get("categories") or {}).get("commitment", ""),
            "url": j.get("hostedUrl"),
            "description_html": j.get("description", ""),
        })
    return out
