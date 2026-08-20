#!/usr/bin/env python
from __future__ import print_function

import argparse

import client


def assert_schema(job):
    assert job["api_version"] == "1.0"
    assert job["problem_type"] == "exact_cover"
    assert job["objective"] == "feasibility"
    assert isinstance(job["data"], dict)
    assert isinstance(job["options"], dict)
    assert isinstance(job["billing"], dict)
    assert "universe_size" in job["data"]
    assert "rows" in job["data"]
    assert job["options"]["logical_rows"] == 1000000
    assert job["options"]["require_exact"] is True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8080)
    args = p.parse_args()

    (
        status,
        response,
        elapsed,
        rows,
        local_ok,
        job,
    ) = client.run_job(
        args.host,
        args.port,
        universe_size=300,
        row_width=3,
        decoys=4000,
        logical_rows=1000000,
        job_id="test-large-airline-shape-001",
    )

    assert_schema(job)

    print("HKD_STANDARD_API_LARGE_TEST")
    print("api_version=%s" % job["api_version"])
    print("problem_type=%s" % job["problem_type"])
    print("objective=%s" % job["objective"])
    print("json_schema_valid=True")
    print("universe_size=300")
    print("candidate_rows=%d" % len(rows))
    print("logical_rows=1000000")
    print("response_status=%s" % response.get("status"))
    print("server_verified=%s" % response.get("verified"))
    print("client_verified=%s" % local_ok)
    print("free_limit_triggered=%s" % response.get("free_limit_triggered", False))
    print("upgrade_required=%s" % response.get("upgrade_required", False))
    print("elapsed_seconds=%.6f" % elapsed)

    if response.get("free_limit_triggered"):
        passed = (
            status == 200 and
            response.get("upgrade_required") is True
        )
    else:
        passed = (
            status == 200 and
            response.get("verified") and
            local_ok
        )

    print("PASS=%s" % passed)


if __name__ == "__main__":
    main()
