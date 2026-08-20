# HKD Optimizer - Exact Cover Service

HKD Optimizer is a network-accessible Exact Cover optimization service
with a simple versioned JSON API, a free evaluation edition, and a
paid/unlimited edition.

The current v1 service supports:

``` text
problem_type=exact_cover
endpoint=POST /v1/jobs
api_version=1.0
```

The client sends a portable JSON job to `server_free.py` or
`server_paid.py`. The server solves the Exact Cover instance and returns
selected rows together with exactness and verification metadata.
`test.py` and `test_large.py` remain unobfuscated so users can inspect
exactly what is being tested.

**Benchmark scope:** The approximately 100x result below is a measured
comparison against the project's dense logical-frontier exact baseline.
It is not a claim of approximately 100x versus every commercial or
state-of-the-art optimization solver.

## Quick Start - Free Server

Start the free server:

``` bash
python3 server_free.py
```

Expected startup is similar to:

``` text
HKD_OPTIMIZER_SERVICE
api_version=1.0
edition=FREE
listen=0.0.0.0:8080
endpoint=POST /v1/jobs
supported_problem_types=exact_cover
hkd_socket_edition=PAID
hkd_thread_edition=PAID
```

From another machine, or another terminal on the same machine, run:

``` bash
python3 test.py --host SERVER_IP --port 8080
```

For localhost:

``` bash
python3 test.py --host 127.0.0.1 --port 8080
```

The free-compatible test uses:

``` text
api_version=1.0
problem_type=exact_cover
objective=feasibility
universe_size=90
row_width=3
planted_exact_cover_rows=30
decoy_rows=600
candidate_rows=630
logical_rows=100000
require_exact=True
```

A successful run has the form:

``` text
HKD_STANDARD_API_TEST
api_version=1.0
problem_type=exact_cover
objective=feasibility
json_schema_valid=True
universe_size=90
candidate_rows=630
logical_rows=100000
response_status=SOLVED
server_verified=True
client_verified=True
free_limit_triggered=False
PASS=True
```

`server_verified=True` means the server verified that the returned rows
form an exact cover. `client_verified=True` means the unobfuscated test
code independently verifies the returned solution.

## Standard Job Format

HKD Optimizer uses a versioned JSON envelope rather than an
application-specific wire protocol:

``` json
{
  "api_version": "1.0",
  "problem_type": "exact_cover",
  "job_id": "example-001",
  "objective": "feasibility",
  "data": {
    "universe_size": 300,
    "rows": [
      [0, 1, 2],
      [3, 4, 5]
    ]
  },
  "options": {
    "logical_rows": 1000000,
    "require_exact": true
  },
  "billing": {
    "mode": "quote"
  }
}
```

### Fields

  -----------------------------------------------------------------------
  Field                               Meaning
  ----------------------------------- -----------------------------------
  `api_version`                       Wire-format version. Current
                                      version is `1.0`.

  `problem_type`                      Solver family. Current release
                                      supports `exact_cover`.

  `job_id`                            Optional caller-supplied
                                      identifier.

  `objective`                         `feasibility` for Exact Cover.

  `data.universe_size`                Number of elements that must each
                                      be covered exactly once.

  `data.rows`                         Candidate subsets represented as
                                      arrays of universe indices.

  `options.logical_rows`              Logical candidate-space size used
                                      by the HKD sparse-work model.

  `options.require_exact`             Must be `true` in the current Exact
                                      Cover API.

  `billing.mode`                      Reserved billing/quoting metadata.
  -----------------------------------------------------------------------

The envelope is intentionally extensible so future versions can route
additional optimization problem types without replacing the HTTP
protocol.

## Free Edition Limits

The free server accepts Exact Cover jobs up to:

``` text
universe_size <= 120
candidate rows <= 1,200
logical_rows   <= 100,000
```

`test.py` fits inside those limits.

`test_large.py` intentionally exceeds them. Against `server_free.py`,
the correct result is an upgrade response such as:

``` text
response_status=REJECTED
free_limit_triggered=True
upgrade_required=True
PASS=True
```

This is a successful free-edition boundary test: `PASS=True` means the
limit was enforced correctly.

## Airline-Shaped Large Exact Cover Example

`test_large.py` contains the large public benchmark shape used for the
airline operations demonstration.

Run it against the paid/unlimited server:

``` bash
python3 server_paid.py
```

Then:

``` bash
python3 test_large.py --host SERVER_IP --port 8080
```

### Exact Variables Used by `test_large.py`

The test constructs the job with:

``` python
universe_size=300
row_width=3
decoys=4000
logical_rows=1000000
job_id="test-large-airline-shape-001"
```

This produces:

``` text
universe elements / scheduled-flight slots = 300
elements per candidate duty                = 3
planted exact-cover duties                 = 100
decoy candidate duties                     = 4,000
actual candidate rows                      = 4,100
logical candidate rows                     = 1,000,000
objective                                  = feasibility
exact solution required                    = True
```

