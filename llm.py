import json
from modelos import gemini_model

def generate_base_structure(desc: str, tone: str, image_summary: str) -> dict:
    """
    Usa Gemini para combinar:
    - descripción del usuario (en español)
    - resumen de la imagen (en inglés o español)
    - tono deseado
    Y generar un JSON estructurado.
    """
    prompt = f"""
Eres un experto en marketing de contenido.

Tono deseado: {tone}

Descripción proporcionada por el usuario (en español):
{desc}

Resumen de la imagen:
{image_summary}

Genera contenido FINAL totalmente en español.

Devuelve SOLO un JSON con la siguiente estructura:

{{
  "headline": "Título corto y llamativo",
  "hook": "Frase inicial que atrape la atención",
  "body": "Párrafo descriptivo del producto u oferta",
  "call_to_action": "Llamado a la acción concreto",
  "benefits": [
    "Beneficio 1",
    "Beneficio 2",
    "Beneficio 3"
  ],
  "hashtags": [
    "#ejemplo1",
    "#ejemplo2"
  ]
}}

No agregues nada fuera del JSON.
"""
    res = gemini_model.generate_content(prompt)
    txt = res.text.strip()

    start = txt.find("{")
    end = txt.rfind("}") + 1

    data = json.loads(txt[start:end])
    return data
