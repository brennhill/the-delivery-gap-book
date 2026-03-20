#!/usr/bin/env python3
"""
Cost per accepted change calculator.

No commercial tool computes this metric today. This script does.
Feed it your numbers and it produces the cost breakdown from the
Verification Triangle chapter, with an optional branded HTML report.

Usage:
    python cost-calculator.py
    python cost-calculator.py --interactive
    python cost-calculator.py --json costs.json
    python cost-calculator.py --json costs.json --html report.html

The --json option reads from a file:
    {
        "model_cost": 4200,
        "infra_cost": 1800,
        "prompting_hours": 30,
        "review_hours": 40,
        "rework_hours": 20,
        "burdened_rate": 120,
        "merged_prs": 88,
        "reverted_prs": 12
    }

The --html option generates a branded Delivery Gap report with
an SVG pie chart suitable for CI/CD artifacts or team dashboards.
"""

import argparse
import json
import math
import re
import subprocess
import sys
from datetime import datetime


def calculate(data: dict) -> dict:
    prompting_cost = data["prompting_hours"] * data["burdened_rate"]
    review_cost = data["review_hours"] * data["burdened_rate"]
    rework_cost = data["rework_hours"] * data["burdened_rate"]

    total_cost = (
        data["model_cost"]
        + data["infra_cost"]
        + prompting_cost
        + review_cost
        + rework_cost
    )

    accepted = data["merged_prs"] - data["reverted_prs"]
    if accepted <= 0:
        print("Error: accepted changes must be > 0", file=sys.stderr)
        sys.exit(1)

    cost_per_change = total_cost / accepted

    return {
        "model_cost": data["model_cost"],
        "infra_cost": data["infra_cost"],
        "prompting_cost": prompting_cost,
        "review_cost": review_cost,
        "rework_cost": rework_cost,
        "total_cost": total_cost,
        "merged_prs": data["merged_prs"],
        "reverted_prs": data["reverted_prs"],
        "accepted_changes": accepted,
        "cost_per_accepted_change": round(cost_per_change, 2),
        "breakdown": {
            "model_pct": round(data["model_cost"] / total_cost * 100, 1),
            "infra_pct": round(data["infra_cost"] / total_cost * 100, 1),
            "prompting_pct": round(prompting_cost / total_cost * 100, 1),
            "review_pct": round(review_cost / total_cost * 100, 1),
            "rework_pct": round(rework_cost / total_cost * 100, 1),
        },
    }


def interactive() -> dict:
    print("Cost per Accepted Change Calculator")
    print("=" * 44)
    print()

    def ask(prompt, default=0):
        val = input(f"  {prompt} [{default}]: ").strip()
        return float(val) if val else default

    data = {
        "model_cost": ask("AI model/API spend this period ($)", 4200),
        "infra_cost": ask("Infrastructure cost ($)", 1800),
        "prompting_hours": ask("Human engineering hours (discussion, specs, prompting)", 30),
        "review_hours": ask("Hours spent reviewing AI output", 40),
        "rework_hours": ask("Hours spent on rework/fixes", 20),
        "burdened_rate": ask("Fully burdened hourly rate ($)", 120),
        "merged_prs": ask("Merged PRs this period", 88),
        "reverted_prs": ask("Reverted/hotfixed PRs within 14 days", 12),
    }
    return data


def print_results(r: dict):
    print()
    print("=" * 50)
    print(" COST PER ACCEPTED CHANGE BREAKDOWN")
    print("=" * 50)
    print()
    print(f"  Model/API cost:      ${r['model_cost']:>10,.0f}  ({r['breakdown']['model_pct']}%)")
    print(f"  Infrastructure:      ${r['infra_cost']:>10,.0f}  ({r['breakdown']['infra_pct']}%)")
    print(f"  Human engineering:   ${r['prompting_cost']:>10,.0f}  ({r['breakdown']['prompting_pct']}%)")
    print(f"  Human review:        ${r['review_cost']:>10,.0f}  ({r['breakdown']['review_pct']}%)")
    print(f"  Rework:              ${r['rework_cost']:>10,.0f}  ({r['breakdown']['rework_pct']}%)")
    print(f"  {'─' * 40}")
    print(f"  Total cost:          ${r['total_cost']:>10,.0f}")
    print()
    print(f"  Merged PRs:          {r['merged_prs']:>10}")
    print(f"  Reverted/fixed:      {r['reverted_prs']:>10}")
    print(f"  Accepted changes:    {r['accepted_changes']:>10}")
    print()
    print(f"  ┌─────────────────────────────────────────┐")
    print(f"  │  Cost per accepted change: ${r['cost_per_accepted_change']:>10,.2f}  │")
    print(f"  └─────────────────────────────────────────┘")
    print()

    visible = r["breakdown"]["model_pct"] + r["breakdown"]["infra_pct"]
    hidden = r["breakdown"]["prompting_pct"] + r["breakdown"]["review_pct"] + r["breakdown"]["rework_pct"]
    print(f"  Visible cost (model + infra): {visible:.0f}%")
    print(f"  Hidden cost (people):         {hidden:.0f}%")
    print()


