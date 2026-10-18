# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.

     Alex D. Lopez FitFindr
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

A user will enter a single line query such as 'vintage graphic tee under $30'.
The agent will then be called to run 3 tools in response. IT will first get best matching listings, then provide outfit suggestions, and generate a realistic two-four sentence caption based on the outfit suggestion provided previously

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** filters listings by text description, with optional params for size & price cap
- **Inputs:** description (str), size (str or None), max_price (float or None).
- **Returns:** A list of matching listing dicts, best match first.
- **When it has nothing:** an empty list when nothing matches — an empty list, not None, and not an exception.

### `suggest_outfit`

- **What it does:** Suggest one or two outfits given a thrifted item and the user's wardrobe
- **Inputs:** new_item (dict), wardrobe (dict). Note: wardrobe can be an empty dict
- **Returns:** outfit suggestions (str) non empty string based on item and current wardrobe
- **When it has nothing:** general styling ideas from model (str)

### `create_fit_card`

- **What it does:** Write a short caption that a person would post about the find, not a product description
- **Inputs:** outfit (str) [outfit suggestion from suggest_outfit()], new_item (dict)
- **Returns:** two-to-four sentence caption (str)
- **When it has nothing:** descriptive message stating "no valid outfit was provided: therefore cannot produce an appropriate caption. Please provide an outfit suggestion next time!

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule**: If search_listings returns an empty list, put a message in the session
and stop. Otherwise take the first result and go to suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Using string splitting to catch $# for price, & something to capture sizes.

**What moves through the session:** run_agent pasess the query & wardrobe dict, gives parsed result from query into search_listinngs, search_listings puts matching results in session["search_results"],then puts first matched into session['selected_item'], then passes it into suggest_outfit() and gets outfit suggestion (session["outfit_suggestion"]),
outfit suggestion passed to create_fit_card(), & store resulting caption in session['fit_card']

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'platform sneakers size 8'

```

Found: Platform Sneakers — White Chunky Sole — $48.0 on poshmark

Outfit: Outfit 1:
White ribbed tank top + Baggy straight-leg jeans, dark wash + Platform Sneakers — White Chunky Sole + Black crossbody bag
Vibe: Effortless, early-2000s model-off-duty streetwear.

Outfit 2:
Oversized grey crewneck sweatshirt + Baggy straight-leg jeans, dark wash + Platform Sneakers — White Chunky Sole
Vibe: Cozy, skater-inspired retro casual.

Fit card: Scored these chunky white platform sneakers on Poshmark for just $48, and I’m already living in them for that early-2000s model-off-duty streetwear look. They give baggy dark-wash jeans and a ribbed tank the exact right amount of height without trying too hard. Plus, throw on an oversized grey crewneck and you've got the ultimate retro skater vibe 👟

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'},

{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'},

{'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```
$ python -c "from tools import suggest_outfit; ..."

```

Outfit 1
Pair the Vintage Levi's 501 Jeans — Medium Wash with your White ribbed tank top, Black cropped zip hoodie worn unzipped over top, and Chunky white sneakers. Add your Black crossbody bag.
Vibe: Casual, streetwear-inspired sporty-cool.

Outfit 2
Pair the Vintage Levi's 501 Jeans — Medium Wash with your Oversized grey crewneck sweatshirt tucked in, and Brown leather belt cinching the waist. Finish with your Black combat boots and Black crossbody bag.
Vibe: Cozy, effortless vintage everyday.

```
$ python -c "from tools import create_fit_card; ..."

```

Found these vintage Levi's 501 jeans on Depop for $38 and they finally give me that perfectly worn-in, slightly slouchy 90s silhouette I've been hunting for. Throwing them on with crisp white sneakers for running errands and grabbing iced coffee this weekend. Honestly thrilled to stop gatekeeping my denim search. 👖

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**
I gave Claude my specs for search_listings and any work I did on my own.
It gave me usable code that worked on my runs, but I reformatted them to
move utilily globals & functions into a util py files, and I did some cleaning up,
such as handling the empty list case when no matches return

**Moment 2**
I gave claude my specs and progress code for suggest_outfits() & create_fit_card().
It gave me functional code using util functions that formatted my prompts and system prompts
for each function. After reviewing the code, I moved the util functions & system prompts into
a separate util py file for code cleaniness.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Incorporate MCP

```
python app.py ask 'vintage graphic tee under $30'
```

**search_listing() function**

```
Found: Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop, size : L
Outfit: Outfit One

