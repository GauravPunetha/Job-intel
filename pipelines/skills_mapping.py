
import json, re
from collections import defaultdict
from typing import List, Dict

with open("taxonomy/skills_seed.json", "r", encoding="utf-8") as f:
    CANON = json.load(f)

ALIAS = {alias.lower(): (canon, meta.get("jsc_id", ""))
         for canon, meta in CANON.items()
         for alias in [canon] + meta.get("aliases", [])}

def extract_skills(text: str) -> List[Dict[str, str]]:
    text_l = (text or "").lower()
    hits = defaultdict(int)
    for alias, (canon, jsc) in ALIAS.items():
        # Use word boundaries for more accurate matching
        pattern = rf"\b{re.escape(alias)}\b"
        if re.search(pattern, text_l):
            hits[(canon, jsc)] += 1
    return [{"skill_canonical": c, "jsc_id": j, "freq": n} for (c, j), n in hits.items()]
