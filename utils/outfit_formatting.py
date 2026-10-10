_CATEGORY_ORDER = ["tops", "bottoms", "outerwear", "shoes", "accessories"]

STYLIST_SYSTEM = (
    "You are a thrift-fashion stylist. You give short, specific outfit ideas. "
    "Never invent clothing the person hasn't said they own. Plain text only, "
    "no markdown headers."
)


def describe_listing(item: dict) -> str:
    """Listing fields: title, category, colors, style_tags, description (no 'name' or 'notes')."""
    lines = [f"Title: {item.get('title', 'Unknown item')}"]
    if item.get("category"):
        lines.append(f"Category: {item['category']}")
    if item.get("colors"):
        lines.append(f"Colors: {', '.join(item['colors'])}")
    if item.get("style_tags"):
        lines.append(f"Style: {', '.join(item['style_tags'])}")
    if item.get("description"):
        lines.append(f"Details: {item['description']}")
    return "\n".join(lines)


def format_wardrobe(items: list[dict]) -> str:
    """One line per piece, grouped by category so the model can see what's covered."""
    by_cat: dict[str, list[dict]] = {}
    for it in items:
        by_cat.setdefault(it.get("category") or "other", []).append(it)

    ordered = [c for c in _CATEGORY_ORDER if c in by_cat]
    ordered += [c for c in by_cat if c not in _CATEGORY_ORDER]   # unknown categories still show up

    lines = []
    for cat in ordered:
        lines.append(f"{cat.upper()}:")
        for it in by_cat[cat]:
            parts = []
            if it.get("colors"):
                parts.append(f"colors: {', '.join(it['colors'])}")
            if it.get("style_tags"):
                parts.append(f"style: {', '.join(it['style_tags'])}")
            if it.get("notes"):                                    # optional, may be None
                parts.append(f"note: {it['notes']}")
            detail = f" ({'; '.join(parts)})" if parts else ""
            lines.append(f"- {it.get('name', 'Unnamed piece')}{detail}")
    return "\n".join(lines)


CAPTION_SYSTEM = (
    "You write social media captions for thrift finds, in the voice of the "
    "person who just bought the piece. You sound like a real person posting "
    "to friends, not like a store listing or an ad. Output only the caption "
    "itself: no quotation marks, no preamble, no labels."
)
 
def format_price(price) -> str:
    """24.0 -> '$24', 24.5 -> '$24.50'. Falls back gracefully if price is missing."""
    if price is None:
        return "an unlisted price"
    return f"${price:.0f}" if float(price) == int(price) else f"${price:.2f}"
