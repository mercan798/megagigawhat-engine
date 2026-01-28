import streamlit as st
import streamlit.components.v1 as components

def show_ip_trace():
    st.title("Your IP Information")
    components.html(
        r"""
        <div style="font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;">
          <div id="trace-card" style="
              padding: 14px;
              border: 1px solid rgba(255,255,255,.15);
              border-radius: 12px;
              color: #e8ffe8;
              background: rgba(0,0,0,.55);
              backdrop-filter: blur(8px);
              margin-bottom: 12px;
          ">
            <div style="font-size:18px; font-weight:800; margin-bottom:8px;">IP Trace</div>
            <div id="trace-meta">Detecting…</div>
          </div>

          <div id="map" style="
              height: 340px;
              border-radius: 12px;
              overflow: hidden;
              border: 1px solid rgba(255,255,255,.15);
              background: rgba(0,0,0,.35);
          "></div>
        </div>

<link rel="stylesheet"
 href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
  function esc(s){
    return (s ?? "").toString()
      .replaceAll("&","&amp;")
      .replaceAll("<","&lt;")
      .replaceAll(">","&gt;")
      .replaceAll('"',"&quot;")
      .replaceAll("'","&#039;");
  }

  function copyIP(ip){
    navigator.clipboard.writeText(ip).then(()=>{
      const el = document.getElementById("copy-status");
      el.innerText = "Copied ✓";
      setTimeout(()=> el.innerText = "", 1200);
    });
  }

  function renderCard(data){
    const ip = esc(data.ip);
    const method = esc(data.method || "unknown");

    const rows = (label, value) => value
      ? `<div style="display:flex;gap:10px;margin:4px 0;">
           <div style="width:120px;opacity:.7">${label}</div>
           <div>${esc(value)}</div>
         </div>` : "";

    document.getElementById("trace-meta").innerHTML = `
      <div style="font-size:18px;font-weight:800;margin-bottom:6px;">
        Your IP:
        <span style="color:#b7ffb7">${ip}</span>
        <button onclick="copyIP('${ip}')"
          style="margin-left:8px;padding:2px 6px;
          border-radius:6px;border:1px solid #666;
          background:#111;color:#eee;cursor:pointer;">
          Copy
        </button>
        <span id="copy-status" style="margin-left:8px;color:#9fff9f;font-size:12px;"></span>
      </div>

      <div style="margin-bottom:10px;">Detection method: <b>${method}</b></div>

      ${rows("ISP", data.isp)}
      ${rows("Org", data.org)}
      ${rows("ASN", data.asn)}
      ${rows("Country", data.country)}
      ${rows("Region", data.region)}
      ${rows("City", data.city)}
      ${rows("Timezone", data.timezone)}

      <div style="margin-top:10px;opacity:.6;font-size:12px;">
        Location is approximate (ISP-based).
      </div>
    `;
  }

  function renderMap(lat, lon, label){
    const el = document.getElementById("map");
    el.innerHTML = "";

    if (!lat || !lon){
      el.innerHTML = "<div style='padding:14px;'>No map coordinates available.</div>";
      return;
    }

    const map = L.map("map").setView([lat, lon], 7);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap"
    }).addTo(map);

    L.marker([lat, lon]).addTo(map).bindPopup(label).openPopup();
  }

  async function fetchJson(url){
    const r = await fetch(url, { cache: "no-store" });
    return await r.json();
  }

  (async ()=>{
    try{
      const data = await fetchJson("/ip-trace");
      renderCard(data);
      renderMap(Number(data.lat), Number(data.lon),
        `${data.city||""} ${data.country||""}`.trim());
    }catch(e){
      document.getElementById("trace-meta").innerText =
        "Could not detect IP trace.";
    }
  })();
</script>
        """,
        height=540,
    )

show_ip_trace()
