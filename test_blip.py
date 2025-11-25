from utils import analyze_image

if __name__ == "__main__":
    caption = analyze_image("se.webp")
    print("Caption generado por BLIP:")
    print(caption)
