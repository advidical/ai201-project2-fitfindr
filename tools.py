"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings
from utils.keyword_ranking import size_matches, rank_listings
from utils.outfit_formatting import describe_listing, format_wardrobe, format_price,\
                                    STYLIST_SYSTEM, CAPTION_SYSTEM


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    
    1. Load every listing with load_listings().
    2. Filter by max_price and by size, when each is provided.
    3. Score what's left by keyword overlap with `description`.
    4. Drop anything scoring zero.
    5. Sort by score, highest first, and return the listing dicts —
       at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()
    # hard filters 
    if max_price is not None:
        listings = [l for l in listings if l["price"] <= max_price]
    if size:  # None or "" -> skip
        listings = [l for l in listings if size_matches(size, l["size"])]

    matches = rank_listings(listings, description)
    if not matches:
        return []
    return [l for _, l in matches[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────
def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.
    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    1. Check whether wardrobe['items'] is empty.
    2. If it is, ask the model for general styling ideas for this item.
    3. If it isn't, format the wardrobe items into the prompt and ask for 
       specific combinations naming pieces the user already owns.
    4. Return the model's response.

    Test it from a terminal before you move on:
    python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

    """
    items = (wardrobe or {}).get("items") or []      # handles {}, None, and {"items": []}
    item_block = describe_listing(new_item)

    if not items:
        prompt = (
            "I'm thinking about buying this thrifted piece:\n"
            f"{item_block}\n\n"
            "I haven't added my wardrobe yet. Give me one or two outfit ideas "
            "built around this piece, using common basics most people own "
            "(e.g. plain jeans, white sneakers). Name each piece, and add one "
            "line on the vibe of each outfit."
        )
    else:
        prompt = (
            "I'm thinking about buying this thrifted piece:\n"
            f"{item_block}\n\n"
            "Here is everything I already own:\n"
            f"{format_wardrobe(items)}\n\n"
            "Suggest one or two outfits that combine the new piece with items "
            "from my wardrobe. Refer to my pieces by the exact names listed "
            "above, and use only pieces from that list. If my wardrobe is "
            "missing something an outfit needs (say, no shoes listed), say so "
            "briefly rather than making something up. Add one line on the "
            "vibe of each outfit."
        )

    response = generate(prompt, system=STYLIST_SYSTEM)
    # The tool's contract is a non-empty string, even if the model returns nothing.
    return response.strip() or (
        f"No outfit suggestion came back for {new_item.get('title', 'this item')}. "
        "Try again."
    )


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # 1. Guard: nothing to caption -> a message, not a crash and not a model call
    if not outfit or not outfit.strip():
        return (
            "No valid outfit was provided, so I can't write an appropriate "
            "caption. Please provide an outfit suggestion next time!"
        )
 
    # 2. Pull out the three facts the caption must contain
    title = new_item.get("title", "this piece")
    price = format_price(new_item.get("price"))
    platform = new_item.get("platform", "a thrift app")
 
    # 3. Build the prompt: facts, then the outfit, then the rules
    prompt = (
        "I just found this on a thrifting app:\n"
        f"- Item: {title}\n"
        f"- Price: {price}\n"
        f"- Platform: {platform}\n\n"
        "Here is how I plan to style it:\n"
        f"{outfit.strip()}\n\n"
        "Write my post caption. Rules:\n"
        "- 2 to 4 sentences, first person, casual.\n"
        "- Mention the item, the price and the platform exactly once each.\n"
        "- Be specific about the vibe of the outfit; don't use generic filler "
        "like 'obsessed' or 'so cute' as the whole point.\n"
        "- No hashtag lists. At most one emoji."
    )
 
    # 4. Call the model (default temperature from config -> varied wording)
    caption = generate(prompt, system=CAPTION_SYSTEM).strip().strip('"').strip()
 
    # 5. Contract: never return an empty string
    return caption or f"No caption came back for {title}. Try again."

