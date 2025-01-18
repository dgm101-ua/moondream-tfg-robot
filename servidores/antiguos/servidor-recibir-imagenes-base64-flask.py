from flask import Flask, request, jsonify
import os
import base64
import signal

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
API_KEY = "tu_token_secreto_12345"

# Crear la carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Borrar archivos en la carpeta uploads al iniciar
def limpiar_uploads():
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error al borrar {file_path}: {e}")

# Limpiar la carpeta al iniciar el programa
limpiar_uploads()

# Contador de imágenes
contador = 0

@app.route('/upload', methods=['POST'])
def upload_image():
    global contador  # Usamos una variable global para llevar el conteo

    # Verificar API Key
    token = request.headers.get('Authorization')
    if not token or token != f"Bearer {API_KEY}":
        return jsonify({"error": "Acceso no autorizado"}), 401

    data = request.get_json()
    if "image" not in data:
        return jsonify({"error": "No se encontró ninguna imagen"}), 400

    try:
        # Decodificar la imagen desde Base64
        image_data = base64.b64decode(data["image"])

        # Crear un nombre de archivo único
        contador += 1
        image_filename = f"img-{contador}.png"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)

        # Guardar la imagen
        with open(image_path, "wb") as file:
            file.write(image_data)

        return jsonify({"message": "Imagen recibida y guardada", "path": image_path}), 200

    except Exception as e:
        return jsonify({"error": f"Error al procesar la imagen: {str(e)}"}), 500

# Manejar la señal de salida para limpiar la carpeta cuando el servidor se detenga
def cerrar_servidor(signal, frame):
    print("\n🧹 Cerrando el servidor... Eliminando archivos en /uploads/")
    limpiar_uploads()
    print("✅ Carpeta uploads limpia. Saliendo...")
    exit(0)

# Capturar señales de interrupción (CTRL+C)
signal.signal(signal.SIGINT, cerrar_servidor)
signal.signal(signal.SIGTERM, cerrar_servidor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
