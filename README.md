# Procesador de Excel con FastAPI

Esta aplicación web permite subir un archivo Excel, procesarlo en el servidor usando FastAPI y pandas, y devolver un nuevo archivo Excel procesado.

## 🚀 Cómo desplegar en Render

### 1. Subir el proyecto a GitHub
1. Crea un nuevo repositorio en GitHub.
2. Sube todos los archivos del proyecto (incluido este README).

### 2. Crear servicio en Render
1. Ve a [https://render.com](https://render.com) y crea una cuenta.
2. Crea un **nuevo Web Service**.
3. Conecta tu cuenta de GitHub y selecciona el repositorio.

### 3. Configuración en Render
- **Runtime**: Python 3
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 10000
  ```
- **Port**: 10000 (Render lo detecta automáticamente)

### 4. ¡Listo!
Render te dará una URL pública donde tu app estará funcionando.

## 🧪 Cómo ejecutar localmente

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre [http://127.0.0.1:8000](http://127.0.0.1:8000) en tu navegador.

---

Hecho con ❤️ usando FastAPI, pandas y Jinja2.
