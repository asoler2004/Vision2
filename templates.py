def render_instagram(struct: dict) -> dict:
    headline = struct["headline"]
    hook = struct["hook"]
    body = struct["body"]
    cta = struct["call_to_action"]
    benefits = struct.get("benefits", [])
    hashtags = struct.get("hashtags", [])

    benefits_lines = ""
    if benefits:
        benefits_lines = "\n".join([f"• {b}" for b in benefits])

    text = (
        f"{headline} ✨\n\n"
        f"{hook}\n\n"
        f"{body}\n\n"
        f"{benefits_lines}\n\n"
        f"{cta} 💬\n\n"
        f"{' '.join(hashtags)}"
    ).strip()

    return {
        "platform": "instagram",
        "content": text,
        "hashtags": hashtags,
        "raw_structure": struct
    }


def render_facebook(struct: dict) -> dict:
    headline = struct["headline"]
    hook = struct["hook"]
    body = struct["body"]
    cta = struct["call_to_action"]
    benefits = struct.get("benefits", [])
    hashtags = struct.get("hashtags", [])

    benefits_lines = ""
    if benefits:
        benefits_lines = "\n".join([f"- {b}" for b in benefits])

    text = (
        f"{headline}\n\n"
        f"{hook}\n\n"
        f"{body}\n\n"
        f"Beneficios:\n{benefits_lines}\n\n"
        f"{cta}\n\n"
        f"{' '.join(hashtags)}"
    ).strip()

    return {
        "platform": "facebook",
        "content": text,
        "hashtags": hashtags,
        "raw_structure": struct
    }


def render_linkedin(struct: dict) -> dict:
    headline = struct["headline"]
    hook = struct["hook"]
    body = struct["body"]
    cta = struct["call_to_action"]
    benefits = struct.get("benefits", [])

    bullets = ""
    if benefits:
        bullets = "\n".join([f"• {b}" for b in benefits])

    text = (
        f"{headline}\n\n"
        f"{hook}\n\n"
        f"{body}\n\n"
        f"Algunos beneficios clave:\n{bullets}\n\n"
        f"{cta}"
    ).strip()

    return {
        "platform": "linkedin",
        "content": text,
        "hashtags": [],
        "raw_structure": struct
    }


def render_html(struct: dict) -> dict:
    headline = struct["headline"]
    hook = struct["hook"]
    body = struct["body"]
    cta = struct["call_to_action"]
    benefits = struct.get("benefits", [])

    benefits_items = ""
    for b in benefits:
        benefits_items += f"<li>{b}</li>"

    html = f"""
<section class="promo-block">
  <h1>{headline}</h1>
  <p class="hook">{hook}</p>
  <p class="body">{body}</p>
  <ul class="benefits">
    {benefits_items}
  </ul>
  <button class="cta">{cta}</button>
</section>
""".strip()

    return {
        "platform": "html",
        "content": html,
        "hashtags": struct.get("hashtags", []),
        "raw_structure": struct
    }
