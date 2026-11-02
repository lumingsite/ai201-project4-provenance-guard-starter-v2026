# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

**The path a submission takes:**

1. A writer sends `POST /submit` with `{"text": ..., "creator_id": ...}`.
2. The route generates a `content_id` (a uuid) so this submission can be
   found again later, by `/log` or by an appeal.
3. **Signal one** runs: `detector.model_signal(text)` loads `gpt2` locally,
   measures how predictable the text is (perplexity), and turns that into a
   0–1 `model_score` (higher = more AI-like).
4. **Signal two** runs: `stylometry.style_signal(text)` measures the text's
   shape — sentence-length spread, vocabulary variety, punctuation density —
   with no understanding of what it says, and turns that into a 0–1
   `style_score` (same direction as signal one).
5. `scoring.combine_signals(model_score, style_score)` merges the two into
   one `combined_score` from 0.0 (confidently human) to 1.0 (confidently AI).
6. `scoring.score_to_label(combined_score)` turns that number into a
   `guess` (`human` / `unsure` / `ai`) and the actual sentence a reader sees.
7. `audit.log_decision(...)` writes the whole decision — both signal scores,
   the combined score, the guess, the label — to the append-only log, and the
   route returns `content_id`, `guess`, `confidence`, `label`, `model_score`,
   and `style_score` to the caller.

**Trace the false positive:** a real person — someone writing in a second
language, or a younger writer, or anyone who writes short, plain sentences on
purpose — submits work they wrote themselves.

- Signal one's blind spot is exactly their situation: plain vocabulary in
  short, ordinary sentences is *predictable*, and predictable is what
  `model_signal` rewards with a high (AI-like) score. They get penalized for
  writing simply, not for using AI.
- Signal two can't rescue them either. If their honest writing also happens
  to keep a fairly even rhythm and a narrower vocabulary (which plain,
  unpretentious writing often does), `style_score` doesn't necessarily push
  back — it has no way to tell "simple because that's how this person
  writes" from "simple because a model generated it."
- Both signals landing AI-like pushes `combined_score` into the
  high-confidence-AI band. The label text they see has to carry real weight,
  because it may be flatly wrong about them.
