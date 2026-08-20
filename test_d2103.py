#!/usr/bin/env python
from __future__ import print_function

import argparse
import json
import math
import os
import urllib.request

import hkd_socket


API_VERSION = "1.0"
D2103_TSP_URL = (
    "https://raw.githubusercontent.com/mastqe/tsplib/master/d2103.tsp"
)
D2103_TOUR_URL = (
    "https://raw.githubusercontent.com/mathinking/HopfieldNetworkToolbox/"
    "master/data/TSPFiles/TSPTours/d2103.opt.tour"
)
KNOWN_OPTIMUM = 80450


def download(url, path):
    print("download=%s" % url)
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    with open(path, "wb") as f:
        f.write(data)
    print("downloaded_bytes=%d path=%s" % (len(data), path))


def ensure_file(path, url):
    if not os.path.isfile(path):
        download(url, path)


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

    if dimension != 2103:
        raise RuntimeError(
            "unexpected d2103 dimension: %r" % dimension
        )

    if edge_weight_type != "EUC_2D":
        raise RuntimeError(
            "unexpected edge type: %r" % edge_weight_type
        )

    if len(coords) != dimension:
        raise RuntimeError(
            "coordinate count mismatch: %d != %d" %
            (len(coords), dimension)
        )

    return dimension, edge_weight_type, coords


def parse_tour(path):
    tour = []
    dimension = None
    comment = None
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

            if not in_tour:
                continue

            if line in ("-1", "EOF"):
                break

            tour.append(int(line))

    if dimension != 2103:
        raise RuntimeError(
            "unexpected tour dimension: %r" % dimension
        )

    if len(tour) != dimension:
        raise RuntimeError(
            "tour length mismatch: %d != %d" %
            (len(tour), dimension)
        )

    if len(set(tour)) != dimension:
        raise RuntimeError(
            "tour contains duplicate cities"
        )

    if set(tour) != set(range(1, dimension + 1)):
        raise RuntimeError(
            "tour does not contain exactly cities 1..2103"
        )

    return tour, comment


def nint(x):
    # TSPLIB EUC_2D: nearest integer.
    return int(x + 0.5)


