#!/usr/bin/env python3
"""
Capstone Milestone 5 -- run the five criteria in criteria.md's Capstone
section, three trials, nothing in between.

No scenario file this unit -- nobody wrote one. Each criterion needs a
different shape of request, worked out here directly rather than through
scenarios.py/run_eval.py (those assume one request shape per scenario;
this unit's criteria mix normal submissions, deliberately malformed ones,
and non-/submit routes in the same criterion).

    python app.py                     # in one terminal
    python capstone_eval.py --trial 1
    python capstone_eval.py --trial 2
    python capstone_eval.py --trial 3
"""

import argparse
import json
import statistics
import time
from pathlib import Path

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"

ORDINARY_TEXTS = [
    "The quarterly report shows a modest increase in regional sales, driven mostly by the new product line launched in March.",
    "I honestly cannot believe how fast this month went by, between work deadlines and trying to fix my sink.",
    "Photosynthesis converts light energy into chemical energy stored in glucose, using carbon dioxide and water as inputs.",
    "My dog refuses to walk past the neighbor's cat without stopping dead in his tracks for a solid two minutes.",
    "The committee reviewed three proposals and recommended moving forward with the second option pending budget approval.",
    "Woke up groggy, drank too much coffee, and now I am wired but also somehow still tired. Great combo.",
    "The algorithm processes each node in the graph exactly once, achieving linear time complexity in the number of edges.",
    "Spent the whole afternoon reorganizing my bookshelf by color instead of doing literally anything on my to-do list.",
    "Market volatility increased sharply following the announcement, with several sectors posting their largest single-day losses this year.",
    "Tried baking bread for the first time and somehow ended up with something closer to a brick. Still proud of it though.",
    "The river flooded its banks after three days of continuous rain, forcing several nearby roads to close overnight.",
    "I keep forgetting my umbrella and somehow it only ever rains on the days I do that. Statistically suspicious.",
    "The study followed two hundred participants over five years, measuring changes in sleep quality and reported stress.",
    "Finally beat that level in the game I've been stuck on for a week. Felt disproportionately good, not going to lie.",
    "The new policy requires all vendors to submit updated compliance documentation before the end of the fiscal quarter.",
]

WARMUP_TEXT = "Warming up the model before timing anything that actually counts for this trial."
IDENTICAL_TEXT = (
    "This exact sentence is sent ten times in a row, unchanged, so any difference "
    "in how long signal one takes to score it is timing variance, not a different input."
)


def post(payload, timeout=60):
    return requests.post(f"{URL}/submit", json=payload, timeout=timeout)


def fetch_log(limit=300):
    return requests.get(f"{URL}/log", params={"limit": limit}, timeout=30).json()["entries"]


def criterion_1(trial):
    """20 calls (15 ordinary + 5 malformed-enough-to-crash-signal-one),
    every one must leave a complete log entry."""
    tag = f"cap_c1_t{trial}"
    sent_ids = []
    for i, text in enumerate(ORDINARY_TEXTS, 1):
        cid = f"{tag}_ok{i}"
        post({"text": text, "creator_id": cid})
        sent_ids.append(cid)
    for i in range(1, 6):
        cid = f"{tag}_bad{i}"
        post({"text": "a", "creator_id": cid})  # below the 3-token minimum -> signal_one_error
        sent_ids.append(cid)

    entries = fetch_log(limit=200)
    by_creator = {e.get("creator_id"): e for e in entries if e.get("creator_id") in sent_ids}

    complete = 0
    detail = []
    for cid in sent_ids:
        e = by_creator.get(cid)
        ok = False
        if e is not None and "input_length" in e and "status" in e:
            if e["status"] == "decided":
                ok = "total_duration_ms" in e and "signal_one_duration_ms" in e
            elif e["status"] == "rejected":
                ok = "total_duration_ms" in e and "reason" in e
        if ok:
            complete += 1
        detail.append({"creator_id": cid, "found": e is not None, "complete": ok})

    return {"met": complete, "total": len(sent_ids), "detail": detail}


def criterion_2_and_3(trial):
    """10 identical-input warm requests. C2: signal_one_duration_ms stays
    within +/-20% of the mean in >=9/10. C3: total-signal_one overhead
    stays <=5ms in >=9/10."""
    post({"text": WARMUP_TEXT, "creator_id": f"cap_c23_t{trial}_warmup"})  # not counted

    tag = f"cap_c23_t{trial}"
    sent_ids = []
    for i in range(1, 11):
        cid = f"{tag}_{i}"
        post({"text": IDENTICAL_TEXT, "creator_id": cid})
        sent_ids.append(cid)

    entries = fetch_log(limit=200)
    by_creator = {e.get("creator_id"): e for e in entries if e.get("creator_id") in sent_ids}
    rows = [by_creator[cid] for cid in sent_ids if cid in by_creator]

    sig_ones = [r["signal_one_duration_ms"] for r in rows]
    totals = [r["total_duration_ms"] for r in rows]
    mean_sig_one = statistics.mean(sig_ones)
    within_20pct = sum(1 for v in sig_ones if abs(v - mean_sig_one) <= 0.20 * mean_sig_one)

    overheads = [round(t - s, 3) for t, s in zip(totals, sig_ones)]
    overhead_ok = sum(1 for o in overheads if o <= 5.0)

    return {
        "c2_met": within_20pct, "c2_total": len(rows), "mean_signal_one_ms": round(mean_sig_one, 2),
        "signal_one_ms": sig_ones,
        "c3_met": overhead_ok, "c3_total": len(rows), "overheads_ms": overheads,
    }


