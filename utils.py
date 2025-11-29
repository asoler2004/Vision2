from PIL import Image
from modelos import blip_processor, blip_model, device

def analyze_image(image_path: str) -> str:
    """
    Usa BLIP para generar una descripción corta de la imagen.
    """
    image = Image.open(image_path).convert("RGB")
    print("imagen cargada")
    inputs = blip_processor(images=image, return_tensors="pt").to(device)
    print("inputs: ",inputs)
    out = blip_model.generate(**inputs, max_new_tokens=30)
    print("output: ",out)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption
