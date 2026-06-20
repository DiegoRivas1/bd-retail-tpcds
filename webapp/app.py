# app.py
# Backend FastAPI: sirve el dashboard y expone los endpoints del agente.
# Uso: uvicorn webapp.app:app --host 0.0.0.0 --port 8000

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from agentic.agente import responder

app = FastAPI(title="Retail Analytics — BigData 2026A")

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


class PreguntaRequest(BaseModel):
    pregunta: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/consulta")
async def consulta(body: PreguntaRequest):
    """
    Recibe una pregunta en lenguaje natural,
    la procesa a traves del pipeline agéntico
    y retorna el resultado como JSON.
    """
    if not body.pregunta.strip():
        return JSONResponse(
            status_code=400,
            content={"exito": False, "mensaje": "La pregunta no puede estar vacia."},
        )

    resultado = responder(body.pregunta)
    return JSONResponse(content=resultado)


@app.get("/health")
async def health():
    return {"estado": "ok"}