def criterion_4(trial):
    """5 requests engineered to crash signal one. Each must come back as a
    clean handled error (never an unhandled 500 HTML page) AND log with
    reason signal_one_error."""
    tag = f"cap_c4_t{trial}"
    results = []
    for i in range(1, 6):
        cid = f"{tag}_{i}"
        r = post({"text": "a", "creator_id": cid})
        is_clean_json_500 = False
        try:
            body = r.json()
            is_clean_json_500 = r.status_code == 500 and body.get("error") == "internal_error"
        except ValueError:
            is_clean_json_500 = False  # an unhandled crash returns Flask's HTML page, not JSON
        results.append({"creator_id": cid, "status": r.status_code, "clean_json_500": is_clean_json_500})

    entries = fetch_log(limit=200)
    by_creator = {e.get("creator_id"): e for e in entries if e.get("creator_id") in [x["creator_id"] for x in results]}

    met = 0
    for row in results:
        e = by_creator.get(row["creator_id"])
        logged = e is not None and e.get("reason") == "signal_one_error"
        row["logged"] = logged
        if row["clean_json_500"] and logged:
            met += 1

    return {"met": met, "total": len(results), "detail": results}


def criterion_5(trial):
    """/ping, /health, and a full submit->appeal round trip, 5 times each,
    must keep returning their documented shape/status after this unit's
    changes."""
    ping_ok = 0
    health_ok = 0
    appeal_ok = 0
    detail = []

    for i in range(1, 6):
        r = requests.post(f"{URL}/ping", json={"message": f"regression {trial}-{i}"}, timeout=30)
        ok = r.status_code == 200 and r.json().get("ok") is True
        ping_ok += ok
        detail.append({"route": "ping", "i": i, "status": r.status_code, "ok": ok})

    for i in range(1, 6):
        r = requests.get(f"{URL}/health", timeout=30)
        body = r.json()
        ok = r.status_code == 200 and body.get("ok") is True and "detector_loaded" in body
        health_ok += ok
        detail.append({"route": "health", "i": i, "status": r.status_code, "ok": ok})

    for i in range(1, 6):
        sub = post({"text": f"Regression round trip {trial}-{i}, a short piece of real writing.",
                    "creator_id": f"cap_c5_t{trial}_{i}"})
        sub_body = sub.json()
        content_id = sub_body.get("content_id")
        app_r = requests.post(f"{URL}/appeal", json={"content_id": content_id, "reasoning": "regression check"}, timeout=30)
        app_body = app_r.json() if app_r.content else {}
        ok = (sub.status_code == 200 and content_id and app_r.status_code == 200
              and app_body.get("status") == "under_review")
        appeal_ok += ok
        detail.append({"route": "submit+appeal", "i": i, "submit_status": sub.status_code,
                        "appeal_status": app_r.status_code, "ok": ok})

    return {"ping_met": ping_ok, "health_met": health_ok, "appeal_met": appeal_ok, "total": 5, "detail": detail}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", type=int, required=True)
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    try:
        requests.get(f"{URL}/health", timeout=5)
    except Exception:
        print(f"Nothing answering at {URL}. Start it: python app.py")
        raise SystemExit(1)

    print(f"=== Trial {args.trial} ===")
    result = {
        "trial": args.trial,
        "criterion_1": criterion_1(args.trial),
        "criterion_2_3": criterion_2_and_3(args.trial),
        "criterion_4": criterion_4(args.trial),
        "criterion_5": criterion_5(args.trial),
    }

    c1, c23, c4, c5 = result["criterion_1"], result["criterion_2_3"], result["criterion_4"], result["criterion_5"]
    print(f"C1 complete records: {c1['met']}/{c1['total']}")
    print(f"C2 within 20% of mean ({c23['mean_signal_one_ms']}ms): {c23['c2_met']}/{c23['c2_total']}")
    print(f"C3 overhead <=5ms: {c23['c3_met']}/{c23['c3_total']}")
    print(f"C4 crash caught+logged: {c4['met']}/{c4['total']}")
    print(f"C5 ping/health/appeal: {c5['ping_met']}/5, {c5['health_met']}/5, {c5['appeal_met']}/5")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    suffix = f"_{args.label}" if args.label else ""
    out_path = config.RESULTS_DIR / f"capstone_trial_{args.trial}{suffix}.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
