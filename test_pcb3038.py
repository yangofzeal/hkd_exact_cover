#!/usr/bin/env python3
from __future__ import print_function

import argparse
import json
import math
import os
import time

import hkd_socket


API_VERSION = "1.0"
KNOWN_OPTIMUM = 137694


def parse_tsp(path):
    coords = {}
    dimension = None
    edge_weight_type = None
    in_coords = False

    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            if line.startswith("DIMENSION"):
                dimension = int(line.split(":")[-1].strip())
                continue

            if line.startswith("EDGE_WEIGHT_TYPE"):
                edge_weight_type = line.split(":")[-1].strip()
                continue

            if line == "NODE_COORD_SECTION":
                in_coords = True
                continue

            if line == "EOF":
                break

            if in_coords:
                parts = line.split()
                if len(parts) >= 3:
                    node = int(parts[0])
                    coords[node] = (
                        float(parts[1]),
                        float(parts[2]),
                    )

    if dimension != 3038:
        raise RuntimeError(
            "unexpected pcb3038 dimension: %r" % dimension
        )

    if edge_weight_type != "EUC_2D":
        raise RuntimeError(
            "unexpected edge type: %r" % edge_weight_type
        )

    if len(coords) != dimension:
        raise RuntimeError(
            "coordinate count mismatch"
        )

    return dimension, edge_weight_type, coords


def parse_opt_tour_after_solve(path):
    """
    NO-CHEAT RULE:
    This function must only be called after the server solve attempt finishes.
    """
    tour = []
    comment = None
    dimension = None
    in_tour = False

    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            if line.startswith("COMMENT"):
                comment = line.split(":", 1)[-1].strip()
                continue

            if line.startswith("DIMENSION"):
                dimension = int(line.split(":")[-1].strip())
                continue

            if line == "TOUR_SECTION":
                in_tour = True
                continue

            if in_tour:
                if line in ("-1", "EOF"):
                    break
                tour.append(int(line))

    return dimension, comment, tour


def nint(x):
    return int(x + 0.5)


def distance(coords, a, b):
    ax, ay = coords[a]
    bx, by = coords[b]
    dx = ax - bx
    dy = ay - by
    return nint(math.sqrt(dx * dx + dy * dy))


def tour_cost(coords, tour):
    total = 0
    n = len(tour)

    for i in range(n):
        total += distance(
            coords,
            tour[i],
            tour[(i + 1) % n],
        )

    return total


def validate_tour(tour, dimension):
    return (
        isinstance(tour, list)
        and len(tour) == dimension
        and len(set(tour)) == dimension
        and set(tour) == set(range(1, dimension + 1))
    )


def http_post(host, port, path, obj, timeout=300):
    body = json.dumps(
        obj,
        separators=(",", ":"),
    ).encode("utf-8")

    request = (
        "POST %s HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n\r\n"
        % (path, host, len(body))
    ).encode("ascii") + body

    sock = hkd_socket.create_connection(
        (host, port),
        timeout,
    )

    try:
        sock.sendall(request)
        raw = bytearray()

        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            raw.extend(chunk)

    finally:
        sock.close()

    if b"\r\n\r\n" not in raw:
        raise RuntimeError("invalid HTTP response")

    head, body = bytes(raw).split(
        b"\r\n\r\n",
        1,
    )

    status = int(
        head.split(None, 2)[1]
    )

    return (
        status,
        json.loads(body.decode("utf-8")),
        len(request),
    )


def build_no_cheat_tsp_job(coords):
    """
    Genuine TSP request.

    This deliberately does NOT encode a supplied optimum tour into Exact Cover.
    It sends only the raw pcb3038 coordinates and asks the standardized service
    to find and prove the minimum Hamiltonian cycle.

    Current server_paid.py is expected to reject this because it only advertises
    problem_type=exact_cover. That rejection is the correct behavior until a
    genuine weighted TSP solver is added.
    """
    ordered = []
    for city in range(1, 3039):
        x, y = coords[city]
        ordered.append([city, x, y])

    return {
        "api_version": API_VERSION,
        "problem_type": "tsp",
        "job_id": "tsplib-pcb3038-no-cheat",
        "objective": "minimize",
        "data": {
            "dimension": 3038,
            "edge_weight_type": "EUC_2D",
            "coordinates": ordered,
        },
        "options": {
            "require_exact": True,
            "require_single_hamiltonian_cycle": True,
            "prove_optimality": True,
        },
        "billing": {
            "mode": "quote",
        },
    }


