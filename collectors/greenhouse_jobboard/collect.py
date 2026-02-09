
import time
import requests
from typing import List, Dict, Any
import urllib3

# Suppress SSL warnings (for testing only - use proper certs in production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_greenhouse_jobs(board_token: str, include_content: bool = True) -> List[Dict[str, Any]]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
    params = {"content": "true"} if include_content else {}
    try:
        # Use verify=False only for testing/dev; use proper certs in production
        r = requests.get(url, params=params, timeout=30, verify=False)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching Greenhouse jobs for {board_token}: {e}")
        return []
    
    data = r.json().get("jobs", [])
    time.sleep(0.25)
    out: List[Dict[str, Any]] = []
    for j in data:
        out.append({
            "source": "greenhouse",
            "source_board": board_token,
            "job_id": j.get("id"),
            "title": j.get("title"),
            "location": (j.get("location") or {}).get("name", ""),
            "absolute_url": j.get("absolute_url"),
            "description_html": j.get("content", ""),
            "departments": [d.get("name") for d in j.get("departments", [])],
            "offices": [o.get("name") for o in j.get("offices", [])],
        })
    return out