def euc_2d(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return nint(math.sqrt(dx * dx + dy * dy))


def tour_cost(coords, tour):
    total = 0
    n = len(tour)

    for i in range(n):
        a = tour[i]
        b = tour[(i + 1) % n]
        total += euc_2d(coords[a], coords[b])

    return total


def build_exact_cover_certificate(tour, group_size=3):
    """
    Encode the supplied Hamiltonian tour as an Exact Cover certificate.

    Universe:
        0..N-1       : each city must appear exactly once
        N..2N-1      : each tour position must be filled exactly once

    A row covers a small consecutive block of city-position assignments from
    the published optimum tour. Grouping 3 positions per row yields 701 rows
    for d2103, keeping recursive Exact Cover depth below Python's usual
    recursion limit.

    This certificate verifies the known tour assignment. It does NOT make
    ordinary unweighted Exact Cover discover the minimum-distance TSP tour.
    Minimum-distance correctness is independently checked from the real
    coordinates and the published optimum length 80450.
    """
    n = len(tour)

    if n % group_size:
        raise ValueError(
            "group_size must divide dimension exactly"
        )

    rows = []
    row_assignments = []

    start = 0
    while start < n:
        row = []
        assignments = []

        for pos in range(start, start + group_size):
            city = tour[pos]

            # City constraint, zero based.
            city_constraint = city - 1

            # Position constraint.
            position_constraint = n + pos

            row.append(city_constraint)
            row.append(position_constraint)
            assignments.append((pos, city))

        rows.append(row)
        row_assignments.append(assignments)
        start += group_size

    return 2 * n, rows, row_assignments


def build_job(
    tour,
    logical_rows=1000000,
    group_size=3,
):
    universe_size, rows, assignments = (
        build_exact_cover_certificate(
            tour,
            group_size=group_size,
        )
    )

    job = {
        "api_version": API_VERSION,
        "problem_type": "exact_cover",
        "job_id": "tsplib-d2103-optimum-certificate",
        "objective": "feasibility",
        "data": {
            "universe_size": universe_size,
            "rows": rows,
        },
        "options": {
            "logical_rows": int(logical_rows),
            "require_exact": True,
        },
        "billing": {
            "mode": "quote",
        },
    }

    return job, assignments


def http_post(host, port, path, obj, timeout=180):
    body = json.dumps(
        obj,
        separators=(",", ":"),
    ).encode("utf-8")

    req = (
        "POST %s HTTP/1.1\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n\r\n"
        % (path, host, len(body))
    ).encode("ascii") + body

    s = hkd_socket.create_connection(
        (host, port),
        timeout,
    )

    try:
        s.sendall(req)
        raw = bytearray()

        while True:
            block = s.recv(65536)
            if not block:
                break
            raw.extend(block)

    finally:
        s.close()

    if b"\r\n\r\n" not in raw:
        raise RuntimeError(
            "invalid HTTP response"
        )

    head, body = bytes(raw).split(
        b"\r\n\r\n",
        1,
    )

    status = int(
        head.split(None, 2)[1]
    )

    return status, json.loads(
        body.decode("utf-8")
    ), len(req)


def reconstruct_tour(
    solution_rows,
    row_assignments,
    n,
):
    if not isinstance(solution_rows, list):
        return None

    positions = [None] * n

    for rid in solution_rows:
        if rid < 0 or rid >= len(row_assignments):
            return None

        for pos, city in row_assignments[rid]:
            if positions[pos] is not None:
                return None
            positions[pos] = city

    if any(x is None for x in positions):
        return None

    if len(set(positions)) != n:
        return None

    return positions


def canonical_cycle_equal(a, b):
    """
    Compare Hamiltonian cycles modulo rotation and reversal.
    """
    if len(a) != len(b):
        return False

    n = len(a)
    try:
        k = b.index(a[0])
    except ValueError:
        return False

    forward = True
    for i in range(n):
        if a[i] != b[(k + i) % n]:
            forward = False
            break

    if forward:
        return True

    for i in range(n):
        if a[i] != b[(k - i) % n]:
            return False

    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8080)
    p.add_argument("--tsp", default="d2103.tsp")
    p.add_argument("--tour", default="d2103.opt.tour")
    p.add_argument("--logical-rows", type=int, default=1000000)
    p.add_argument("--dump-json", default=None)
    args = p.parse_args()

    ensure_file(
        args.tsp,
        D2103_TSP_URL,
    )
    ensure_file(
        args.tour,
        D2103_TOUR_URL,
    )

    dimension, edge_type, coords = parse_tsp(
        args.tsp
    )
    optimum_tour, comment = parse_tour(
        args.tour
    )

    cost = tour_cost(
        coords,
        optimum_tour,
    )

    if cost != KNOWN_OPTIMUM:
        raise RuntimeError(
            "published tour cost mismatch: %d != %d" %
            (cost, KNOWN_OPTIMUM)
        )

    job, row_assignments = build_job(
        optimum_tour,
        logical_rows=args.logical_rows,
        group_size=3,
    )

    if args.dump_json:
        with open(args.dump_json, "w") as f:
            json.dump(
                job,
                f,
                separators=(",", ":"),
                sort_keys=True,
            )

    status, response, wire_bytes = http_post(
        args.host,
        args.port,
        "/v1/jobs",
        job,
    )

    solution_rows = (
        response.get("solution") or {}
    ).get("rows")

    reconstructed = reconstruct_tour(
        solution_rows,
        row_assignments,
        dimension,
    )

    reconstructed_cost = None
    cycle_match = False

    if reconstructed is not None:
        reconstructed_cost = tour_cost(
            coords,
            reconstructed,
        )
        cycle_match = canonical_cycle_equal(
            reconstructed,
            optimum_tour,
        )

    server_ok = bool(
        response.get("verified")
    )

    pass_all = (
        status == 200 and
        server_ok and
        reconstructed is not None and
        reconstructed_cost == KNOWN_OPTIMUM and
        cycle_match
    )

    print("HKD_TSPLIB_D2103_EXACT_COVER_CERTIFICATE")
    print("source_instance=d2103.tsp")
    print("source_tour=d2103.opt.tour")
    print("dimension=%d" % dimension)
    print("edge_weight_type=%s" % edge_type)
    print("published_tour_comment=%s" % comment)
    print("known_optimum=%d" % KNOWN_OPTIMUM)
    print("local_real_data_tour_cost=%d" % cost)
    print("exact_cover_universe=%d" % job["data"]["universe_size"])
    print("exact_cover_rows=%d" % len(job["data"]["rows"]))
    print("assignments_per_row=3")
    print("logical_rows=%d" % args.logical_rows)
    print("wire_bytes=%d" % wire_bytes)
    print("http_status=%d" % status)
    print("response_status=%s" % response.get("status"))
    print("server_exact=%s" % response.get("exact"))
    print("server_verified=%s" % server_ok)
    print("selected_certificate_rows=%s" % (
        len(solution_rows)
        if isinstance(solution_rows, list)
        else None
    ))
    print("reconstructed_2103_city_tour=%s" % (
        reconstructed is not None
    ))
    print("reconstructed_cost=%s" % reconstructed_cost)
    print("matches_published_optimum_cycle=%s" % cycle_match)
    print("IMPORTANT=Exact Cover verifies the supplied optimum-tour certificate; distance minimization is verified independently from TSPLIB coordinates.")
    print("PASS=%s" % pass_all)


if __name__ == "__main__":
    main()
