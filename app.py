from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
from graphs import grafica_columna
import plotly.io as pio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes especificar dominios en lugar de "*", si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configura la carpeta donde se guardarán los archivos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Montar un directorio estático para los archivos de frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload File</title>
    </head>
    <body>
        <h1>Upload File</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")

    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Upload a valid file")

    # Guardar el archivo en el servidor
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        df = pd.read_csv(file_path)
        charts = {}
        j = 0
        if not df.empty:
            for i in df.columns:
                fig = grafica_columna(df[i])
                # Serializar el gráfico a JSON
                charts[f'fig{j}'] = json.loads(pio.to_json(fig))
                j += 1

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")
    
    # Retornar los gráficos en formato JSON
    return charts

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
