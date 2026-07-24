from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .atis import get_lga_status
from .templates import INDEX_HTML

app = FastAPI(title="NY Metro Ops")
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "assets")), name="assets")


@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(INDEX_HTML)


@app.get("/api/lga")
def lga():
    try:
        return JSONResponse(get_lga_status())
    except Exception as exc:
        return JSONResponse(
            {
                "airport": "KLGA",
                "status": f"Failed to load ATIS: {exc}",
                "updated_at": None,
                "raw_atis": None,
            },
            status_code=502,
        )
