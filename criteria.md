# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

Of 10 pieces of text I wrote myself, at most 1 is labeled high-confidence AI.

**Why this target:** Signal one's blind spot (perplexity) penalizes
predictable, plainly-written text regardless of who actually wrote it —
exactly the kind of honest, simple writing a real person produces. The system
has to stay conservative about accusing real writers; the appeal path exists
to catch the rare miss, not to excuse a looser first judgment.

---

## 2.

The combined score for clearly-AI text and clearly-human text differs by at
least 0.3.

**Why this target:** A smaller gap isn't convincing evidence the two signals
are distinguishing anything real — it could just as easily be noise. 0.3 is
large enough that the difference can't be explained away as coincidence.

---

## 3.

I can find at least one real piece of text that produces each of the three
labels — human, unsure, and AI.

**Why this target:** A label that can never actually be produced is a label
that doesn't exist, no matter how the scoring math underneath it was
designed. This has to be checked by submitting real text and observing the
output, not by inspecting the weights — if a label isn't reachable, that's a
scoring bug to fix in Milestone 5, not a detail to note and move past.

---

## 4.

Every appeal changes the submission's status to `under_review` and is
recorded in the audit log. Both happen every time, with no exceptions.

**Why this target:** The appeal is the only recourse a wrongly-accused writer
has. A path that works most of the time is, for the person it fails, the
same as no path at all.

---

## 5.

Missing or empty `text` returns HTTP 400 with a clear error message. Text
over 20,000 characters returns HTTP 413 with a clear error message. Neither
case ever returns a 500.

**Why this target:** A crash on bad input is one of the most common real
failures a service has. Missing data and too much data are different
problems for a caller to fix, so they get different status codes instead of
being lumped into one generic error.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone — five new criteria, unaided

Written before any capstone results exist, same rule as units 7/8: no
template, no worked examples. Four of five are about the extension itself
(the timing/failure instrumentation added this unit); one checks the
original system didn't regress.

## 1. Every call writes a complete instrumentation record

Across 20 `/submit` calls (15 ordinary, 5 deliberately malformed enough to
crash signal one), every single one produces a log entry containing
`input_length`, `status`, and either both duration fields (`decided`) or
`total_duration_ms` + a `reason` (`rejected`) — 20 of 20, zero gaps.

**Why this target:** this unit's own warning is "a failure that shows up
only as an absence is one you'll never find" — a logging layer that's
*mostly* reliable is worse than one that's visibly unreliable, because a
gap in an audit trail looks exactly like a quiet period. The standard has
to be perfect, not "most of the time."

## 2. The cost measurement is stable, not a fluke

Across 10 identical-input warm requests, `signal_one_duration_ms` stays
within ±20% of the 10-run mean in at least 9 of 10.

**Why this target:** a number that swings wildly run to run isn't a
measurement, it's one lucky or unlucky sample dressed up as one. 20% is
loose enough to absorb ordinary OS scheduling jitter on a laptop CPU, but
tight enough to catch something real going wrong — a memory leak slowing
later runs, say — rather than passing no matter what happened.

## 3. Instrumentation overhead stays small next to what it measures

`total_duration_ms − signal_one_duration_ms` (everything that isn't
signal one: the style signal, combining, labeling, the log write) stays
at or under 5ms in at least 9 of 10 runs.

**Why this target:** logging that costs as much as the thing it's
measuring corrupts the number it's trying to report. 5ms is roughly 10%
of the ~50ms warm signal-one time already observed — tight enough to
matter, loose enough that ordinary Python/JSON-write overhead doesn't
trip it by accident.

## 4. A crash in signal one is always caught and always logged

A request engineered to crash signal one (text under the 3-token minimum)
never returns a raw, unhandled 500 and always produces a log entry with
`reason: "signal_one_error"` — 5 of 5 trials.

**Why this target:** this exact gap was invisible through all of unit 8
(MF02, RQ07) because nothing caught the exception before it reached the
log call. The fix this unit made only counts if it holds every time — the
one trial it doesn't fire is indistinguishable, from the outside, from
the bug never having been fixed at all.

## 5. The instrumentation change didn't break anything it touches

`/ping`, `/health`, and the full submit→appeal flow each return their
documented shape and status code in 5 of 5 calls, after the timing and
failure-logging changes.

**Why this target:** an extension that works but silently breaks
something else is a regression I'd find out about from a real user, not
from testing — cheap to rule out now with a blunt, repeated check rather
than trusting "I didn't touch that file."
