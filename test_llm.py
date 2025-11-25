from llm import generate_base_structure

if __name__ == "__main__":
    desc = "Promoción 2x1 en gelatinas navideñas hechas con técnica de inyección y tallado."
    tone = "cálido y festivo"
    image_summary = "a holiday dessert with red flowers and bright colors"

    struct = generate_base_structure(desc, tone, image_summary)

    print(struct)
