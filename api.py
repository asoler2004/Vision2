import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from agent import PublicationAgent
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
agent = PublicationAgent()

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def root():
    return FileResponse("static/index.html")


# @app.get("/")
# def root():
#     return {"message": "Agente de publicaciones activo."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/generate_post")
async def generate_post(
    image: UploadFile = File(...),
    desc: str = Form(...),
    tone: str = Form(...),
    platform: str = Form(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        content = await image.read()
        tmp.write(content)
        tmp_path = tmp.name

    result = agent.run(
        image_path=tmp_path,
        desc=desc,
        tone=tone,
        platform=platform
    )

    return result
