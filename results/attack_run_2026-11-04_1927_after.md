# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 19:27
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `92675fe8-3099-4dd5-9eb8-bb005fd1ca54` | unsure | 0.000 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c127a83e-0e02-48c5-af02-c0eb66699ded` | unsure | 0.000 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `08cf778c-ac36-47fd-926f-19eddcbfe193` | unsure | 0.000 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `d78402fb-cda7-4b32-b57f-84e1eda0096d` | unsure | 0.000 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `107c1dbe-a511-4fc1-86c3-5d04c4ddea64` | unsure | 0.000 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `39d85cf8-a712-4cdd-9179-f36a5c4d2b9d` | unsure | 0.000 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e7b87a41-223e-4b3d-af11-a77fc1d3aa5b` | unsure | 0.000 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `6576483d-8444-4c32-8714-23cfba5d66dc` | unsure | 0.000 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `792ff191-9ef1-4cb2-a9a5-ea1a588c095e` | unsure | 0.000 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `4502f1bf-df14-4062-a4ce-f83c997699b5` | ai | 0.247 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0a5b6c37-d01b-4533-9a7f-30ec3d0c1323` | unsure | 0.000 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `12ea3d79-f691-47ba-a129-4cc948663e4d` | unsure | 0.000 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `f16305e1-042b-43d6-b9a3-f27d2b2d9aca` | unsure | 0.000 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `901cd540-cfb6-40ec-93e6-3d81827d7e52` | unsure | 0.000 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `1c98fc56-3fe0-44fa-9f38-e584a144c0b0` | unsure | 0.000 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `e5741f52-616e-4f9f-a31b-5a6b6166d42e` | unsure | 0.000 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `4fe0847c-7412-4e45-b0d1-7dc26a5ded80` | unsure | 0.000 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `087de0df-41ca-4a81-81d1-5c1d9dd0d5e1` | unsure | 0.000 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c5203ea4-2e60-4bdb-abf1-49979d5ed436` | unsure | 0.000 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `6936f291-aaca-4d60-bedc-78f9d8afb1d9` | unsure | 0.000 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2a07e479-04bf-4652-8c5a-d32a13926608` | unsure | 0.000 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `5106da21-990c-4950-8194-0dcab88e1472` | unsure | 0.000 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4d1ae2f0-0b61-4ed6-91cf-b1391bfa5542` | unsure | 0.000 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `f8d304ba-56d1-4c41-bec7-c9a8226af3f3` | unsure | 0.000 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `a2d5fe5c-a2be-4880-abb9-10e25686c7f8` | human | 0.333 |  |
| MF04 | malformed | text is only punctuation | 200 | `dbf1beee-6dbb-41f2-acd9-13928aa06224` | unsure | 0.000 |  |
| MF05 | malformed | text is a very long single word | 200 | `476ff68e-8a30-4fbf-8811-1837283bebc7` | unsure | 0.000 |  |
| MF06 | malformed | text is emoji only | 200 | `c6e273d6-4d4b-4364-ab36-9e381b783cc3` | ai | 0.331 |  |
| MF07 | malformed | text is right-to-left script | 200 | `9c7630d2-b8b6-4610-bf6d-67384e0e1c64` | ai | 0.253 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `7d40b6c2-5e55-4bbd-80c7-abc710e415ec` | human | 0.128 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `7349a539-edb6-4c38-919a-5aa1031b3e64` | human | 0.291 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7f55778d-1887-4f8d-bd58-7c8d972c3398` | human | 0.309 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d7b5c5a2-23ff-4f12-8849-f0d6a7d2465c` | human | 0.309 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `58ba5358-7d99-4557-b4b5-9d95eba39663` | human | 0.309 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `95236d0b-a8c9-4e55-840f-868cc55e7ce8` | human | 0.309 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2bba2add-b119-4e12-afa7-0f461d28dd2a` | human | 0.309 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "92675fe8-3099-4dd5-9eb8-bb005fd1ca54",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.1635,
  "style_score": 0.497,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c127a83e-0e02-48c5-af02-c0eb66699ded",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.5943,
  "style_score": 0.4348,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "08cf778c-ac36-47fd-926f-19eddcbfe193",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.6662,
  "style_score": 0.5784,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "d78402fb-cda7-4b32-b57f-84e1eda0096d",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.6114,
  "style_score": 0.4932,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "107c1dbe-a511-4fc1-86c3-5d04c4ddea64",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.3212,
  "style_score": 0.5587,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "39d85cf8-a712-4cdd-9179-f36a5c4d2b9d",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.5727,
  "style_score": 0.4025,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "e7b87a41-223e-4b3d-af11-a77fc1d3aa5b",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.5862,
  "style_score": 0.2749,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "6576483d-8444-4c32-8714-23cfba5d66dc",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.2452,
  "style_score": 0.4265,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "792ff191-9ef1-4cb2-a9a5-ea1a588c095e",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.7042,
  "style_score": 0.4449,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "4502f1bf-df14-4062-a4ce-f83c997699b5",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.2468,
  "model_score": 0.9792,
  "style_score": 0.6323,
  "label": "We think this was likely written by AI. If you wrote this yourself and believe this is wrong, you can appeal this decision and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "0a5b6c37-d01b-4533-9a7f-30ec3d0c1323",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.6175,
  "style_score": 0.4925,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "12ea3d79-f691-47ba-a129-4cc948663e4d",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.7387,
  "style_score": 0.5319,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "f16305e1-042b-43d6-b9a3-f27d2b2d9aca",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8051,
  "style_score": 0.51,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "901cd540-cfb6-40ec-93e6-3d81827d7e52",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8329,
  "style_score": 0.4743,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "1c98fc56-3fe0-44fa-9f38-e584a144c0b0",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8005,
  "style_score": 0.5658,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "e5741f52-616e-4f9f-a31b-5a6b6166d42e",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8814,
  "style_score": 0.4746,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "4fe0847c-7412-4e45-b0d1-7dc26a5ded80",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8816,
  "style_score": 0.54,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "087de0df-41ca-4a81-81d1-5c1d9dd0d5e1",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.3223,
  "style_score": 0.3993,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c5203ea4-2e60-4bdb-abf1-49979d5ed436",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.4625,
  "style_score": 0.3894,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "6936f291-aaca-4d60-bedc-78f9d8afb1d9",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.2044,
  "style_score": 0.4574,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "2a07e479-04bf-4652-8c5a-d32a13926608",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.5943,
  "style_score": 0.3846,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "5106da21-990c-4950-8194-0dcab88e1472",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.4998,
  "style_score": 0.4543,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "4d1ae2f0-0b61-4ed6-91cf-b1391bfa5542",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.6401,
  "style_score": 0.2377,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "f8d304ba-56d1-4c41-bec7-c9a8226af3f3",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.5583,
  "style_score": 0.4946,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "a2d5fe5c-a2be-4880-abb9-10e25686c7f8",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3334,
  "model_score": 0.0,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "dbf1beee-6dbb-41f2-acd9-13928aa06224",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0112,
  "style_score": 0.6667,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "476ff68e-8a30-4fbf-8811-1837283bebc7",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9976,
  "style_score": 0.3333,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it just means our system didn't find a clear signal either way. Nothing happens to your account because of this.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c6e273d6-4d4b-4364-ab36-9e381b783cc3",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.3307,
  "model_score": 0.9969,
  "style_score": 0.6667,
  "label": "We think this was likely written by AI. If you wrote this yourself and believe this is wrong, you can appeal this decision and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "9c7630d2-b8b6-4610-bf6d-67384e0e1c64",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.2532,
  "model_score": 0.9064,
  "style_score": 0.6667,
  "label": "We think this was likely written by AI. If you wrote this yourself and believe this is wrong, you can appeal this decision and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "7d40b6c2-5e55-4bbd-80c7-abc710e415ec",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.1281,
  "model_score": 0.2395,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "7349a539-edb6-4c38-919a-5aa1031b3e64",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.2912,
  "model_score": 0.0492,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "7f55778d-1887-4f8d-bd58-7c8d972c3398",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3088,
  "model_score": 0.0287,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "d7b5c5a2-23ff-4f12-8849-f0d6a7d2465c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3088,
  "model_score": 0.0287,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "58ba5358-7d99-4557-b4b5-9d95eba39663",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3088,
  "model_score": 0.0287,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "95236d0b-a8c9-4e55-840f-868cc55e7ce8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3088,
  "model_score": 0.0287,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "2bba2add-b119-4e12-afa7-0f461d28dd2a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3088,
  "model_score": 0.0287,
  "style_score": 0.3333,
  "label": "We think this was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
