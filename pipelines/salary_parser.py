
import re
from decimal import Decimal
from typing import Optional, Dict, Any

C_SIGN = {"₹": "INR", "$": "USD", "€": "EUR", "£": "GBP"}
FX = {"INR->USD": Decimal("0.012")}  # replace with daily FX table

def parse_salary(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None
    t = text.replace(",", "").lower()
    m = re.search(r"(₹|\$|€|£)?\s?(\d+(?:\.\d+)?)\s*(?:-|to)?\s*(₹|\$|€|£)?\s?(\d+(?:\.\d+)?)?\s*(lpa|year|per annum|month|hour)", t)
    if not m:
        return None
    c1, v1, c2, v2, unit = m.groups()
    cur = C_SIGN.get(c1 or c2 or "₹", "INR")
    lo = Decimal(v1)
    hi = Decimal(v2 or v1)
    if unit == "month":
        lo, hi = lo * 12, hi * 12
    return {"currency": cur, "pay_type": "year", "min": float(lo), "max": float(hi)}
