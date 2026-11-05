#!/usr/bin/env python3
"""
Criterion 4 — the appeal path always changes status and always logs.

Not expressible in scenarios.py: an appeal needs a real content_id from a
prior /submit response, which the texts/bodies model there can't produce.
This does one submit -> appeal round trip, 5 times per trial, 3 trials.

    python run_appeal_eval.py --label before
"""

import argparse
import json

import config
import requests

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    all_trials = []
    for trial in range(1, args.trials + 1):
        results = []
        for i in range(1, args.rounds + 1):
            submit_body = {
                "text": f"Appeal eval round {trial}-{i}. This is a short piece of "
                        f"writing submitted purely to generate a real content_id "
                        f"so the appeal path can be exercised against it.",
                "creator_id": f"eval_appeal_{trial}_{i}",
            }
            submit_resp = requests.post(f"{args.url}/submit", json=submit_body, timeout=90)
            submit_payload = submit_resp.json()
            content_id = submit_payload["content_id"]

            appeal_body = {
                "content_id": content_id,
                "reasoning": "I wrote this myself and am appealing the label.",
            }
            appeal_resp = requests.post(f"{args.url}/appeal", json=appeal_body, timeout=30)
            appeal_payload = appeal_resp.json() if appeal_resp.content else {}

            results.append({
                "content_id": content_id,
                "submit_status": submit_resp.status_code,
                "submit_label": submit_payload.get("label"),
                "appeal_status": appeal_resp.status_code,
                "appeal_response_status_field": appeal_payload.get("status"),
                "changed_to_under_review": appeal_payload.get("status") == "under_review",
            })

        changed = sum(1 for r in results if r["changed_to_under_review"])
        print(f"trial {trial}: {changed}/{args.rounds} appeals moved to under_review")
        all_trials.append(results)

    config.RESULTS_DIR.mkdir(exist_ok=True)
    import datetime as dt
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_run_{stamp}{label}.md"

    lines = [f"# Appeal eval{f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `run_appeal_eval.py::main`",
             "- Service: `app.py::appeal` · `audit.py::log_appeal`", ""]
    for trial_number, results in enumerate(all_trials, 1):
        lines += [f"**Trial {trial_number}**", "", "```json",
                  json.dumps(results, indent=2), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
