from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/procesar")
async def procesar_archivo(archivo: UploadFile = File(...)):
    nombre_archivo = archivo.filename
    ruta_subida = os.path.join(UPLOAD_FOLDER, nombre_archivo)

    with open(ruta_subida, "wb") as f:
        f.write(await archivo.read())

    try:
        df = pd.read_excel(ruta_subida)

        # Procesamiento (puedes modificar esto)
        if pd.api.types.is_numeric_dtype(df.iloc[:, 0]):
            df["Procesado"] = df.iloc[:, 0] * 2
        else:
            df["Procesado"] = "Texto procesado"

        nombre_salida = f"resultado_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        ruta_salida = os.path.join(PROCESSED_FOLDER, nombre_salida)
        df.to_excel(ruta_salida, index=False)

        return FileResponse(ruta_salida, filename=nombre_salida, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return {"error": str(e)}
