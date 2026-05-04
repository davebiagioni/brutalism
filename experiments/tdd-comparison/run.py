#!/usr/bin/env python3
"""Run the TDD comparison experiment headlessly across plugin arms.

For each (arm, rep) pair:
  1. Create a fresh workdir under results/ with the task + fixed tests.
  2. Invoke `claude -p` with a known session-id and the arm-specific prompt.
  3. Locate the resulting transcript JSONL and run pytest to verify.
  4. Save run metadata to results/runs.json.

Run analyze.py afterwards to aggregate metrics.
"""
from __future__ import annotations

import argparse
import json
import os
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
TESTS = ROOT / "tests" / "test_lru.py"
TASK = ROOT / "task.md"
RESULTS = ROOT / "results"
TRANSCRIPT_BASE = Path.home() / ".claude" / "projects"


def sanitize_cwd(p: Path) -> str:
    return str(p).replace("/", "-")


def setup_workdir(arm: str, rep: int) -> Path:
    workdir = RESULTS / f"{arm}-{rep:02d}"
    if workdir.exists():
        shutil.rmtree(workdir)
    (workdir / "tests").mkdir(parents=True)
    shutil.copy(TESTS, workdir / "tests" / "test_lru.py")
    shutil.copy(TASK, workdir / "task.md")
    return workdir


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
    try:
        proc = subprocess.run(
            cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout_s
        )
        timed_out = False
    except subprocess.TimeoutExpired as e:
        elapsed = time.time() - start
        return {
            "arm": arm, "rep": rep, "session_id": session_id,
            "workdir": str(workdir), "elapsed_s": elapsed,
            "exit_code": None, "timed_out": True,
            "stdout_tail": (e.stdout or b"")[-2000:].decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")[-2000:],
            "stderr_tail": (e.stderr or b"")[-2000:].decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")[-2000:],
            "transcript": None, "test_returncode": None, "test_output": "",
        }
    elapsed = time.time() - start

    sanitized = sanitize_cwd(workdir)
    transcript = TRANSCRIPT_BASE / sanitized / f"{session_id}.jsonl"

    test_proc = subprocess.run(
        ["uv", "run", "--quiet", "--with", "pytest",
         "python", "-m", "pytest", "tests/test_lru.py", "-q"],
        cwd=workdir, capture_output=True, text=True, timeout=120,
    )

    final_json = None
    try:
        final_json = json.loads(proc.stdout)
    except Exception:
        pass

    return {
        "arm": arm, "rep": rep, "session_id": session_id,
        "workdir": str(workdir), "elapsed_s": elapsed,
        "exit_code": proc.returncode, "timed_out": timed_out,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
        "final_json": final_json,
        "transcript": str(transcript) if transcript.exists() else None,
        "test_returncode": test_proc.returncode,
        "test_output": (test_proc.stdout + test_proc.stderr)[-1500:],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--arms", nargs="+", default=list(PROMPTS),
                    choices=list(PROMPTS),
                    help="Which arms to run (default: all)")
    ap.add_argument("--reps", type=int, default=1,
                    help="Repetitions per arm (default: 1)")
    ap.add_argument("--model", default=None,
                    help="Optional model alias passed to claude (e.g. 'sonnet', 'opus')")
    ap.add_argument("--timeout", type=int, default=1800,
                    help="Per-run timeout seconds (default: 1800)")
    args = ap.parse_args()

    if shutil.which("claude") is None:
        sys.exit("error: `claude` not found in PATH")
    if shutil.which("uv") is None:
        sys.exit("error: `uv` not found in PATH (used to run pytest)")

    RESULTS.mkdir(exist_ok=True)
    runs = []
    for arm in args.arms:
        for rep in range(1, args.reps + 1):
            print(f"\n=== {arm} rep {rep}/{args.reps} ===", flush=True)
            r = run_arm(arm, rep, args.model, args.timeout)
            ok = (r.get("test_returncode") == 0)
            print(f"  elapsed: {r['elapsed_s']:.1f}s "
                  f"exit: {r.get('exit_code')} "
                  f"tests: {'PASS' if ok else 'FAIL'}")
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