Pair the Graphic Tee — 2003 Tour Bootleg Style with the Baggy straight-leg jeans, dark wash, and the Black combat boots. Add the Black crossbody bag and the Vintage black denim jacket on top.
Vibe: 90s grunge streetwear, effortless and moody.

Outfit Two

Layer the White ribbed tank top under the Graphic Tee — 2003 Tour Bootleg Style (letting the white hem peek out), tucked into the Wide-leg khaki trousers worn with the Brown leather belt. Finish with the Chunky white sneakers.
Vibe: Skater-meets-minimalist thrifted casual.

Fit card: Scored this 2003 tour bootleg graphic tee on Depop for twenty-four bucks and I'm already picturing it under a vintage denim jacket with combat boots for that moody 90s grunge streetwear look. 💀
```

**mcp_client.call_tool('search_listing', Params:Dict)**

```
Found: Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop, size : L
Outfit: Outfit 1
Wear the graphic tee with the baggy straight-leg jeans, the brown leather belt, the black combat boots, and the black crossbody bag.
Vibe: 90s grunge streetwear with a worn-in, effortless edge.

Outfit 2
Layer the black cropped zip hoodie unzipped over the graphic tee, paired with the wide-leg khaki trousers, the chunky white sneakers, and the black crossbody bag.
Vibe: Casual streetwear mixing faded rock aesthetics with sharp earth tones.

Fit card: Scored this 2003 tour bootleg graphic tee on Depop for $24 and I'm already planning two ways to wear it. First up is straight-leg jeans, combat boots, and a leather belt for that heavy 90s grunge streetwear feel. Or I'll layer it under an unzipped black hoodie with khaki trousers and chunky sneakers to mix faded rock aesthetics with sharp earth tones. 🎸
```

**Conclusion**
Gets the same outfit, just generates different outfit combinations & captions

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion                                            | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict   |
| ---------------------------------------------------- | ------ | ----- | ----- | ----- | ----- | ----- | --------- |
| 1. Matching query completes                          | 5 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 2. Impossible query stops early                      | 5 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| Empty wardrobe _(diagnostic — not one of your five)_ | n/a    | PASS  | PASS  | PASS  | PASS  | PASS  | n/a (5/5) |
| 3. State of selected item                            | 5 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 4. Fit card gives unique, structured responses       | 4 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |
| 5. Item always respects price ceiling                | 5 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
"- Produced by: `run_eval.py::main`",
"- Loop: `agent.py::run_agent` · tools: `tools.py`",
### matching query completes

- Query: `vintage graphic tee under $30`
- Wardrobe: example

**Try 1**

- stopped early: no
- selected_item: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
- search_results: 3

Outfit suggestion:

Outfit 1
Pair the Graphic Tee — 2003 Tour Bootleg Style with your baggy straight-leg jeans, dark wash and black combat boots. Add your black crossbody bag.
Vibe: 90s grunge streetwear.

Outfit 2
Layer your black cropped zip hoodie unzipped over the Graphic Tee — 2003 Tour Bootleg Style, paired with your wide-leg khaki trousers and chunky white sneakers.
Vibe: Relaxed, layered skate aesthetic.

Fit card:

Scored this 2003 tour bootleg tee on Depop for just 24 dollars and it is going right into my 90s grunge rotation with baggy dark denim and combat boots. I am also definitely layering it under a zip hoodie with wide-leg khakis for that effortless skate aesthetic 🖤

Trace:

[1] call_tool
      in:  tool: search_listings, params='description, size, max_price'
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[2] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: Outfit 1 Pair the Graphic Tee — 2003 Tour Bootleg Style with your baggy straight-leg jeans, dark wash and blac…
[3] create_fit_card
      in:  dict with keys: outfit_suggestion, selected_item
      out: Scored this 2003 tour bootleg tee on Depop for just 24 dollars and it is going right into my 90s grunge rotati…
```

---

## Verdicts and Diagnoses

