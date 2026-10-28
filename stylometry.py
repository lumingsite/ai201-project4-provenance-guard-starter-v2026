"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.

    Returns:
        The coefficient of variation of sentence length (stdev / mean word
        count per sentence). Unbounded, >= 0. **Higher means more human** —
        lumpy, uneven sentences. Low/zero means sentences march in step,
        which is more AI-like.

    Edge case: fewer than two sentences gives no spread to measure. `stdev`
    raises on fewer than two values, so that case returns -1.0 as a sentinel
    (not "zero spread" — zero spread would wrongly read as maximally AI-like).
    `style_signal` treats -1.0 as "can't tell" and scores it neutral (0.5)
    rather than guessing.
    """
    sents = sentences(text)
    if len(sents) < 2:
        return -1.0

    lengths = [len(words(s)) for s in sents]
    mean_len = statistics.mean(lengths)
    if mean_len == 0:
        return -1.0

    return statistics.stdev(lengths) / mean_len


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0 and 1. **Higher means more varied vocabulary**,
        which this module treats as more human — generated text tends toward
        a narrower, more repetitive word choice.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths
    aren't directly comparable on it.
    """
    w = words(text)
    if not w:
        return 0.0
    return len(set(w)) / len(w)


def punctuation_density(text: str) -> float:
    """
    How much "interesting" punctuation shows up, relative to word count.

    Returns:
        A float >= 0. Counts semicolons, colons, em/en dashes, and
        parentheses — not periods or commas, which are common enough in both
        human and AI writing to say little on their own. **Higher means more
        human** — varied punctuation choices are a writer's habit; plain
        generated prose tends to lean on simple full stops and commas.

    Divided by word count rather than character count so a short and a long
    text are comparable.
    """
    w = words(text)
    if not w:
        return 0.0
    marks = re.findall(r"[;:—–()]", text)
    return len(marks) / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    All three measures above are written so that a HIGHER raw value means
    MORE human. This function inverts each to an "AI-likeness" sub-score
    before averaging, so the direction matches `detector.model_signal`
    (higher = more likely AI) and `scoring.combine_signals` can treat both
    the same way.

    Scaling, decided and written down here rather than left implicit:

      - `sentence_length_spread` is an unbounded coefficient of variation.
        Squashed with `1 / (1 + spread)`: spread 0 -> 1.0 (max AI-ish),
        spread growing -> approaches 0. A -1.0 sentinel (too few sentences
        to measure) scores neutral (0.5) instead of guessing either way.
      - `type_token_ratio` is already 0–1, so it's just inverted (`1 - ttr`).
      - `punctuation_density` is unbounded but small in practice. Capped at
        `PUNCT_DENSITY_CAP` interesting marks per word, then inverted —
        anything at or above the cap scores as maximally human-like on this
        measure, so one heavy semicolon-user doesn't dominate.

        ⚠️ Found while calibrating (see README): short, ordinary text of
        either origin very often has ZERO semicolons/colons/dashes/parens at
        all — these marks are simply rare at this length. Treating "zero
        marks" as "maximally AI-like" punished every short, plain submission
        regardless of who wrote it, which is exactly the blind spot
        detector.py warns about, just reintroduced by this module. Zero
        marks now scores neutral (0.5) instead of the worst case.

    The three sub-scores are averaged unweighted. Tested against the four
    calibration inputs from Milestone 4 (clearly AI, clearly human, formal
    human, lightly-edited AI) — see README for what those four produced and
    whether this direction/scaling held up.
    """
    PUNCT_DENSITY_CAP = 0.08  # ~1 interesting mark per 12 words

    spread = sentence_length_spread(text)
    if spread < 0:
        spread_ai = 0.5
    else:
        spread_ai = 1.0 / (1.0 + spread)

    ttr = type_token_ratio(text)
    ttr_ai = 1.0 - ttr

    punct = punctuation_density(text)
    if punct <= 0:
        punct_ai = 0.5  # absence isn't evidence — see the note above
    else:
        punct_ai = 1.0 - min(punct / PUNCT_DENSITY_CAP, 1.0)

    score = (spread_ai + ttr_ai + punct_ai) / 3.0
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
