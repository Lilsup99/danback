from flask import Flask, request, render_template
import os
import pandas as pd
from graphs import grafica_columna

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

# Configura la carpeta donde se guardarán los archivos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv','xlxs'}

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    # Guardar el archivo en el servidor
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if file and allowed_file(file.filename):

        try:
            df = pd.read_csv(file_path)
            print(df.head(5))
            processed_data = df.head().to_html()  # Convertir a HTML para mostrar en la respuesta
        except Exception as e:
            return f'Error processing file: {e}', 400
    
        return f'File uploaded and processed successfully:<br>{processed_data}', 200

    else:
        return 'upload valid file'

if __name__ == '__main__':
    app.run(debug=True)
