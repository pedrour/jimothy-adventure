#!/usr/bin/env python3
"""Daily Jimothy digest: pull yesterday's funnel from GA4, post it as a comment
on the 'Jimothy Daily Digest' issue so GitHub notifies the owner. A day with
purchase events gets a SALE headline. Skips cleanly when secrets are absent."""
import json
import os
import sys
import urllib.request

MONEY_EVENTS = ["purchase"]          # one per redeemed Gold Pass receipt link
FUNNEL_EVENTS = [
    ("purchase", "💰 GOLD PASS SALES"),
    ("game_start", "L1 starts"),
    ("win_screen_view", "L1 wins"),
    ("trial_granted", "gold trials granted"),
    ("level2_start", "L2 starts"),
    ("level2_win", "L2 wins"),
    ("toll_view", "🚧 Toll views"),
    ("toll_pay_click", "⚡ pay clicks"),
    ("toll_wait_click", "⏳ chose to wait"),
    ("pike_open", "gates opened (L2)"),
    ("toll_open", "🔓 gates passed (hub/L3)"),
    ("gate_dismiss", "gate dismissed"),
    ("level3_start", "L3 starts"),
    ("level3_win", "L3 wins"),
    ("finale_view", "finale views"),
    ("gold_cta_click", "gold CTA clicks"),
    ("gold_unlocked", "gold coat redeems"),
    ("share_completed", "shares completed"),
    ("daily_deeplink", "daily deep links"),
    ("hub_view", "hub views"),
]


def gh(path, data=None, method=None):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        data=json.dumps(data).encode() if data is not None else None,
        method=method or ("POST" if data is not None else "GET"),
        headers={
            "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    sa, prop = os.environ.get("GA4_SA_JSON"), os.environ.get("GA4_PROPERTY_ID")
    if not sa or not prop:
        print("GA4_SA_JSON / GA4_PROPERTY_ID not configured — skipping digest.")
        return 0

    from google.oauth2 import service_account
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest,
    )

    creds = service_account.Credentials.from_service_account_info(
        json.loads(sa), scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    client = BetaAnalyticsDataClient(credentials=creds)
    pid = f"properties/{prop}"
    ranges = [
        DateRange(start_date="yesterday", end_date="yesterday"),
        DateRange(start_date="7daysAgo", end_date="yesterday"),
    ]

    # event counts, yesterday + trailing 7 days (dateRange dimension splits the ranges)
    ev2 = client.run_report(RunReportRequest(
        property=pid, date_ranges=ranges,
        dimensions=[Dimension(name="eventName"), Dimension(name="dateRange")],
        metrics=[Metric(name="eventCount")],
        limit=400,
    ))
    counts = {}
    for row in ev2.rows:
        name = row.dimension_values[0].value
        dr = row.dimension_values[1].value  # date_range_0 / date_range_1
        c = int(row.metric_values[0].value)
        slot = 0 if dr.endswith("0") else 1
        counts.setdefault(name, [0, 0])[slot] = c

    us = client.run_report(RunReportRequest(
        property=pid, date_ranges=ranges, metrics=[Metric(name="activeUsers")],
        dimensions=[Dimension(name="dateRange")],
    ))
    users = [0, 0]
    for row in us.rows:
        slot = 0 if row.dimension_values[0].value.endswith("0") else 1
        users[slot] = int(row.metric_values[0].value)

    sales_y = sum(counts.get(e, [0, 0])[0] for e in MONEY_EVENTS)
    head = "💰 SALE ACTIVITY!" if sales_y else "🦝 quiet day at the market"
    lines = [
        f"### {head}",
        "",
        f"**Yesterday:** {users[0]} players · **7-day:** {users[1]} players",
        "",
        "| funnel | yesterday | 7-day |",
        "|---|---:|---:|",
    ]
    for key, label in FUNNEL_EVENTS:
        y, w = counts.get(key, [0, 0])
        if y or w:
            lines.append(f"| {label} | {y} | {w} |")
    lines += ["", "_automated digest · playjimothy.com_"]
    body = "\n".join(lines)

    owner_repo = os.environ["GITHUB_REPOSITORY"]
    issues = gh(f"/repos/{owner_repo}/issues?state=open&per_page=50")
    issue = next((i for i in issues if i["title"] == "📊 Jimothy Daily Digest"), None)
    if issue is None:
        issue = gh(f"/repos/{owner_repo}/issues", {
            "title": "📊 Jimothy Daily Digest",
            "body": "Daily funnel + sales digest lands here as comments. "
                    "Subscribe to this issue for phone pings on 💰 days.",
        })
    gh(f"/repos/{owner_repo}/issues/{issue['number']}/comments", {"body": body})
    print(f"Posted digest to issue #{issue['number']} — {head}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
