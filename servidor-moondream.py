from flask import Flask, request, jsonify
import os
import signal
import moondream as md
from PIL import Image
import time

UPLOAD_FOLDER = "uploads"
API_KEY = "tu_token_secreto_12345"

# Cargar el modelo una sola vez al iniciar la aplicación para ahorrar tiempo
model = None

# Contador de imágenes
contador = 0

# MÉTODOS AUXILIARES #

# Borrar archivos en la carpeta uploads al iniciar
def limpiar_uploads():
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error al borrar {file_path}: {e}")

def load_model():
    global model
    if model is None:
        start_time = time.time()
        model = md.vl(model='./moondream-models/moondream-0_5b-int8.mf')  # Inicializar el modelo
        end_time = time.time()
        print(f"Model loaded in {end_time - start_time:.2f} seconds.")

# Manejar la señal de salida para limpiar la carpeta cuando el servidor se detenga
def cerrar_servidor(signal, frame):
    print("\n🧹 Cerrando el servidor... Eliminando archivos en /uploads/")
    limpiar_uploads()
    print("✅ Carpeta uploads limpia. Saliendo...")
    exit(0)

# INICIO APLICACIÓN #

app = Flask(__name__)

# Crear la carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Limpiar la carpeta al iniciar el programa
limpiar_uploads()

# Cargar el modelo al inicio únicamente una vez
load_model()

# ENDPOINTS #

@app.route('/upload', methods=['POST'])
def upload_image():
    global contador  # Usamos una variable global para llevar el conteo

    # Verificar API Key
    token = request.headers.get('Authorization')
    if not token or token != f"Bearer {API_KEY}":
        return jsonify({"error": "Acceso no autorizado"}), 401

    # Verificar si la imagen está en el archivo de la solicitud
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    file = request.files['image']
    
    # Verificar que el archivo sea una imagen PNG
    if not file.filename.endswith('.png'):
        return jsonify({"error": "El archivo debe ser una imagen PNG"}), 400

    try:
        # Crear un nombre de archivo único
        contador += 1
        image_filename = f"img-{contador}.png"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)

        # Guardar la imagen
        file.save(image_path)

        return jsonify({"message": "Imagen recibida y guardada", "path": image_path}), 200

    except Exception as e:
        return jsonify({"error": f"Error al procesar la imagen: {str(e)}"}), 500


# Endpoint para cargar la imagen y hacer una consulta con el modelo
@app.route('/balloon_colour', methods=['POST'])
def query_balloon_colour():
    # Verificar la API Key
    token = request.headers.get('Authorization')
    if not token or token != f"Bearer {API_KEY}":
        return jsonify({"error": "Acceso no autorizado"}), 401

    # Verificar que se haya enviado una imagen
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    # Obtener la imagen enviada
    image_file = request.files['image']
    try:
        # Abrir la imagen
        image = Image.open(image_file.stream)  # Utilizamos .stream para trabajar con la imagen en memoria

        # Iniciar temporizador para medir el tiempo de procesamiento
        start_time = time.time()

        # Consultar la imagen con el modelo
        #answer = model.query(image, "What colour are the balloons?")["answer"]
        answer = model.query(image, "Are there any balloons in the image? What are their color?")["answer"]
        print("\nAnswer:", answer)  # Respuesta única

        # Finalizar el temporizador
        end_time = time.time()
        print(f"Image processed in {end_time - start_time:.2f} seconds.")

        return jsonify({"message": "Consulta procesada con éxito", "answer": answer}), 200

    except Exception as e:
        return jsonify({"error": f"Error al procesar la imagen: {str(e)}"}), 500


# Capturar señales de interrupción (CTRL+C)
signal.signal(signal.SIGINT, cerrar_servidor)
signal.signal(signal.SIGTERM, cerrar_servidor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
