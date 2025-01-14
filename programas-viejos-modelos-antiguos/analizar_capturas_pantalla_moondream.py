import os
from moondream_procesar_estados import cargar_modelo, procesar_imagen_y_prompt
from PIL import Image

# Cargar el modelo Moondream
moondream, tokenizer, device = cargar_modelo(cpu=False)  # Usa 'cpu=True' si no tienes una GPU disponible

# Carpeta con las imágenes de las capturas de pantalla
carpeta_imagenes = r"F:\UNI\practicas I\github - practicas branch desi\practicas\desi\omniparser\OmniParser-master\imgs-pruebas-descripciones\diferencia-template-dark-light"  # Asegúrate de que esta carpeta exista y contenga imágenes

# Asegúrate de que la carpeta de imágenes exista
if not os.path.exists(carpeta_imagenes):
    print(f"La carpeta {carpeta_imagenes} no existe.")
else:
    # Recorrer todas las imágenes en la carpeta
    for archivo in os.listdir(carpeta_imagenes):
        # Verifica si el archivo tiene una extensión de imagen válida (png, jpg, jpeg, etc.)
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Construir la ruta completa de la imagen
            ruta_imagen = os.path.join(carpeta_imagenes, archivo)
            
            print(f"Procesando la imagen: {archivo}")
            prompt = "This is a computer screenshot. Describe what the user is doing and what app is using."
            # Procesar la imagen con el modelo Moondream y obtener la descripción
            caption = procesar_imagen_y_prompt(ruta_imagen, prompt=prompt, moondream=moondream, tokenizer=tokenizer, device=device)
            
            # Imprimir la descripción en la terminal
            print(f"Descripción para {archivo}:")
            print(caption)
            print('-' * 40)  # Separador entre imágenes
