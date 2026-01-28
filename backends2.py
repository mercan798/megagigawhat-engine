import math
from typing import Dict


def calculate_storage_cost(
    amount: float,
    unit: str,
    months: int,
    storage_class: str,
    retrieval_gb: float = 0.0,
    egress_gb: float = 0.0,
    requests_count: int = 0,
    tb_to_gb: int = 1024,  # invoice-grade is often 1000; keep 1024 if you want TiB-style
) -> Dict[str, float]:
    """
    Pure function. No HTTP calls.
    """
    price_per_gb_month = 0.023 if storage_class == "standard" else 0.004
    retrieval_price_per_gb = 0.02 if storage_class == "archive" else 0.0
    request_price_per_1000 = 0.005
    egress_price_per_gb = 0.09

    u = unit.upper()
    gb = amount * (tb_to_gb if u == "TB" else 1)

    storage_cost = gb * price_per_gb_month * months
    retrieval_cost = retrieval_gb * retrieval_price_per_gb
    egress_cost = egress_gb * egress_price_per_gb
    request_cost = (requests_count / 1000) * request_price_per_1000

    total = storage_cost + retrieval_cost + egress_cost + request_cost

    return {
        "storage": round(storage_cost, 2),
        "retrieval": round(retrieval_cost, 2),
        "egress": round(egress_cost, 2),
        "requests": round(request_cost, 2),
        "total": round(total, 2),
        "monthly": round(total / months, 2) if months else round(total, 2),
        "yearly": round((total / months) * 12, 2) if months else round(total * 12, 2),
    }


def calculate_transfer_time(amount: float, unit: str, link_mbit: float) -> Dict[str, int]:
    """
    Pure function. No HTTP calls.
    Returns dict with days/hours/minutes/seconds.
    """
    u = unit.upper()
    bits = amount * (8 * 1024**3 if u == "GB" else 8 * 1024**4)
    bandwidth = link_mbit * 1_000_000
    sec = bits / bandwidth
    real_sec = math.ceil(sec)

    day = real_sec // 86400
    rem = real_sec % 86400
    hour = rem // 3600
    rem %= 3600
    minute = rem // 60
    seconds = rem % 60

    return {"days": day, "hours": hour, "minutes": minute, "seconds": seconds}
