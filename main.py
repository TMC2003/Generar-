from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from datetime import datetime

usuarios = []

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") # Le dice a FastAPI: “Busca las plantillas HTML (como index.html) en la carpeta llamada templates.”

# crear carpetas donde se guardarán archivos temporales en el servidor
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
# Crea las carpetas automáticamente (si no existen)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse) # "/ " (decorador que envia a la ruta raiz), respon... (le dice a fastapi que la respuesta va ser un html y no json)
async def read_root(request: Request):  # async (funcion ayncrona), read... (nombre de la funcion), reques... (xq jinja2 lo necesita para que funcione la libreria Jinja2Templates)
    return templates.TemplateResponse("index.html", {"request": request}) # retorna ejecucion de archivo "index.html" ubicada en la carpeta templates

@app.get("/registro", response_class=HTMLResponse)
async def mostrar_registro(request: Request):
    return templates.TemplateResponse('registro.html', {"request" : request})

@app.post("/registro")
async def registrar_usuario(username: str = Form(...), password: str = Form(...)):
    usuarios.append({"username" : username, "password" : password})
    return {"mensaje": f"Usuario {username} registrado correctamente."}

@app.get("/login", response_class=HTMLResponse)
async def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    for user in usuarios:
        if user["username"] == username and user["password"] == password:
            return {"mensaje": f"Bienvenido, (username)!"}
    return {"error": "Credenciales incorrectas"}



@app.post("/procesar")
async def procesar_archivo(archivo: UploadFile = File(...)): # File(...) señala a Fastapi que el dato viene de un formulario
    nombre_archivo = archivo.filename   # obtiene elnombre del archivo subido
    ruta_subida = os.path.join(UPLOAD_FOLDER, nombre_archivo) # crea la ruta para subir el archivo de forma temporal a la carpeta del servidor

    # Sube y guarda el archivo en el servidor
    with open(ruta_subida, "wb") as f:
        f.write(await archivo.read())

    try: # indica ejecutar, pero si falla se va a except (manejo de errores), try y except siempre van juntos.
        df = pd.read_excel(ruta_subida) # Crea un DataFrame llamado df con los datos del Excel

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
