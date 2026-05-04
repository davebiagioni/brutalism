#!/usr/bin/env python3
"""Aggregate metrics from a completed experiment run.

Reads results/runs.json (produced by run.py), parses each session's JSONL
transcript, and prints a per-arm comparison table. Writes a structured
summary.json alongside.
"""
from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "results" / "runs.json"
SUMMARY = ROOT / "results" / "summary.json"


def parse_ts(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def metrics_from_transcript(path: Path) -> dict:
    if not path.exists():
        return {}

    rows = [json.loads(line) for line in path.open() if line.strip()]

    in_tok = out_tok = cache_create = cache_read = 0
    tool_calls: Counter[str] = Counter()
    sidechain_entries = 0
    sidechain_session_ids = set()
    timestamps: list[datetime] = []

    for r in rows:
        if r.get("isSidechain"):
            sidechain_entries += 1
            if r.get("sessionId"):
                sidechain_session_ids.add(r["sessionId"])
        ts = parse_ts(r.get("timestamp"))
        if ts:
            timestamps.append(ts)

        if r.get("type") != "assistant":
            continue
        msg = r.get("message") or {}
        usage = msg.get("usage") or {}
        in_tok += usage.get("input_tokens", 0) or 0
        out_tok += usage.get("output_tokens", 0) or 0
        cache_create += usage.get("cache_creation_input_tokens", 0) or 0
        cache_read += usage.get("cache_read_input_tokens", 0) or 0

        content = msg.get("content") or []
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    tool_calls[c.get("name", "?")] += 1

    wall = None
    if timestamps:
        timestamps.sort()
        wall = (timestamps[-1] - timestamps[0]).total_seconds()

    return {
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cache_creation_input_tokens": cache_create,
        "cache_read_input_tokens": cache_read,
        "total_input_tokens": in_tok + cache_create + cache_read,
        "tool_calls_total": sum(tool_calls.values()),
        "tool_calls_by_name": dict(tool_calls),
        "task_invocations": tool_calls.get("Task", 0) + tool_calls.get("Agent", 0),
        "sidechain_entries": sidechain_entries,
        "sidechain_session_count": len(sidechain_session_ids),
        "wall_seconds_transcript": wall,
        "assistant_turns": sum(1 for r in rows if r.get("type") == "assistant"),
        "transcript_rows": len(rows),
    }


def code_metrics(workdir: Path) -> dict:
    out: dict[str, dict] = {}
    for py in workdir.rglob("*.py"):
        if "tests" in py.parts or ".venv" in py.parts:
            continue
        rel = py.relative_to(workdir)
        text = py.read_text()
        out[str(rel)] = {
            "lines": len(text.splitlines()),
            "non_blank_lines": sum(1 for line in text.splitlines() if line.strip()),
            "chars": len(text),
        }
    return out


CELL_W = 22


def fmt_num(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:,.1f}"
    if isinstance(v, int):
        return f"{v:,}"
    return str(v)


def fmt_cell(v) -> str:
    return f"{fmt_num(v):>{CELL_W}}" if not isinstance(v, str) else f"{v:>{CELL_W}}"


def agg_mean_std(values: list) -> str:
    nums = [v for v in values if isinstance(v, (int, float))]
    if not nums:
        return "-"
    if len(nums) == 1:
        return fmt_num(nums[0])
    m = statistics.mean(nums)
    sd = statistics.stdev(nums)
    return f"{fmt_num(m)} ± {fmt_num(sd)}"


def main() -> int:
    if not RUNS.exists():
        raise SystemExit(f"missing {RUNS}; run run.py first")
    runs = json.loads(RUNS.read_text())

    enriched = []
    for r in runs:
        t = r.get("transcript")
        m = metrics_from_transcript(Path(t)) if t else {}
        c = code_metrics(Path(r["workdir"]))
        enriched.append({**r, "metrics": m, "code": c})

    by_arm: dict[str, list] = defaultdict(list)
    for r in enriched:
        by_arm[r["arm"]].append(r)

    arms = list(by_arm)
    header = f"{'metric':<32} | " + " | ".join(f"{a:>{CELL_W}}" for a in arms)
    print()
    print(header)
    print("-" * len(header))

    def row(label, getter):
        cells = [f"{agg_mean_std([getter(r) for r in by_arm[a]]):>{CELL_W}}" for a in arms]
        print(f"{label:<32} | " + " | ".join(cells))

    print(f"{'runs':<32} | " + " | ".join(f"{len(by_arm[a]):>{CELL_W}}" for a in arms))
    row("tests pass rate", lambda r: 1.0 if r.get("test_returncode") == 0 else 0.0)
    row("wall_s (subprocess)", lambda r: r.get("elapsed_s"))
    row("wall_s (transcript)", lambda r: r.get("metrics", {}).get("wall_seconds_transcript"))
    row("assistant turns", lambda r: r.get("metrics", {}).get("assistant_turns"))
    row("output tokens", lambda r: r.get("metrics", {}).get("output_tokens"))
    row("input tokens (uncached)", lambda r: r.get("metrics", {}).get("input_tokens"))
    row("cache create tokens", lambda r: r.get("metrics", {}).get("cache_creation_input_tokens"))
    row("cache read tokens", lambda r: r.get("metrics", {}).get("cache_read_input_tokens"))
    row("total input tokens", lambda r: r.get("metrics", {}).get("total_input_tokens"))
    row("tool calls", lambda r: r.get("metrics", {}).get("tool_calls_total"))
    row("Task/Agent calls", lambda r: r.get("metrics", {}).get("task_invocations"))
    row("sidechain entries", lambda r: r.get("metrics", {}).get("sidechain_entries"))
    row("sidechain sessions", lambda r: r.get("metrics", {}).get("sidechain_session_count"))
    row("impl lines", lambda r: sum(c["lines"] for c in r.get("code", {}).values()) or None)
    row("impl non-blank lines", lambda r: sum(c["non_blank_lines"] for c in r.get("code", {}).values()) or None)
    row("impl chars", lambda r: sum(c["chars"] for c in r.get("code", {}).values()) or None)

    # Per-arm tool breakdown
    print()
    print("tool call breakdown (mean per run):")
    for a in arms:
        agg_tools: Counter[str] = Counter()
        n = len(by_arm[a])
        for r in by_arm[a]:
            for k, v in (r.get("metrics", {}).get("tool_calls_by_name") or {}).items():
                agg_tools[k] += v
        items = ", ".join(f"{k}={v / n:.1f}" for k, v in agg_tools.most_common())
        print(f"  {a}: {items or '(none)'}")

    summary = {
        a: [
            {
                "rep": r["rep"],
                "elapsed_s": r.get("elapsed_s"),
                "test_returncode": r.get("test_returncode"),
                "transcript": r.get("transcript"),
                "metrics": r.get("metrics"),
                "code": r.get("code"),
            }
            for r in by_arm[a]
        ]
        for a in arms
    }
    SUMMARY.write_text(json.dumps(summary, indent=2))
    print(f"\nwrote {SUMMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