- What they can do about it right now: **nothing** — `/appeal` doesn't exist
  yet (that's Milestone 5). Until then, a wrongly-accused plain writer has no
  path back. This is the scenario `criteria.md`'s "expensive mistake is
  one-sided" framing is about, and it's why the thresholds in Milestone 5 and
  the appeal path matter more than squeezing out a slightly better score.

**The two endpoint shapes:**

`POST /submit`

```
in:  {"text": "string, required", "creator_id": "string, required"}
out: {
  "content_id":  "string — uuid, used by /appeal and /log",
  "guess":       "string — \"human\" | \"unsure\" | \"ai\"",
  "confidence":  "float 0–1",
  "label":       "string — the full sentence a reader sees",
  "model_score": "float 0–1 — signal one",
  "style_score": "float 0–1 — signal two"
}
```

Decided before coding, not after: missing, empty, or enormous `text` gets a
4xx and a logged rejection (`audit.log_rejection`) — never a crash and never
a silent 200.

`POST /appeal`

```
in:  {"content_id": "string, required — must match an existing submission",
      "reasoning": "string, required"}
out: {
  "content_id": "string",
  "status":     "\"under_review\"",
  "message":    "string — confirmation shown to the writer"
}
```

A `content_id` that doesn't exist (checked via `audit.entries_for`) gets a
clear 404, not a silent no-op that looks like the appeal worked when it
didn't.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity — how surprised a local language model
(`gpt2`) is by the text, i.e. how predictable it finds each next word. That
gets squashed into a 0–1 score where higher means more likely AI.

**Why that might differ between human and AI writing:** A language model
writes by repeatedly picking a likely next word, so text a model produced
tends to be text a model (even a different one) finds easy to predict. Human
writing wanders more — odd word choices, abrupt turns, the specific rather
than the typical.

**What it can't see:** The difference between "predictable because an AI
wrote it" and "predictable because the writer is being plain on purpose."
Someone writing in a second language, a younger writer, or anyone sticking to
vocabulary they're sure of all score about as machine-like as actual machine
writing. The reverse is also blind: dense, ornate prose full of rare words
reads as *human* here, because rare words are exactly what the model fails to
predict — regardless of who or what actually wrote them.

### Signal two — the style signal

**What it measures:** The shape of the text, not its meaning — how much
sentence length varies, how much the vocabulary repeats, how much (and what
kind of) punctuation shows up.

**Why that might differ between human and AI writing:** Generated prose
tends toward even, mid-length sentences and a narrower band of vocabulary,
because that's what "most likely next word" produces on average. Human
writing is lumpier — a three-word sentence next to a forty-word one.

**What it can't see:** It cannot read. It has no idea what the text actually
says, so anything that changes the text's shape without touching its
substance moves the score — adding typos, re-breaking sentences, pasting in
a quoted passage. That's a cheap, deliberate thing for someone to do, and
it's exactly what Unit 8's attack set is built to exploit.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted average — `combined = 0.9 * model_score + 0.1 *
style_score` — weighted heavily toward the model signal, because the
calibration run below showed it discriminates and the style signal, as
built, mostly doesn't.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.9`, `WEIGHT_STYLE_SIGNAL = 0.1` in
`config.py`. Thresholds unchanged from the starter: `HUMAN_THRESHOLD = 0.35`,
`AI_THRESHOLD = 0.65`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**The four calibration texts, both signals, and the combined score:**

| Text | model_score | style_score | combined | lands as |
|---|---|---|---|---|
| Clearly AI (generic formal paragraph) | 0.7035 | 0.4472 | 0.6779 | `ai` |
| Clearly human (casual, first-person) | 0.1766 | 0.5001 | 0.2090 | `human` |
| Formal human (plain, specific personal detail) | 0.4665 | 0.5009 | 0.4700 | `unsure` |
| Lightly-edited AI (same paragraph, loosened up) | 0.6559 | 0.4736 | 0.6377 | `unsure` |

Why the weighting: `model_score` produced a clean, monotonic order across all
four — exactly the order you'd want (human lowest, AI highest, the two
harder cases in between). `style_score` did not: it clustered tightly
between 0.45 and 0.50 on all four, and even ran backward once — the
*clearly-AI* paragraph scored more human-like on style than the plain,
human-written formal paragraph did. That's a real, measured finding, not a
guess: at this text length (one short paragraph, 2–4 sentences), two of
style_signal's three components turned out to be close to useless.
`sentence_length_spread` needs more sentences than a short submission has to
mean anything, and `type_token_ratio` runs high for any short text
regardless of who wrote it — the stub's own docstring warned about both of
these, and the calibration run confirmed it. (`punctuation_density` had its
own bug, fixed before this table was generated: short text of either origin
very often has zero semicolons/colons/dashes, and scoring "zero marks" as
"maximally AI-like" was punishing plain writing again, the exact blind spot
signal one already has. Zero marks now scores neutral instead of worst-case.)
Given that, folding `style_score` in at equal weight would let a
demonstrably noisier signal drag down a signal that's actually working — so
it's kept in at a small weight rather than dropped, since it's still real
information when `model_score` itself is uncertain.

**A case where my two signals split, and what my rule does with it:** The
*clearly human* text: `model_score` = 0.1766 (confidently human) while
`style_score` = 0.5001 (no opinion at all — too few sentences to show
spread, and plain language that registers as neither narrow nor varied
enough to move the vocabulary measure). At 0.9/0.1 weighting the combined
score stays close to what `model_score` already knew (0.209, still clearly
human). An equal-weight average would have landed at ≈0.338 — hugging the
human threshold for no good reason, on the strength of a signal that
genuinely had nothing to say either way.

Which way this is deliberately wrong: weighting this heavily toward one
signal means a submission that specifically fools `model_score` (reads as
unpredictable to GPT-2 while still being AI-generated by something else)
gets very little pushback from `style_score`. That trade favors fewer false
accusations of real writers over catching every evasion — the one-sided
mistake named in `criteria.md` #1.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was written by a person. No action is needed." |
| unsure | 0.35 – 0.65 | "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it just means our system didn't find a clear signal either way. Nothing happens to your account because of this." |
| high-confidence AI | 0.65 – 1.00 | "We think this was likely written by AI. If you wrote this yourself and believe this is wrong, you can appeal this decision and a person will take a look." |

