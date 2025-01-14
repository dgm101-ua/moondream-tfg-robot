# ===== STEP 1: Install Dependencies =====
# pip install moondream  # Install dependencies in your project directory


# ===== STEP 2: Download Model =====
# Download model (422 MiB download size, 816 MiB memory usage)
# Use: wget (Linux and Mac) or curl.exe -O (Windows)
# wget https://huggingface.co/vikhyatk/moondream2/resolve/9dddae84d54db4ac56fe37817aeaeb502ed083e2/moondream-0_5b-int4.mf.gz

import moondream as md
from PIL import Image
import time  # Importa el módulo para medir el tiempo

# Inicia el temporizador para cargar el modelo
start_time = time.time()
model = md.vl(model='./moondream-models/moondream-0_5b-int8.mf')  # Initialize model
# model = md.vl(model='./moondream-models/moondream-2b-int8.mf')  # Initialize model
end_time = time.time()
print(f"Model loaded in {end_time - start_time:.2f} seconds.")



image = Image.open("./imagenes/img4.jpg")  # Load image

# Inicia el temporizador desde que recibe imagen hasta que imprime el prompt
start_time = time.time()
#image = model.encode_image(image)  # Encode image (recommended for multiple operations)


# 1. Caption any image (length options: "short" or "normal" (default))
# caption = model.caption(image, length="short")["caption"]
# print("Short Caption:", caption)


# 2. Query any image
answer = model.query(image, "What colour are the balloons?")["answer"]
print("\nAnswer:", answer)  # Single response

end_time = time.time()
print(f"Image encoded in {end_time - start_time:.2f} seconds.")

# 3. Detect any object
# detect_result = model.detect(image, "subject")  # change 'subject' to what you want to detect
# print("\nDetected:", detect_result["objects"])

# Point functionality is only available for 2B models