def extract_candidate_tour(response):
    solution = response.get("solution")

    if not isinstance(solution, dict):
        return None

    tour = solution.get("tour")

    if not isinstance(tour, list):
        return None

    try:
        return [int(x) for x in tour]
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--tsp", default="pcb3038.tsp")
    p.add_argument("--opt-tour", default="pcb3038.opt.tour")
    p.add_argument("--dump-json", default="pcb3038_tsp_job.json")
    args = p.parse_args()

    print("HKD_TSPLIB_PCB3038_NO_CHEAT_TEST")

    # Phase 1: raw problem only.
    dimension, edge_type, coords = parse_tsp(
        args.tsp
    )

    print("phase=RAW_PROBLEM_ONLY")
    print("source_instance=%s" % args.tsp)
    print("dimension=%d" % dimension)
    print("edge_weight_type=%s" % edge_type)
    print("opt_tour_read_before_solve=False")

    job = build_no_cheat_tsp_job(coords)

    with open(args.dump_json, "w") as f:
        json.dump(
            job,
            f,
            separators=(",", ":"),
            sort_keys=True,
        )

    t0 = time.time()

    status, response, wire_bytes = http_post(
        args.host,
        args.port,
        "/v1/jobs",
        job,
    )

    elapsed = time.time() - t0

    print("phase=SERVER_SOLVE_ATTEMPT_COMPLETE")
    print("http_status=%d" % status)
    print("response_status=%s" % response.get("status"))
    print("server_error=%s" % response.get("error"))
    print("server_detail=%s" % response.get("detail"))
    print("wire_bytes=%d" % wire_bytes)
    print("elapsed_seconds=%.6f" % elapsed)

    candidate = extract_candidate_tour(response)

    # Only now may the benchmark/reference optimum file be opened.
    opt_dimension, opt_comment, opt_tour = (
        parse_opt_tour_after_solve(
            args.opt_tour
        )
    )

    print("phase=POST_SOLVE_REFERENCE_VERIFICATION")
    print("opt_tour_read_after_solve=True")
    print("published_tour_comment=%s" % opt_comment)

    reference_valid = validate_tour(
        opt_tour,
        dimension,
    )

    reference_cost = (
        tour_cost(coords, opt_tour)
        if reference_valid
        else None
    )

    print("reference_tour_valid=%s" % reference_valid)
    print("reference_cost=%s" % reference_cost)
    print("known_optimum=%d" % KNOWN_OPTIMUM)
    print("reference_matches_known_optimum=%s" % (
        reference_cost == KNOWN_OPTIMUM
    ))

    if candidate is None:
        print("candidate_tour_returned=False")
        print("candidate_cost=None")
        print("candidate_matches_optimum=False")

        unsupported = (
            response.get("error") == "invalid_job"
            and "unsupported_problem_type" in str(
                response.get("detail")
            )
        )

        print("current_server_supports_exact_tsp=False")
        print("capability_rejection_correct=%s" % unsupported)
        print(
            "IMPORTANT=Current server_paid.py cannot honestly solve pcb3038 "
            "because v1 supports exact_cover feasibility only; weighted TSP "
            "minimization and subtour elimination are not implemented."
        )
        print("PASS=%s" % (
            unsupported
            and reference_cost == KNOWN_OPTIMUM
        ))
        return

    candidate_valid = validate_tour(
        candidate,
        dimension,
    )

    candidate_cost = (
        tour_cost(coords, candidate)
        if candidate_valid
        else None
    )

    exact_flag = response.get("exact") is True
    verified_flag = response.get("verified") is True
    objective = response.get("objective_value")

    print("candidate_tour_returned=True")
    print("candidate_tour_valid=%s" % candidate_valid)
    print("candidate_cost=%s" % candidate_cost)
    print("server_objective_value=%s" % objective)
    print("server_exact=%s" % exact_flag)
    print("server_verified=%s" % verified_flag)
    print("candidate_matches_optimum=%s" % (
        candidate_cost == KNOWN_OPTIMUM
    ))

    passed = (
        candidate_valid
        and candidate_cost == KNOWN_OPTIMUM
        and exact_flag
        and verified_flag
        and objective == KNOWN_OPTIMUM
    )

    print("PASS=%s" % passed)


if __name__ == "__main__":
    main()
