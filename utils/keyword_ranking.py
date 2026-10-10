import re
import nltk
from nltk.stem import PorterStemmer

# ── Word Matching ──────────────────────────────────────────────────
MAX_STEM_LEN = 40

_MIN_SAFE_NLTK_VERSION = (3, 10, 3)

def _parse_version(v: str) -> tuple:
    parts = []
    for piece in v.split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)

def _check_nltk_version():
    if _parse_version(nltk.__version__) < _MIN_SAFE_NLTK_VERSION:
        import warnings

        warnings.warn(
            f"nltk {nltk.__version__} is installed, but PorterStemmer.stem() has "
            f"a known quadratic-time DoS bug (CVE-2026-81722), fixed only in "
            f"nltk>=3.10.3. Run `pip install --upgrade nltk` to fix this.",
            stacklevel=2,
        )

_stemmer = PorterStemmer()
_WORD = re.compile(r"[a-z0-9]+")

def _tokenize(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def _safe_stem(word: str) -> str:
    """Stem a word, skipping anything implausibly long."""
    if len(word) > MAX_STEM_LEN:
        return word
    return _stemmer.stem(word)


def _stems(words) -> set[str]:
    return {_safe_stem(w) for w in words}

# ── Size Tokenization ──────────────────────────────────────────────────
_SIZE_TOKEN = re.compile(r"[a-z0-9.]+")
 
def _size_tokens(text: str) -> set[str]:
    """'S/M' -> {'s','m'}   'XL (fits oversized)' -> {'xl','fits','oversized'}
       'US 8.5' -> {'us','8.5'}   'W30 L30' -> {'w30','l30'}"""
    return set(_SIZE_TOKEN.findall(text.lower()))

# ── Item-Type Vocabulary ──────────────────────────────────────────────────────
# listing['category'] = where it sits on the body.
# canonical type -> words that name it. Matched against the listing TITLE only.
# (Descriptions say things like "pairs well with jeans" and would cause false hits.)
ITEM_TYPES = {
    "jacket":     ["jacket", "windbreaker", "bomber"],
    "blazer":     ["blazer"],
    "vest":       ["vest"],
    "coat":       ["coat", "shacket"],
    "tee":        ["tee", "t-shirt", "tshirt"],
    "shirt":      ["shirt", "flannel", "button-down", "polo", "henley"],
    "hoodie":     ["hoodie"],
    "sweatshirt": ["sweatshirt", "crewneck"],
    "cardigan":   ["cardigan"],
    "top":        ["top", "tank", "halter"],
    "jeans":      ["jeans"],
    "pants":      ["pants", "trousers"],
    "shorts":     ["shorts"],
    "dress":      ["dress"],
    "sneakers":   ["sneakers"],
    "boots":      ["boots"],
    "mary janes": ["maryjanes"],
    "belt":       ["belt"],
    "hat":        ["hat"],
    "bag":        ["bag"],
}
 
def _normalize(text: str) -> str:
    # make multiword/hyphenated aliases single tokens before tokenizing
    return (text.lower()
            .replace("t-shirt", "tshirt")
            .replace("button-down", "buttondown")
            .replace("mary janes", "maryjanes").replace("mary jane", "maryjanes"))
 
def _build_alias_index() -> dict[str, str]:
    """Create alias dict to identify type of clothing"""
    idx = {}
    for canon, aliases in ITEM_TYPES.items():
        for a in aliases:
            for tok in _tokenize(_normalize(a)):
                idx[_safe_stem(tok)] = canon
    return idx
 
_ALIAS_TO_TYPE = _build_alias_index()
 
# Query words that are really a *group* of types ("shoes" -> any footwear).
# Maps a query stem to the listing categories it allows.
_GROUP_CATEGORY = {_safe_stem(w): cat for w, cat in {
    "shoes": "shoes", "footwear": "shoes",
    "outerwear": "outerwear", "bottoms": "bottoms", "tops": "tops",
    "accessories": "accessories",
}.items()}
 
 
def _detect_type(query_stems: set[str]) -> str | None:
    for s in query_stems:
        if s in _ALIAS_TO_TYPE:
            return _ALIAS_TO_TYPE[s]
    return None
 
 
def _listing_type(listing: dict) -> str | None:
    """Head noun of the title = the LAST alias word before the dash.
    'Low-Top Canvas Sneakers' -> sneakers (not 'top');
    'Oversized Crewneck Sweatshirt' -> sweatshirt."""
    head = listing["title"].split("\u2014")[0]          # drop the "— Medium Wash" part
    found = None
    for tok in _tokenize(_normalize(head)):
        found = _ALIAS_TO_TYPE.get(_safe_stem(tok), found)
    return found
 
 
# ── scoring ───────────────────────────────────────────────────────────────────
_STOPWORDS = {"a", "an", "the", "for", "i", "im", "want", "looking", "need", "find",
              "me", "some", "under", "below", "size", "in", "of", "and", "with", "to"}
_WEIGHTS = {"title": 3, "tags": 2, "colors": 2, "brand": 2, "description": 1}
 
 
def _score(listing: dict, query_stems: set[str]) -> int:
    fields = {
        "title":       listing["title"],
        "tags":        " ".join(listing.get("style_tags") or []),
        "colors":      " ".join(listing.get("colors") or []),
        "brand":       listing.get("brand") or "",          # brand is often None!
        "description": listing.get("description") or "",
    }
    score = 0
    for name, text in fields.items():
        field_stems = _stems(_tokenize(_normalize(text)))
        score += _WEIGHTS[name] * len(query_stems & field_stems)
    return score

# ── Util Functions (import these) ─────────────────────────────────────────────────────────────────── 

def size_matches(wanted: str, listing_size: str) -> bool:
    """Whole-token match: every token the user typed must be a whole token of the
    listing's size. 'M' matches 'S/M' and 'M/L' but not 'US 9' or 'XL (fits oversized)'."""
    want = _size_tokens(wanted)
    return bool(want) and want <= _size_tokens(listing_size)


def rank_listings(listings: list[dict], query: str) -> list[tuple]:
    _check_nltk_version()
    # 1. understand the query
    q_stems = _stems(w for w in _tokenize(_normalize(query)) if w not in _STOPWORDS)
    if not q_stems:
        return []
    wanted_type = _detect_type(q_stems)
    wanted_cats = {_GROUP_CATEGORY[s] for s in q_stems if s in _GROUP_CATEGORY}
 
    # 2. item-type gate: "jacket" must be a jacket, not just outerwear
    if wanted_type:
        listings = [l for l in listings if _listing_type(l) == wanted_type]
    if wanted_cats:
        listings = [l for l in listings if l["category"] in wanted_cats]

    # 4. score, drop zeros, sort (score desc, cheaper first on ties)
    # passing the type gate is itself a match ("t-shirt" never appears in a title, "Tee" does)
    bonus = _WEIGHTS["title"] if (wanted_type or wanted_cats) else 0
    scored = [(_score(l, q_stems) + bonus, l) for l in listings]
    scored = [(s, l) for s, l in scored if s > 0]
    scored.sort(key=lambda sl: (-sl[0], sl[1]["price"]))
    return scored

