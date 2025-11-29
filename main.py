import json
from agent import PublicationAgent

if __name__ == "__main__":
    agent = PublicationAgent()
    print("Agente creado")
    output = agent.run(
        image_path="se.webp",
        desc="mirada a la nada",
        tone="cálido y festivo",
        platform="facebook"
    )

    print(json.dumps(output, indent=2, ensure_ascii=False))
