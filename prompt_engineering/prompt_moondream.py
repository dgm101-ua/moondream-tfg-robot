"""Exportar resultados a CSV para tu memoria del TFG."""

import json
import moondream as md
from PIL import Image
import time  # Importa el módulo para medir el tiempo
import os

# === Configuración ===
MODELS = {
    # "0.5B-int8": "../moondream-models/moondream-0_5b-int8.mf",
    "2B-int8": "../moondream-models/moondream-2b-int8.mf"
}

# === Selección del modelo activo ===
MODEL_NAME, MODEL_PATH = next(iter(MODELS.items()))
print(f"Usando modelo: {MODEL_NAME} ({MODEL_PATH})")

PROMPTS = {
    # --- BASIC ---
    "basic-1": lambda: "Is there a balloon in this image?",
    "basic-2": lambda: "Can you see any balloons in this picture?",
    "basic-3": lambda: "Does the image contain one or more balloons?",
    "basic-4": lambda: "Balloon?",
    "basic-5": lambda: "Any balloons?",
    "basic-6": lambda: "Do balloons appear?",
    "basic-7": lambda: "Presence of balloons?",
    # --- LIST-COLORS ---
    "list-colors-1": lambda: "List all balloon colors present.",
    "list-colors-2": lambda: "What are the colors of the balloons in the image?",
    "list-colors-3": lambda: "Identify the different colors of any balloons you see.",
    "list-colors-4": lambda: "Colour of Balloon?",
    "list-colors-5": lambda: "Color of Balloon?",
    "list-colors-6": lambda: "Balloon Color?",
    "list-colors-7": lambda: "Give me the balloon hues you detect.",
    # --- TWO-STEP COMBINADO ---
    "two-step-1": lambda: "Are there any balloons? If yes, what color are they?",
    "two-step-2": lambda: "Do you see balloons? If so, tell me their colors.",
    "two-step-3": lambda: "Is there a balloon? Describe the colors if any are present.",
    "two-step-4": lambda: "Is there any balloon shown? If yes, list their colors.",
}


IMAGE_FOLDER = "images-test"
EXPECTED_JSON = "expected_results.json"
LOG_FILE = f"metrics_{MODEL_NAME}.log"


# === Utilidad para procesar respuestas ===
def construir_respuesta(answer):
    respuesta = {"answer": answer}
    if "no" in answer.lower():
        respuesta["found"] = False
        respuesta["colours"] = []
    else:
        respuesta["found"] = True
        colores_comunes = {
            "red",
            "blue",
            "green",
            "yellow",
            "purple",
            "orange",
            "pink",
            "white",
            "black",
            "gray",
            "brown",
        }
        palabras = answer.split()
        colores = [
            p.lower().strip(".,;?")
            for p in palabras
            if p.lower().strip(".,;?") in colores_comunes
        ]
        respuesta["colours"] = list(set(colores))
    return respuesta


# === Carga etiquetas esperadas ===
with open(EXPECTED_JSON, "r") as f:
    expected = json.load(f)

# === Ejecutar pruebas ===
with open(LOG_FILE, "w", encoding="utf-8") as log:
    for model_name, model_path in MODELS.items():
        log.write(f"\n\n=== Modelo: {model_name} ===\n")
        print(f"🔄 Cargando modelo {model_name}...")

        # Carga del modelo una única vez
        start_load = time.time()
        model = md.vl(model=model_path)
        log.write(f"Modelo cargado en {time.time() - start_load:.2f}s\n")
        print(f"✅ Modelo {model_name} cargado correctamente.")

        for prompt_type, prompt_func in PROMPTS.items():
            total_time = 0
            correct_found = 0
            correct_colors = 0
            total_imgs = len(expected)

            log.write(f"\n-- Prompt: {prompt_type} --\n")
            print(f"🔄 Ejecutando pruebas con prompt '{prompt_type}'...")

            for img_name, gt in expected.items():
                img_path = os.path.join(IMAGE_FOLDER, img_name)
                image = Image.open(img_path)

                start = time.time()
                answer = model.query(image, prompt_func())["answer"]
                latency = time.time() - start
                total_time += latency

                respuesta = construir_respuesta(answer)

                # Métricas
                if respuesta["found"] == gt["found"]:
                    correct_found += 1
                    # Si al menos un color coincide, lo contamos como correcto
                    if any(c in gt["colours"] for c in respuesta["colours"]):
                        correct_colors += 1

                log.write(
                    f"\n[{img_name}] -> {respuesta} | GT: {gt} | Time: {latency:.2f}s"
                )
                print(f"[{img_name}] -> {respuesta} | GT: {gt} | Time: {latency:.2f}s")
            avg_time = total_time / total_imgs
            found_acc = correct_found / total_imgs * 100
            color_acc = correct_colors / total_imgs * 100

            log.write(f"\n\nResumen para prompt '{prompt_type}':\n")
            log.write(f"Latencia media: {avg_time:.2f} s\n")
            log.write(f"Precisión detección: {found_acc:.2f}%\n")
            log.write(f"Precisión colores: {color_acc:.2f}%\n")
