from utils import analyze_image
from llm import generate_base_structure
from templates import (
    render_instagram,
    render_facebook,
    render_linkedin,
    render_html
)

class PublicationAgent:
    def __init__(self):
        self.memory = []

    def run(self, image_path: str, desc: str, tone: str, platform: str) -> dict:
        platform = platform.lower()

        # Paso 1 — BLIP analiza la imagen

        print("Analizando imagen...")
        image_summary = analyze_image(image_path)
        print("imagen analizada: ",image_summary)
        self.memory.append({
            "step": "image_summary",
            "value": image_summary
        })

        # Paso 2 — Gemini genera estructura base
        struct = generate_base_structure(desc, tone, image_summary)
        print("Resultado de Gemini: ", struct)
        self.memory.append({
            "step": "base_structure",
            "value": struct
        })

        # Paso 3 — Plantilla según plataforma
        if platform == "instagram":
            result = render_instagram(struct)
        elif platform == "facebook":
            result = render_facebook(struct)
        elif platform == "linkedin":
            result = render_linkedin(struct)
        elif platform == "html":
            result = render_html(struct)
        else:
            raise ValueError(f"Plataforma no soportada: {platform}")

        self.memory.append({
            "step": "final_output",
            "value": result
        })

        return result
