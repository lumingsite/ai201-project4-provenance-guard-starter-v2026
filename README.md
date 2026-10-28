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
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



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

**An appeal**

`/appeal` isn't built yet (Milestone 5). Here's its current, honest state —
the starter's 501, not a fake success:

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "706ebbf3-3d81-4963-8d5e-c9e3dfad2566", "reasoning": "I wrote this myself"}'
```

```json
{
  "error": "not_implemented",
  "message": "POST /appeal isn't built yet — see the TODO in app.py.",
  "you_sent": {
    "content_id": "706ebbf3-3d81-4963-8d5e-c9e3dfad2566",
    "reasoning": "I wrote this myself"
  }
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "creator_id": "tester1",
      "event": "rejected",
      "reason": "missing_or_empty_text",
      "status": "rejected",
      "timestamp": "2026-10-28T23:40:17+00:00"
    },
    {
      "creator_id": "tester1",
      "event": "rejected",
      "length": 20005,
      "max_allowed": 20000,
      "reason": "text_too_long",
      "status": "rejected",
      "timestamp": "2026-10-28T23:40:17+00:00"
    },
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
    }
  ]
}
```

The two `rejected` entries above are from testing criteria.md #5 (missing
text and oversized text) before this submission — proof the bad-input
handling logs a trace instead of just returning an error and vanishing.

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

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
