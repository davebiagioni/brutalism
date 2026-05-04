#!/usr/bin/env python3
"""Run the parallelism experiment.

Same shape as correctness-comparison/run.py, but the task asks for four
independent modules so the agent has an opportunity to dispatch parallel
subagents. The harness copies all visible test files into the workdir up
front and all held-out test files in only after the agent finishes.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS = {
    "brutalism": ROOT / "prompts" / "brutalism.md",
    "superpowers": ROOT / "prompts" / "superpowers.md",
}
VISIBLE_TESTS_DIR = ROOT / "tests" / "visible"
HOLDOUT_TESTS_DIR = ROOT / "tests" / "holdout"
TASK = ROOT / "task.md"
RESULTS = ROOT / "results"
TRANSCRIPT_BASE = Path.home() / ".claude" / "projects"

PYTEST_RESULT_RE = re.compile(
    r"^(?P<file>tests/[^:\s]+)::(?P<name>[\w\[\]\-]+)\s+(?P<status>PASSED|FAILED|ERROR|SKIPPED)"
)


def sanitize_cwd(p: Path) -> str:
    return str(p).replace("/", "-")


def setup_workdir(arm: str, rep: int) -> Path:
    workdir = RESULTS / f"{arm}-{rep:02d}"
    if workdir.exists():
        shutil.rmtree(workdir)
    (workdir / "tests").mkdir(parents=True)
    for f in VISIBLE_TESTS_DIR.glob("*.py"):
        shutil.copy(f, workdir / "tests" / f.name)
    shutil.copy(TASK, workdir / "task.md")
    return workdir


def grade(workdir: Path) -> dict:
    for f in HOLDOUT_TESTS_DIR.glob("*.py"):
        shutil.copy(f, workdir / "tests" / f.name)

    proc = subprocess.run(
        [
            "uv", "run", "--quiet", "--with", "pytest",
            "python", "-m", "pytest", "tests/", "-v", "--tb=no", "--no-header",
        ],
        cwd=workdir, capture_output=True, text=True, timeout=120,
    )
    out = proc.stdout + proc.stderr
    per_test: dict[str, dict[str, str]] = {"visible": {}, "holdout": {}}
    for line in out.splitlines():
        m = PYTEST_RESULT_RE.match(line)
        if not m:
            continue
        bucket = "holdout" if "holdout" in m.group("file") else "visible"
        per_test[bucket][f"{m.group('file')}::{m.group('name')}"] = m.group("status")

    def summarize(d):
        passed = sum(1 for s in d.values() if s == "PASSED")
        return {
            "total": len(d),
            "passed": passed,
            "failed": [n for n, s in d.items() if s != "PASSED"],
        }

    return {
        "visible": summarize(per_test["visible"]),
        "holdout": summarize(per_test["holdout"]),
        "pytest_returncode": proc.returncode,
        "pytest_output_tail": out[-1500:],
    }


def run_arm(arm: str, rep: int, model: str | None, timeout_s: int) -> dict:
    workdir = setup_workdir(arm, rep)
    prompt = PROMPTS[arm].read_text()
    session_id = str(uuid.uuid4())

    cmd = [
        "claude", "-p",
        "--session-id", session_id,
        "--output-format", "json",
        "--permission-mode", "bypassPermissions",
    ]
    if model:
        cmd += ["--model", model]
    cmd.append(prompt)

    print(f"  cwd: {workdir}")
    print(f"  session_id: {session_id}")
    sys.stdout.flush()

    start = time.time()
    timed_out = False
    try:
        proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout_s)
        stdout, stderr, rc = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        timed_out = True
        rc = None
        stdout = e.stdout if isinstance(e.stdout, str) else (e.stdout or b"").decode("utf-8", "replace") if e.stdout else ""
        stderr = e.stderr if isinstance(e.stderr, str) else (e.stderr or b"").decode("utf-8", "replace") if e.stderr else ""
    elapsed = time.time() - start

    sanitized = sanitize_cwd(workdir)
    transcript = TRANSCRIPT_BASE / sanitized / f"{session_id}.jsonl"

    final_json = None
    try:
        final_json = json.loads(stdout)
    except Exception:
        pass

    grading = grade(workdir) if not timed_out else {}

    return {
        "arm": arm, "rep": rep, "session_id": session_id,
        "workdir": str(workdir), "elapsed_s": elapsed,
        "exit_code": rc, "timed_out": timed_out,
        "stdout_tail": stdout[-2000:],
        "stderr_tail": stderr[-2000:],
        "final_json": final_json,
        "transcript": str(transcript) if transcript.exists() else None,
        "grading": grading,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--arms", nargs="+", default=list(PROMPTS), choices=list(PROMPTS))
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--model", default=None)
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    if shutil.which("claude") is None:
        sys.exit("error: `claude` not found in PATH")
    if shutil.which("uv") is None:
        sys.exit("error: `uv` not found in PATH")

    RESULTS.mkdir(exist_ok=True)
    runs = []
    for arm in args.arms:
        for rep in range(1, args.reps + 1):
            print(f"\n=== {arm} rep {rep}/{args.reps} ===", flush=True)
            r = run_arm(arm, rep, args.model, args.timeout)
            g = r.get("grading", {})
            v = g.get("visible", {})
            h = g.get("holdout", {})
            print(f"  elapsed: {r['elapsed_s']:.1f}s "
                  f"visible: {v.get('passed','?')}/{v.get('total','?')} "
                  f"holdout: {h.get('passed','?')}/{h.get('total','?')}")
            if r.get("transcript"):
                print(f"  transcript: {r['transcript']}")
            else:
                print("  transcript: (not found)")
            runs.append(r)

    out = RESULTS / "runs.json"
    out.write_text(json.dumps(runs, indent=2))
    print(f"\nwrote {out}")
    print("next: uv run python analyze.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