# ── SVG pie chart generation ─────────────────────────────────────────

def polar_to_cart(cx, cy, r, angle_deg):
    """Convert polar angle (0=top, clockwise) to SVG cartesian."""
    angle_rad = math.radians(angle_deg - 90)
    return cx + r * math.cos(angle_rad), cy + r * math.sin(angle_rad)


def pie_slice(cx, cy, r, start_deg, end_deg, color, opacity=1.0):
    """Generate an SVG path for a pie slice."""
    if end_deg - start_deg >= 360:
        end_deg = start_deg + 359.99
    x1, y1 = polar_to_cart(cx, cy, r, start_deg)
    x2, y2 = polar_to_cart(cx, cy, r, end_deg)
    large = 1 if (end_deg - start_deg) > 180 else 0
    op = f' fill-opacity="{opacity}"' if opacity < 1 else ""
    return f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large},1 {x2:.1f},{y2:.1f} Z" fill="{color}"{op}/>'


def label_pos(cx, cy, r, start_deg, end_deg):
    """Position for a label at the midpoint of a slice."""
    mid = (start_deg + end_deg) / 2
    lr = r * 0.65
    return polar_to_cart(cx, cy, lr, mid)


def generate_svg(r: dict) -> str:
    """Generate a branded SVG pie chart from calculation results."""
    cx, cy, radius = 150, 150, 130
    font = "'Avenir Next', 'Helvetica Neue', Arial, sans-serif"
    serif = "Georgia, 'Iowan Old Style', serif"

    slices = [
        ("Model cost", r["model_cost"], r["breakdown"]["model_pct"], "#2BA99A", 1.0),
        ("Infrastructure", r["infra_cost"], r["breakdown"]["infra_pct"], "#2BA99A", 0.5),
        ("Human engineering", r["prompting_cost"], r["breakdown"]["prompting_pct"], "#B06835", 1.0),
        ("Human review", r["review_cost"], r["breakdown"]["review_pct"], "#C9962A", 1.0),
        ("Rework", r["rework_cost"], r["breakdown"]["rework_pct"], "#1D3557", 1.0),
    ]

    paths = []
    labels = []
    angle = 0

    for i, (name, cost, pct, color, opacity) in enumerate(slices):
        sweep = pct / 100 * 360
        if sweep < 1:
            angle += sweep
            continue
        paths.append(pie_slice(cx, cy, radius, angle, angle + sweep, color, opacity))

        lx, ly = label_pos(cx, cy, radius, angle, angle + sweep)
        if pct >= 8:
            labels.append(
                f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="middle" dominant-baseline="middle" '
                f'font-family="{font}" font-size="13" fill="white" font-weight="600">{pct:.0f}%</text>'
            )

        angle += sweep

    svg = f'''<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" width="300" height="300">
  <rect width="480" height="400" fill="#fcfaf6" rx="8"/>

  <!-- Pie slices -->
  {"".join(paths)}

  <!-- Percentage labels -->
  {"".join(labels)}
</svg>'''
    return svg


def _render_warnings(warnings: list, repo_url: str = "") -> str:
    if not warnings:
        return ""
    cards = []
    for w in warnings:
        items_html = ""
        # Structured items (rework details)
        if w.get("structured_items"):
            item_blocks = []
            for item in w["structured_items"]:
                sha = item["sha"]
                sha_link = f'<a href="{repo_url}/commit/{sha}" class="commit-sha">{sha}</a>' if repo_url else f'<span class="commit-sha">{sha}</span>'
                signals_html = "".join(
                    f'<div class="signal">{format_signal_html(s, repo_url)}</div>'
                    for s in item.get("signals", [])
                )
                item_blocks.append(
                    f'<div class="warning-item">'
                    f'<div class="commit-header">{sha_link} <span class="commit-subject">— {item["subject"][:60]}</span></div>'
                    f'{signals_html}'
                    f'</div>'
                )
            items_html = f'<div class="warning-items">{"".join(item_blocks)}</div>'
        # Simple items (oversized PRs)
        elif w.get("items"):
            item_blocks = []
            for item_text in w["items"]:
                item_blocks.append(f'<div class="warning-item"><div class="commit-header">{item_text}</div></div>')
            items_html = f'<div class="warning-items">{"".join(item_blocks)}</div>'

        cards.append(
            f'<div class="warning-card {w["level"]}">'
            f'<div class="warning-title">{w["title"]}</div>'
            f'<div class="warning-detail">{w["detail"]}</div>'
            f'{items_html}'
            f'</div>'
        )
    return f'<div class="warnings">{"".join(cards)}</div>'