All three confirmed reachable with real submissions (Milestone 4's
calibration texts): clearly-human → `human` (0.209), formal-human and
lightly-edited-AI → `unsure` (0.470, 0.638), clearly-AI → `ai` (0.678).

**Why I worded the "unsure" one this way, and what I found when I checked
it:**

I wrote "this isn't an accusation" specifically to head off the fear that
"unsure" is a soft version of "guilty." I tested this the way the milestone
asks — gave Claude just the label text, no system explanation, and asked
what a writer would think reading it cold, without asking it to rewrite
anything.

The gap: a writer reading "this isn't an accusation" doesn't feel reassured
by it — they notice that the sentence only exists because an accusation was
possible, and start wondering whether something about their writing looked
suspicious enough to need that disclaimer in the first place. The attempt at
reassurance draws attention to the exact thing it's trying to defuse.

Rule I'm going with for this unit: **keep the current wording and write the
gap down rather than patch it blind.** I only have one piece of outside
feedback on one label, and rewording now risks trading a known, named
problem for an unknown one I haven't tested at all. The label still does the
two things the milestone actually requires — it admits uncertainty, and it
doesn't tell the writer anything happened to their account — so it's not
broken, just imperfect in a specific, now-documented way. If a future
pass revisits this, the fix to try first is cutting the reassurance clause
entirely rather than strengthening it: "We couldn't confidently tell whether
this was written by a person or by AI. Nothing happens to your account
because of this." — stating the fact plainly instead of naming the fear and
then denying it.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "ok so I missed the bus AGAIN, third time this week, and my phone died right as I needed the map lol. anyway I walked 40 min and now my feet are destroyed, 10/10 would not recommend mondays", "creator_id": "yingfei"}'
```

```json
{
  "content_id": "5347b046-81be-4291-b1ef-c098a399c532",
  "guess": "human",
  "confidence": null,
  "label": "PLACEHOLDER — write the high-confidence human label.",
  "model_score": 0.1766,
  "style_score": 0.5001,
  "combined_score": 0.20895
}
```

Both signals and the combined score are real as of Milestone 4 — only
`confidence` and the real label text are still Milestone 5 placeholders.

**A submission that lands `ai` (used for the appeal below)**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "It is important to note that effective time management involves several key strategies. First, individuals should prioritize tasks based on their urgency and importance. Additionally, breaking larger projects into smaller, manageable steps can significantly improve productivity and reduce overall stress levels.", "creator_id": "yingfei"}'
```

```json
{
  "content_id": "1e644fad-eb8c-4caa-9b91-2e3b65aff3ed",
  "guess": "ai",
  "confidence": 0.0796,
  "label": "We think this was likely written by AI. If you wrote this yourself and believe this is wrong, you can appeal this decision and a person will take a look.",
  "model_score": 0.7035,
  "style_score": 0.4472,
  "combined_score": 0.67787
}
```

**An appeal, using that `content_id`**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "1e644fad-eb8c-4caa-9b91-2e3b65aff3ed", "reasoning": "I wrote this myself as part of a work report, I did not use AI."}'
```

```json
{
  "content_id": "1e644fad-eb8c-4caa-9b91-2e3b65aff3ed",
  "status": "under_review",
  "message": "Your appeal has been recorded. A person will review this decision."
}
```

**An appeal against a `content_id` that doesn't exist (the typo case the
milestone warns about)**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "does-not-exist", "reasoning": "test"}'
```

```json
{
  "error": "not_found",
  "message": "No submission found with content_id 'does-not-exist'."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=5"
```