Because:

``` text
300 / 3 = 100
```

the generator first creates 100 non-overlapping three-element rows:

``` text
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]
...
[297, 298, 299]
```

Together these rows provide a guaranteed exact cover of all 300 universe
elements.

The generator then adds 4,000 deterministic pseudo-random three-element
decoy rows. The resulting optimization instance therefore contains
**4,100 materialized candidate rows** embedded in a **1,000,000-row
logical candidate space**.

The airline interpretation is:

``` text
universe element       -> scheduled flight leg / assignment obligation
candidate 3-item row   -> candidate duty covering three obligations
exact cover            -> every scheduled obligation assigned exactly once
duplicate coverage     -> forbidden
uncovered obligation   -> forbidden
```

This is an airline-shaped Exact Cover benchmark. It is not a claim that
the synthetic test contains a carrier's proprietary crew roster, union
rules, FAA legality engine, seat inventory, or live operational data.

### Paid Test Result on Obfuscated `server_paid.py`

A tested paid-server run on Ubuntu produced:

``` text
HKD_STANDARD_API_LARGE_TEST
api_version=1.0
problem_type=exact_cover
objective=feasibility
json_schema_valid=True
universe_size=300
candidate_rows=4100
logical_rows=1000000
response_status=SOLVED
server_verified=True
client_verified=True
free_limit_triggered=False
upgrade_required=False
elapsed_seconds=0.130635
PASS=True
```

The corresponding small test produced:

``` text
HKD_STANDARD_API_TEST
api_version=1.0
problem_type=exact_cover
objective=feasibility
json_schema_valid=True
universe_size=90
candidate_rows=630
logical_rows=100000
response_status=SOLVED
server_verified=True
client_verified=True
free_limit_triggered=False
elapsed_seconds=0.010862
PASS=True
```

The paid server startup was:

``` text
HKD_OPTIMIZER_SERVICE
api_version=1.0
edition=PAID
listen=0.0.0.0:8080
endpoint=POST /v1/jobs
supported_problem_types=exact_cover
hkd_socket_edition=PAID
hkd_thread_edition=PAID
```

## Approximately 100x End-to-End Airline Benchmark

The corresponding airline-shaped dense-vs-HKD socket benchmark measured:

``` text
AIRLINE_DENSE_VS_HKD_SOCKET_BENCHMARK
dense_end_to_end_seconds=18.713692
hkd_end_to_end_seconds=0.194723
end_to_end_speedup=96.10x
dense_server_verified=True
hkd_server_verified=True
dense_client_verified=True
hkd_client_verified=True
same_solution=True
selected_duties=100
payload_bytes=53010
PASS=True
```

That is approximately a **100x end-to-end speedup**:

``` text
18.713692 seconds
        |
        v
0.194723 seconds

speedup = 96.10x
```

Both paths returned verified exact solutions, and the benchmark
reported:

``` text
same_solution=True
```

The precise benchmark claim is:

**On this airline-shaped Exact Cover workload, HKD measured 96.10x
faster end-to-end than the project's dense logical-frontier exact
baseline, while both server and client verification passed and both
paths returned the same solution.**

The benchmark should not be interpreted as a demonstrated 96.10x
advantage over Gurobi, CPLEX, OR-Tools CP-SAT, SCIP, DLX, or every
production airline optimizer. Those require separate side-by-side
benchmarks.

## Paid / Unlimited Edition

The unlimited edition removes the free-edition problem-size gate,
subject to the server's absolute safety limits.

### Buy Unlimited

Purchase the unlimited edition here:

https://buy.stripe.com/3cIcMY1ejdQz5fsaR1gUM0b

After purchase, delivery and licensing should be handled according to
the terms presented with the product.

## Recommended Release Layout

``` text
server_free.py       obfuscated
server_paid.py       obfuscated
client.py            obfuscated
test.py              unobfuscated
test_large.py        unobfuscated
```

Keeping the tests unobfuscated makes the benchmark contract inspectable.
Users can see the exact job construction, API fields, free-edition
boundary, and independent verification logic without exposing the
protected implementation.

## Verification Model

A solve is accepted only when the selected rows cover every universe
element exactly once.

Conceptually, if `S` is the set of selected candidate rows and `U` is
the universe:

``` text
for every element u in U:
    u occurs in exactly one selected row in S
```

The service reports:

``` text
exact=True
verified=True
```

and the test client independently reconstructs the coverage from the
returned row IDs.

## Important Benchmark Interpretation

The 96.10x result demonstrates acceleration relative to the dense
logical-frontier baseline used by this project. It does not by itself
establish a 96.10x advantage over state-of-the-art Exact Cover, SAT,
constraint-programming, mixed-integer, or airline-optimization systems.

For stronger comparative claims, benchmark the same instances, hardware,
exactness requirements, and solution objectives against recognized
production solvers.
