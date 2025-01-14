 # moondream_procesar_estados.py
import torch
from PIL import Image
from transformers import AutoTokenizer
from moondream_main.moondream.hf import LATEST_REVISION, Moondream, detect_device


def cargar_modelo(cpu=False):
    """Carga el modelo Moondream y el tokenizador."""
    if cpu:
        device = torch.device("cpu")
        dtype = torch.float32
    else:
        device, dtype = detect_device()
        if device != torch.device("cpu"):
            print("Usando dispositivo:", device)
            print("Si tienes problemas, pasa el flag `--cpu` a este script.")
            print()

    model_id = "vikhyatk/moondream2"
    tokenizer = AutoTokenizer.from_pretrained(
        model_id, revision=LATEST_REVISION, ignore_mismatched_sizes=True
    )
    moondream = Moondream.from_pretrained(
        model_id,
        revision=LATEST_REVISION,
        torch_dtype=dtype,
        ignore_mismatched_sizes=True,
    ).to(device=device)
    moondream.eval()

    return moondream, tokenizer, device


def procesar_imagen_y_prompt(image_path, prompt=None, moondream=None, tokenizer=None, device=None):
    """
    Procesa la imagen con Moondream y genera una respuesta basada en el prompt.
    Si no se proporciona un prompt, genera una descripción de la imagen.
    """

    # Abrir la imagen
    image = Image.open(image_path)

    # Codificar la imagen
    image_embeds = moondream.encode_image(image)

    if prompt:
        # Si se proporciona un prompt, responder a la pregunta
        respuesta = moondream.answer_question(image_embeds, prompt, tokenizer)
        return respuesta
    else:
        # Si no hay prompt, generar una descripción de la imagen
        caption = moondream.caption(images=[image], tokenizer=tokenizer)[0]
        return caption
