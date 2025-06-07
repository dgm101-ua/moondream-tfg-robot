from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import time

# Cargar imagen
image = Image.open("img-example/img3.png")  # <-- Aquí se define `image`

model = AutoModelForCausalLM.from_pretrained(
    "vikhyatk/moondream2",
    revision="2025-04-14",
    trust_remote_code=True,
    # Uncomment to run on GPU.
    device_map={"": "cuda"}
)

# Captioning
#print("Short caption:")
#print(model.caption(image, length="short")["caption"])

#print("\nNormal caption:")
#for t in model.caption(image, length="normal", stream=True)["caption"]:
    # Streaming generation example, supported for caption() and detect()
#    print(t, end="", flush=True)
#print(model.caption(image, length="normal"))

# Visual Querying
start = time.time()
print("\nVisual query: 'How many balloons are in the image?'")
print(model.query(image, "How many balloons are in the image?")["answer"])
print(f"Tardó {time.time() - start:.2f} segundos")

# Object Detection
start = time.time()
print("\nObject detection: 'balloon'")
objects = model.detect(image, "balloon")["objects"]
print(f"Found {len(objects)} balloon(s)")
print(f"Tardó {time.time() - start:.2f} segundos")

# Pointing
start = time.time()
print("\nPointing: 'balloon'")
points = model.point(image, "balloon")["points"]
print(f"Found {len(points)} balloon(s)")
print(f"Tardó {time.time() - start:.2f} segundos")
