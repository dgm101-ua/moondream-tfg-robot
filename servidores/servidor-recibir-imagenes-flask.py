from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
# Token de acceso para impedir atasques a esta api
API_KEY = "tu_token_secreto_12345"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear carpeta para almacenar imágenes

@app.route('/upload', methods=['POST'])
def upload_image():
    # Verificar la API Key en los encabezados de la solicitud
    token = request.headers.get('Authorization')
    if not token or token != f"Bearer {API_KEY}":
        return jsonify({"error": "Acceso no autorizado"}), 401

    if 'image' not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    file.save(file_path)  # Guardar la imagen
    return jsonify({"message": "Imagen recibida", "path": file_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Escuchar en todas las interfaces
