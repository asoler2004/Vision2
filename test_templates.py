from templates import render_instagram, render_facebook, render_linkedin, render_html

dummy_struct = {
    "headline": "Gelatinas navideñas 2x1",
    "hook": "Endulza tus fiestas con un detalle diferente.",
    "body": "Gelatinas artesanales con técnica de inyección y tallado, ideales para reuniones familiares y eventos especiales.",
    "call_to_action": "Reserva tu pedido hoy mismo.",
    "benefits": [
        "Diseños personalizados",
        "Ingredientes de calidad",
        "Entrega puntual"
    ],
    "hashtags": [
        "#GelatinasNavideñas",
        "#PostresArtesanales",
        "#2x1"
    ]
}

if __name__ == "__main__":
    insta = render_instagram(dummy_struct)
    face = render_facebook(dummy_struct)
    link = render_linkedin(dummy_struct)
    html = render_html(dummy_struct)

    print("=== INSTAGRAM ===")
    print(insta["content"])
    print("\n=== FACEBOOK ===")
    print(face["content"])
    print("\n=== LINKEDIN ===")
    print(link["content"])
    print("\n=== HTML ===")
    print(html["content"])
