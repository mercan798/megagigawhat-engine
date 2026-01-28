from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import markdown
import uvicorn


def read_file(filename: str) -> str:
    p = Path(filename)
    if not p.exists():
        return f"# Not Found\n`{filename}` was not found."
    return p.read_text(encoding="utf-8")


def read_html_file(filename: str) -> str:
    """Read HTML file"""
    p = Path(filename)
    if not p.exists():
        return f"<!-- File not found: {filename} -->"
    return p.read_text(encoding="utf-8")


def md_html_from_text(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=["fenced_code", "tables"])


def render_md_page(title: str, filename: str) -> HTMLResponse:
    md_text = read_file(filename)
    body_html = md_html_from_text(md_text)
    template = read_html_file("templates/page_template.html")
    html = template.format(title=title, body_html=body_html)
    return HTMLResponse(html)


app = FastAPI()


@app.get("/myapi")
def my_api(request: Request):
    """Get client IP address from reverse proxy headers"""
    
    def is_public_ip(ip_str: str) -> bool:
        """Check if IP is public (not private/local)"""
        if not ip_str or ip_str == "unknown":
            return False
        # Filter out private IPs
        if ip_str.startswith(("127.", "10.", "192.168.", "172.16.", "172.17.", 
                              "172.18.", "172.19.", "172.20.", "172.21.", "172.22.",
                              "172.23.", "172.24.", "172.25.", "172.26.", "172.27.",
                              "172.28.", "172.29.", "172.30.", "172.31.", "::1", "localhost")):
            return False
        return True
    
 
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        ips = [ip.strip() for ip in x_forwarded_for.split(",")]
        for ip in ips:
            if is_public_ip(ip):
                return JSONResponse(
                    {"ip": ip},
                    headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
                )
    
   
    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip and is_public_ip(cf_ip):
        return JSONResponse(
            {"ip": cf_ip},
            headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
        )
    
  
    real_ip = request.headers.get("x-real-ip")
    if real_ip and is_public_ip(real_ip):
        return JSONResponse(
            {"ip": real_ip},
            headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
        )
    
  
    client_ip = request.client.host if request.client else None
    if client_ip and is_public_ip(client_ip):
        return JSONResponse(
            {"ip": client_ip},
            headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
        )
    
   
    return JSONResponse(
        {"ip": "unavailable", "message": "Your IP address could not be reliably detected."},
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


@app.get("/contact")
def contact_page():
    return render_md_page("Contact — Mega Giga What?", "contact.md")


@app.get("/blog")
def blog_page():
    return render_md_page("Blog — Mega Giga What?", "blog.md")


@app.get("/privacy")
def privacy_page():
    return render_md_page("Privacy Policy — Mega Giga What?", "privacy.md")


@app.get("/terms")
def terms_page():
    return render_md_page("Terms of Service — Mega Giga What?", "terms_of_service.md")


@app.get("/", response_class=HTMLResponse)
def streamlit_frame():
    """Embed Streamlit via iframe"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mega Giga What?</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        html, body {
            height: 100%;
            overflow: hidden;
        }
        iframe {
            width: 100%;
            height: 100vh;
            border: none;
            display: block;
        }
    </style>
</head>
<body>
    <iframe src="http://localhost:8501" allow="clipboard-write"></iframe>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
