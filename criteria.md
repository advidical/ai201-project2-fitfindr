# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. _"The agent handles errors"_ is an opinion.
_"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"_ is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; _"80% seemed reasonable"_ does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
My search is a plain keyword match w/ some formatting, so it's very natural that some phrasings will miss

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
this should work all the time, because a query with no listings means there is no
valid input for suggest_outfit. Without that, suggest_outfit will crash the system.

---

## 3. State of selected item is consistent across tool calls

Given a selected item chosen from a list of matching items, the agent picks the first item returned
(provided in session["search_results"]), puts it in session["selected_item"], and sends session["selected_item]
as the new_item (dict) param for suggest_outfits(). Use a comparison test between first result & item in selected item
for clarity — 5 of 5 times.

**Why this target:**
We want to be absolutely sure what we give to suggest_outfit is what we picked based on our results, otherwise
a state management problem will be disguised as a tool problem, which will lead to hours of searching for a bug
in the tools when the problem resulted from how we pass things along tools.

---

## 4. The fit card gives a unique, structured response almost every time

Given a valid outfit suggestion, the fit card should provide a unique caption, compared
mainly by different outfit suggestion combinations, structured as such. Starts with a line or two
mentioning each item with its price & brand (if applicable), and then a line or two to describe
overall vibe of the outfit (ie what style does it represent or what feeling does it evoke to other people
seeing someone dressed like this) — should be at least 4 out of 5 times.

**Why this target:**
I want to reproduce realistic captions that looks like a user who bought the outfit,
and I want it to at least be accurate enough to be able to do it 80% of the time to account
for edge cases where there might not be a wardrobe or not large enough wardrobe, which might result
in very similar answers.

---

## 5. Respects price ceiling at all times

For any given user query, the top matching result (which will be passed to suggest_outfit)
must be at most the specified price ceiling, ex. under $30 means price < $30, around $30 is price <= $30, etc.
You compare that value to the max_price given in the top matching result - should be 5 out of 5 times

**Why this target:**
I want to make sure that outfit requests are able to respect price ceiling at all times when given,
especially because it requires just a simple check.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
