import os
from dotenv import load_dotenv
import google.generativeai as genai

from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Cargar variables de entorno
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Falta GEMINI_API_KEY en .env")

# Configurar Gemini
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# Configurar BLIP
device = "cuda" if torch.cuda.is_available() else "cpu"

blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)