```json
{
  "count": 5,
  "entries": [
    {
      "combined_score": 0.20895,
      "content_id": "5347b046-81be-4291-b1ef-c098a399c532",
      "creator_id": "yingfei",
      "guess": "human",
      "label": "PLACEHOLDER — write the high-confidence human label.",
      "model_score": 0.1766,
      "status": "decided",
      "style_score": 0.5001,
      "timestamp": "2026-10-28T23:48:23+00:00"
    },
    {
      "combined_score": 0.20895,
      "content_id": "4036e1e8-225b-4669-a4f1-13a6ac82508f",
      "creator_id": "yingfei",
      "guess": "human",
      "label": "We think this was written by a person. No action is needed.",
      "model_score": 0.1766,
      "status": "decided",
      "style_score": 0.5001,
      "timestamp": "2026-11-02T15:40:50+00:00"
    },
    {
      "combined_score": 0.4699400000000001,
      "content_id": "dabcc45a-2c51-48f7-93b1-09e3531b094f",
      "creator_id": "yingfei",
      "guess": "unsure",
      "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
      "model_score": 0.4665,
      "status": "decided",
      "style_score": 0.5009,
      "timestamp": "2026-11-02T15:40:50+00:00"
    },
    {
      "combined_score": 0.67787,
      "content_id": "1e644fad-eb8c-4caa-9b91-2e3b65aff3ed",
      "creator_id": "yingfei",
      "guess": "ai",
      "label": "We think this was likely written by AI. If you wrote this yourself and believe this is wrong, you can appeal this decision and a person will take a look.",
      "model_score": 0.7035,
      "status": "decided",
      "style_score": 0.4472,
      "timestamp": "2026-11-02T15:40:50+00:00"
    },
    {
      "content_id": "1e644fad-eb8c-4caa-9b91-2e3b65aff3ed",
      "creator_id": "yingfei",
      "event": "appeal",
      "reasoning": "I wrote this myself as part of a work report, I did not use AI.",
      "status": "under_review",
      "timestamp": "2026-11-02T15:40:59+00:00"
    }
  ]
}
```

The original `decided` entry for `1e644fad-...` is still there, untouched —
the log is append-only. The `appeal` entry right after it is what actually
carries the new `under_review` status; the decision itself isn't rewritten,
which is the whole point of an audit trail someone could check later.

---

## How I Used AI

**Moment 1**

- *What I asked for:* In Milestone 4, after `style_signal` produced nearly
  identical scores (0.61–0.67) across all four calibration texts — including
  the clearly-AI and clearly-human ones — I asked Claude to help me figure
  out which of the three measures was responsible, rather than just
  re-weighting blind.
- *What came back:* Running each measure separately on the four texts showed
  `punctuation_density` returning exactly 0.0 for every single one. The
  diagnosis: short calibration text almost never contains semicolons,
  colons, or em-dashes, so treating "zero marks" as "maximally AI-like" was
  applying a constant penalty to everyone, not measuring anything.
- *What I changed:* Rewrote that sub-score so zero marks reads as neutral
  (0.5) instead of worst-case, and documented the bug and the fix in
  `stylometry.py` and the README rather than silently patching it.

**Moment 2**

- *What I asked for:* For the Milestone 5 "talk this through" check, I had
  Claude read my three label texts cold — as a writer encountering them with
  no system context — and say what each would make them think and do next,
  without rewriting the wording.
- *What came back:* For the `unsure` label, the read was that "this isn't an
  accusation" doesn't land as reassurance — it signals that an accusation
  was possible in the first place, which is the exact anxiety the sentence
  was trying to head off.
- *What I changed:* I decided not to reword the label on the strength of one
  reaction to one phrasing. Instead I documented the gap plainly in the
  README, along with the specific alternative I'd try next (dropping the
  reassurance clause and stating the fact plainly) if a future pass revisits
  it — a named, evidenced problem instead of an untested rewrite.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 100 per day

**Why those numbers and not others:** A real writer iterating on a single
piece might resubmit a handful of times in a minute while editing, but
rarely faster than once every 10-15 seconds — 5/minute is generous room for
that without being anywhere near what a script sending rapid-fire variations
to map the thresholds would want. 100/day covers someone checking many
separate pieces across a very heavy day, while still making a bulk automated
sweep expensive rather than free.

**What a caller counts as:** `creator_id`, falling back to the caller's IP
address only if `creator_id` is missing or not a string (the starter's
`rate_limit_key`). This is the more human-centered choice — a shared office
network shouldn't all count as one caller — but it has an obvious failure
mode: nothing stops an attacker from sending a different `creator_id` on
every request to appear as a thousand separate "callers" and dodge the limit
entirely. That gap is a `creator_id`-authentication problem this project
doesn't solve, not something the rate limiter itself can fix.

**The run of status codes when I pushed past it:**

```bash
$ python run_attacks.py --flood 15
```

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================
```

Exactly 5 through, then 429 for the rest — matching the 5/minute limit. `GET
/log` confirms each 429 was recorded as a `rejected` entry with
`reason: "rate_limited"`, not just returned and forgotten.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
