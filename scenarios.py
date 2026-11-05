"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Ten short paragraphs I actually wrote for this evaluation — casual,
        # first-person, uneven sentence lengths, the ordinary register of
        # someone just typing out a thought rather than drafting formal prose.
        "texts": [
            "I finally fixed the bug that's been bugging me since Tuesday. Turned out "
            "it was a one-character typo in a config file, of course.",
            "Woke up late today and missed the bus, so I just walked the whole way in. "
            "Not the worst thing, honestly — needed the air.",
            "My roommate keeps leaving dishes in the sink and I keep not saying "
            "anything about it. One of these days I'll actually bring it up.",
            "Tried a new recipe last night, way too much garlic. Still ate the whole "
            "thing though, no regrets.",
            "I've been putting off calling the dentist for like three weeks now. I "
            "know, I know. I'll do it this week. Probably.",
            "The group project is going fine except nobody has touched the slides "
            "yet and the presentation is Thursday. Classic.",
            "Took my little cousin to the park and she insisted on going down the "
            "same slide like twenty times in a row. Kids are weird like that.",
            "I keep meaning to read more but every time I sit down I just end up on "
            "my phone instead. Starting to feel like a lost cause.",
            "Spent way too long picking a paint color for my room and ended up just "
            "going with the first one I liked anyway.",
            "My car made a weird noise on the way home so now I'm just hoping it "
            "goes away on its own, which I realize is not how cars work.",
        ],
    },
    {
        "name": "score spread, clearly AI vs clearly human",
        "criterion": 2,
        # One text generated to read as typical AI-style prose, one written in
        # my own plain voice — far enough apart to check the 0.3 gap.
        "texts": [
            "Leveraging cutting-edge methodologies, our comprehensive solution "
            "empowers organizations to optimize operational efficiency while "
            "simultaneously enhancing stakeholder engagement across diverse "
            "functional domains. This holistic approach facilitates seamless "
            "integration of best practices, ultimately driving sustainable value "
            "creation and fostering a culture of continuous improvement.",
            "Honestly I just wanted to vent for a sec because today was kind of a "
            "mess. My alarm didn't go off, I spilled coffee on my only clean shirt, "
            "and then the printer at work jammed right before my meeting. "
            "Somehow I still laughed about it on the drive home though.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs spread across the score range, so all three labels are
        # actually reachable, not just theoretically possible.
        "texts": [
            "Leveraging cutting-edge methodologies, our comprehensive solution "
            "empowers organizations to optimize operational efficiency while "
            "simultaneously enhancing stakeholder engagement across diverse "
            "functional domains. This holistic approach facilitates seamless "
            "integration of best practices, ultimately driving sustainable value "
            "creation and fostering a culture of continuous improvement.",
            "Honestly I just wanted to vent for a sec because today was kind of a "
            "mess. My alarm didn't go off, I spilled coffee on my only clean shirt, "
            "and then the printer at work jammed right before my meeting. "
            "Somehow I still laughed about it on the drive home though.",
            "The meeting covered the quarterly budget. Sales were up slightly. "
            "Marketing requested additional resources for the next campaign. "
            "The team agreed to revisit the topic next month.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        # Raw request bodies — the point IS the malformed shape, so this has
        # to be "bodies", not "texts".
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   ", "creator_id": "eval_bad_whitespace"},
            {"creator_id": "eval_bad_missing"},          # no text field at all
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },

    # Criterion 4 (appeal path) isn't here on purpose: it needs a real
    # content_id from a prior submission before it can appeal against it,
    # which run_eval.py's single-pass texts/bodies model can't express. It's
    # run separately with run_appeal_eval.py (same --trials/--label idea,
    # three submit+appeal round trips per run) — see criteria.md writeup.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
