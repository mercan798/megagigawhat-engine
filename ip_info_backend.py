from fastapi import FastAPI, Request
import requests
import math
from typing import Tuple, Dict, Any

app = FastAPI()


def _get_client_ip(request: Request) -> Tuple[str, str]:
    h = request.headers
    for key in ("cf-connecting-ip", "x-forwarded-for", "x-real-ip"):
        val = h.get(key)
        if val:
            ip = val.split(",")[0].strip() if key == "x-forwarded-for" else val
            return ip, key

    remote = request.client.host if request.client else "unavailable"
    return remote, "request.client.host"


@app.get("/myip")
async def myip(request: Request) -> Dict[str, Any]:
    ip, method = _get_client_ip(request)
    return {"ip": ip, "method": method}


@app.get("/serverip")
async def serverip() -> Dict[str, Any]:
    r = requests.get("https://api.ipify.org?format=json", timeout=5)
    return {"ip": r.json().get("ip", "unavailable"), "method": "ipify.org"}


@app.get("/ip-trace")
async def ip_trace(request: Request) -> Dict[str, Any]:
    ip, method = _get_client_ip(request)

    geo: Dict[str, Any] = {}
    geo_error = ""
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}",
            timeout=5,
            headers={"User-Agent": "MegaGigaWhat-IP-Trace"},
        )
        if r.status_code == 200:
            geo = r.json()
            if geo.get("status") == "fail":
                geo_error = geo.get("message", "geo_lookup_failed")
        else:
            geo_error = f"geo_http_{r.status_code}"
    except Exception as e:
        geo_error = str(e)

    return {
        "ip": ip,
        "method": method,
        "host": geo.get("reverse"),
        "isp": geo.get("isp"),
        "org": geo.get("org"),
        "asn": geo.get("as"),
        "country": geo.get("country"),
        "country_code": geo.get("countryCode"),
        "region": geo.get("regionName"),
        "city": geo.get("city"),
        "lat": geo.get("lat"),
        "lon": geo.get("lon"),
        "timezone": geo.get("timezone"),
        "source": "ip-api.com",
        "geo_status": geo.get("status"),
        "geo_error": geo_error,
        "note": "Location is approximate (ISP-based geolocation)",
    }