def generate_html(r: dict, team_name: str = "", warnings: list | None = None, repo_url: str = "") -> str:
    """Generate a branded HTML report with SVG pie chart."""
    svg = generate_svg(r)
    warnings = warnings or []
    date = datetime.now().strftime("%B %d, %Y")
    team_line = f" — {team_name}" if team_name else ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Cost per Accepted Change{team_line}</title>
<style>
  :root {{
    --cream: #FCFAF6;
    --navy: #1D3557;
    --copper: #B06835;
    --gold: #C9962A;
    --copy: #2F353C;
    --muted: #6D7178;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Avenir Next', 'Helvetica Neue', Arial, sans-serif;
    background: var(--cream);
    color: var(--copy);
    padding: 40px 20px;
    max-width: 860px;
    margin: 0 auto;
  }}
  .header {{
    border-bottom: 3px solid var(--gold);
    padding-bottom: 20px;
    margin-bottom: 32px;
  }}
  .header h1 {{
    font-family: Georgia, 'Iowan Old Style', serif;
    font-size: 28px;
    color: var(--navy);
    font-weight: bold;
  }}
  .header .subtitle {{
    font-size: 14px;
    color: var(--copper);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 4px;
  }}
  .header .date {{
    font-size: 13px;
    color: var(--muted);
    margin-top: 8px;
  }}
  .metrics {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }}
  .metric-card {{
    background: white;
    border: 1px solid #e8e2d8;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
  }}
  .metric-card .value {{
    font-family: Georgia, 'Iowan Old Style', serif;
    font-size: 28px;
    font-weight: bold;
    color: var(--navy);
  }}
  .metric-card .label {{
    font-size: 12px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 6px;
  }}
  .metric-card.highlight .value {{
    color: var(--gold);
    font-size: 32px;
  }}
  .chart-row {{
    display: flex;
    gap: 32px;
    align-items: flex-start;
    margin-bottom: 32px;
  }}
  .chart-row .pie {{
    flex: 0 0 auto;
  }}
  .chart-row .pie svg {{
    display: block;
  }}
  .chart-row .breakdown {{
    flex: 1;
    min-width: 0;
  }}
  .breakdown-table {{
    width: 100%;
    border-collapse: collapse;
  }}
  .breakdown-table th {{
    text-align: left;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--copper);
    padding: 8px 12px;
    border-bottom: 2px solid var(--navy);
  }}
  .breakdown-table td {{
    padding: 10px 12px;
    border-bottom: 1px solid #e8e2d8;
    font-size: 14px;
  }}
  .breakdown-table td:nth-child(2),
  .breakdown-table td:nth-child(3) {{
    text-align: right;
    font-family: 'SF Mono', 'Menlo', monospace;
  }}
  .breakdown-table tr:last-child td {{
    border-bottom: 2px solid var(--navy);
    font-weight: 600;
  }}
  .color-dot {{
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 2px;
    margin-right: 8px;
  }}
  .footer {{
    border-top: 1px solid #e8e2d8;
    padding-top: 16px;
    font-size: 11px;
    color: var(--muted);
    text-align: center;
  }}
  .footer a {{
    color: var(--copper);
    text-decoration: none;
  }}
  .warnings {{
    margin-bottom: 32px;
  }}
  .warning-card {{
    border-left: 4px solid var(--gold);
    background: white;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin-bottom: 12px;
  }}
  .warning-card.high {{
    border-left-color: #C0392B;
  }}
  .warning-card .warning-title {{
    font-weight: 600;
    color: var(--navy);
    font-size: 14px;
    margin-bottom: 4px;
  }}
  .warning-card .warning-detail {{
    font-size: 13px;
    color: var(--muted);
  }}
  .warning-card .warning-items {{
    margin-top: 12px;
  }}
  .warning-item {{
    background: var(--cream);
    border: 1px solid #e8e2d8;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 8px;
  }}
  .warning-item .commit-header {{
    font-size: 13px;
    color: var(--navy);
    margin-bottom: 6px;
  }}
  .warning-item .commit-sha {{
    font-family: 'SF Mono', 'Menlo', monospace;
    font-weight: 700;
    font-size: 12px;
  }}
  .warning-item .commit-subject {{
    font-weight: 500;
  }}
  .warning-item .signal {{
    font-size: 12px;
    color: var(--muted);
    padding-left: 16px;
    line-height: 1.7;
  }}
  .warning-item .signal .fix-sha {{
    font-family: 'SF Mono', 'Menlo', monospace;
    font-weight: 600;
    color: var(--copper);
  }}
  .warning-item .signal .file-list {{
    color: var(--copy);
    font-family: 'SF Mono', 'Menlo', monospace;
    font-size: 11px;
  }}
  @media print {{
    body {{ padding: 20px; }}
    .metric-card {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>

<div class="header">
  <h1>Cost per Accepted Change</h1>
  <div class="subtitle">The Delivery Gap</div>
  <div class="date">{date}{team_line}</div>
</div>

<div class="metrics">
  <div class="metric-card highlight">
    <div class="value">${r["cost_per_accepted_change"]:,.2f}</div>
    <div class="label">Cost per accepted change</div>
  </div>
  <div class="metric-card">
    <div class="value">{r["accepted_changes"]}</div>
    <div class="label">Accepted changes</div>
  </div>
  <div class="metric-card">
    <div class="value">{r["merged_prs"]}</div>
    <div class="label">Merged PRs</div>
  </div>
  <div class="metric-card">
    <div class="value">{r["reverted_prs"]}</div>
    <div class="label">Reverted / hotfixed</div>
  </div>
</div>

<div class="chart-row">
  <div class="pie">
    {svg}
  </div>
  <div class="breakdown">
    <table class="breakdown-table">
      <thead>
        <tr>
          <th>Category</th>
          <th>Cost</th>
          <th>Share</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="color-dot" style="background: #2BA99A"></span>Model / API</td>
          <td>${r["model_cost"]:,.0f}</td>
          <td>{r["breakdown"]["model_pct"]}%</td>
        </tr>
        <tr>
          <td><span class="color-dot" style="background: #2BA99A; opacity: 0.5"></span>Infrastructure</td>
          <td>${r["infra_cost"]:,.0f}</td>
          <td>{r["breakdown"]["infra_pct"]}%</td>
        </tr>
        <tr>
          <td><span class="color-dot" style="background: #B06835"></span>Human engineering</td>
          <td>${r["prompting_cost"]:,.0f}</td>
          <td>{r["breakdown"]["prompting_pct"]}%</td>
        </tr>
        <tr>
          <td><span class="color-dot" style="background: #C9962A"></span>Human review</td>
          <td>${r["review_cost"]:,.0f}</td>
          <td>{r["breakdown"]["review_pct"]}%</td>
        </tr>
        <tr>
          <td><span class="color-dot" style="background: #1D3557"></span>Rework</td>
          <td>${r["rework_cost"]:,.0f}</td>
          <td>{r["breakdown"]["rework_pct"]}%</td>
        </tr>
        <tr>
          <td>Total</td>
          <td>${r["total_cost"]:,.0f}</td>
          <td>100%</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

{_render_warnings(warnings, repo_url)}

<div class="footer">
  Generated by <a href="https://github.com/brennhill/the-delivery-gap-book">The Delivery Gap Execution Kit</a>
  &middot; Methodology from <em>The Delivery Gap: Speed and Certainty in the Age of AI</em> by Brenn Hill
</div>

</body>
</html>'''


def detect_repo_info() -> tuple[str, str]:
    """Try to detect repo name and GitHub URL from git remote.
    Returns (name, url) e.g. ("owner/repo", "https://github.com/owner/repo")."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            raw = result.stdout.strip()
            for pattern in [r"[:/]([^/]+/[^/]+?)(?:\.git)?$", r"([^/]+/[^/]+?)(?:\.git)?$"]:
                m = re.search(pattern, raw)
                if m:
                    name = m.group(1)
                    url = f"https://github.com/{name}"
                    return name, url
    except FileNotFoundError:
        pass
    return "", ""


def load_rework_data(rework_json_path: str, data: dict) -> tuple[dict, list]:
    """Override merged_prs and reverted_prs from rework-detector.py output.
    Returns (data, rework_items) where rework_items has per-PR detail."""
    with open(rework_json_path) as f:
        rework_results = json.load(f)

    accepted = sum(1 for r in rework_results if r["status"] == "accepted")
    rework = sum(1 for r in rework_results if r["status"] == "rework")
    total = accepted + rework  # exclude pending

    data["merged_prs"] = total
    data["reverted_prs"] = rework
    return data, rework_results


def generate_warnings(r: dict, rework_items: list | None = None) -> list[dict]:
    """Generate warning cards based on thresholds from research."""
    warnings = []

    # Rework rate warning
    total = r["merged_prs"]
    if total > 0:
        rework_rate = r["reverted_prs"] / total * 100
        if rework_rate > 15:
            warnings.append({
                "level": "high",
                "title": f"Rework rate: {rework_rate:.0f}%",
                "detail": "Above 15% baseline. Check spec quality and gate coverage.",
            })

    # Large PR warnings from rework data
    if rework_items:
        large_prs = [
            item for item in rework_items
            if item.get("files_changed", 0) > 20  # rough proxy if no line count
        ]
        oversized = [
            item for item in rework_items
            if item.get("lines_changed", item.get("files_changed", 0) * 30) > 400
        ]
        reworked = [item for item in rework_items if item["status"] == "rework"]

        if oversized:
            warnings.append({
                "level": "medium",
                "title": f"{len(oversized)} PRs likely over 400 lines",
                "detail": "Review effectiveness drops sharply above 400 lines (SmartBear/Cisco). Consider enforcing a PR size limit in CI.",
                "structured_items": oversized[:10],
            })

        if reworked:
            warnings.append({
                "level": "high",
                "title": f"{len(reworked)} changes required rework",
                "detail": "These changes were reverted or patched within 14 days.",
                "structured_items": reworked[:10],
            })

    return warnings


def format_signal_html(signal: str, repo_url: str = "") -> str:
    """Format a rework signal with linked SHAs and file lists."""
    # Extract fix SHA and file list from signal text
    import re as _re
    m = _re.match(r"(Reverted by|Fixes: trailer in|Same ticket .+ fixed by|Fix) (\w{10})(.*)", signal)
    if m:
        prefix = m.group(1)
        fix_sha = m.group(2)
        rest = m.group(3)
        sha_html = f'<a href="{repo_url}/commit/{fix_sha}" class="fix-sha">{fix_sha}</a>' if repo_url else f'<span class="fix-sha">{fix_sha}</span>'

        # Extract file list if present
        files_match = _re.search(r"touches same source files: (.+)$", rest)
        if files_match:
            files = files_match.group(1)
            return f'{prefix} {sha_html}<br><span class="file-list">{files}</span>'
        return f'{prefix} {sha_html}{rest}'
    return signal


def main():
    parser = argparse.ArgumentParser(description="Cost per accepted change calculator")
    parser.add_argument("--json", help="Read inputs from JSON file")
    parser.add_argument("--interactive", action="store_true", help="Interactive prompt mode")
    parser.add_argument("--output", help="Write results to JSON file")
    parser.add_argument("--html", help="Generate branded HTML report")
    parser.add_argument("--team", default=None, help="Team or repo name for report header (default: auto-detect from git remote)")
    parser.add_argument("--from-rework", help="Read merged/reverted counts from rework-detector.py JSON output (overrides merged_prs and reverted_prs in input)")
    parser.add_argument("--repo-url", default=None, help="GitHub repo URL for commit links (default: auto-detect from git remote)")
    args = parser.parse_args()

    if args.json:
        with open(args.json) as f:
            data = json.load(f)
    elif args.interactive or sys.stdin.isatty():
        data = interactive()
    else:
        data = json.load(sys.stdin)

    rework_items = None
    if args.from_rework:
        data, rework_items = load_rework_data(args.from_rework, data)
        print(f"  Loaded rework data: {data['merged_prs']} classifiable, {data['reverted_prs']} reworked")

    results = calculate(data)
    print_results(results)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"  Results written to {args.output}")

    if args.html:
        detected_name, detected_url = detect_repo_info()
        team = args.team if args.team is not None else detected_name
        repo_url = args.repo_url if args.repo_url is not None else detected_url
        warnings = generate_warnings(results, rework_items)
        html = generate_html(results, team, warnings, repo_url)
        with open(args.html, "w") as f:
            f.write(html)
        print(f"  HTML report written to {args.html}")


if __name__ == "__main__":
    main()