| #   | Criterion                                   | Target | Verdict | How I decided                                                                                                                |
| --- | ------------------------------------------- | ------ | ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1   | Matching query completes                    | 5 of 5 | MET     | Compared all five tries in the run log. All five PASSED (5/5), which meets the target of 5 of 5.                             |
| 2   | Impossible query stops early                | 5 of 5 | MET     | Compared all five tries in the run log. All five PASSED (5/5), which meets the target of 5 of 5.                             |
| 3   | State of selected item                      | 5 of 5 | MET     | Compared all five tries in the run log. All five PASSED (5/5), which meets the target of 5 of 5.                             |
| 4   | Fit card gives unique, structured responses | 4 of 5 | MET     | Compared all five tries in the run log. all five fit cards were different strings and each named the price and platform once |
| 5   | Item always respects price ceiling          | 5 of 5 | MET     | Compared all five tries in the run log. All five PASSED (5/5), which meets the target of 5 of 5.                             |

**Diagnoses**

No criterion was missed. Every criterion passed on all five tries, so there is no failure to place in a tool, the loop's branch, the session or the model's output, and no pattern across misses to look for.
However, I do realize that criterion #5 was very easy to pass & while I made it to test the model, I should've
known it wasn't an issue that I needed to worry about, so I'll rewrite criterion #5 to check matches & see if we got the best
match based on closest match to description, then by lowest price available.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
python app.py ask 'silk slip dress in midi length under $40' --empty-wardrobe –trace
```

```
(running with an empty wardrobe)

  Found:    90s Silk Slip Dress — Floral, Midi Length — $30.0 on depop,  size : M
  Outfit:   Outfit 1: Grunge Contrast
Layer an oversized black knit cardigan over the slip dress and pair with chunky black combat boots.
Vibe: 90s Courtney Love grunge meets delicate romance.

Outfit 2: Casual Layering
Wear a plain white fitted t-shirt underneath the slip dress and finish with white canvas low-top sneakers.
Vibe: Easy, everyday 90s streetwear.

  Fit card: Just scored this floral midi 90s silk slip dress on Depop for thirty bucks and I am totally channeling Courtney Love with an oversized black knit cardigan and chunky combat boots. For a more casual streetwear vibe, I'm definitely throwing a white fitted tee underneath and pairing it with low-top sneakers. 🖤

[1] call_tool
      in:  tool: search_listings, params='description, size, max_price'
      out: 90s Silk Slip Dress — Floral, Midi Length ($30.0, depop)
[2] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: Outfit 1: Grunge Contrast Layer an oversized black knit cardigan over the slip dress and pair with chunky blac…
      →    Branch: No wardrobe, give general styling advice
[3] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: Outfit 1: Grunge Contrast Layer an oversized black knit cardigan over the slip dress and pair with chunky blac…
2 model calls this session, 455 prompt + 148 output tokens

```

**Empty search**

```
python app.py ask 'platform sneakers size 11' --trace
```

```
  No items matched 'platform sneakers' in size 11. Try a broader description, a different size, or a higher price cap.

[1] call_tool
      in:  tool: search_listings, params='description, size, max_price'
      →    branch: empty, stopping
0 model calls this session
```

**On the MCP move:**
It worked from what I could tell, acted pretty much the same. I just changed the call to
mcp.call_tool with the tool and its params, and added my trace steps

<!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
Didn't change anything since I passed all criteria before

**Which failure it was meant to fix:**
N/A

### Run Log — After

| #   | Criterion                                                     | Target | Verdict | How I decided                                                                                                                |
| --- | ------------------------------------------------------------- | ------ | ------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1   | Matching query completes                                      | 5 of 5 | MET     | Compared all five tries in the run log. All five PASSED (5/5), which meets the target of 5 of 5.                             |
| 2   | Impossible query stops early                                  | 5 of 5 | MET     | Compared all five tries in the run log. All five PASSED (5/5), which meets the target of 5 of 5.                             |
| 3   | State of selected item                                        | 5 of 5 | MET     | Compared all five tries in the run log. All five PASSED (5/5), which meets the target of 5 of 5.                             |
| 4   | Fit card gives unique, structured responses                   | 4 of 5 | MET     | Compared all five tries in the run log. all five fit cards were different strings and each named the price and platform once |
| 5   | Item gets best match based on description, ties go to cheaper | 4 of 5 | MET     | Compared all five tries in the run log. 4 PASSED (4/5), which meets the target of 4 of 5.                                    |

**Did it help, and how do I know:**
It helped actually understanding what my system does well & what could be tweaked a bit with how I am
ranking my matches in search_listings.

---

## What's Still Broken

Everything is working as intended. Would ideally want to tweak search_listings so that
item queries matching style tags are stripped from consideration, so that an item that
doesn't mention a specific style but has the style tag will be considered as a priority
if it matches all other query requirements and is cheaper.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
