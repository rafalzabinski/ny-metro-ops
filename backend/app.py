from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from .atis import get_nyc_airports_status
from .templates import render_index

app = FastAPI(title='NY Metro Ops')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN', '')

@app.get('/', response_class=HTMLResponse)
def home():
    return HTMLResponse(render_index(mapbox_token=MAPBOX_TOKEN))

@app.get('/api/nyc')
def nyc():
    return JSONResponse({'airports': get_nyc_airports_status(), 'status': 'Live ATIS loaded'})
