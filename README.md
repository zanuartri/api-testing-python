# api-testing-python

![CI](https://github.com/zanuartri/api-testing-python/actions/workflows/ci.yml/badge.svg)

API test automation portfolio project in Python + pytest. Pure API testing
(no UI, no mobile) against two public REST services:

- [restful-api.dev](https://restful-api.dev) `/objects` — a free REST API
  that actually persists what you write, used for CRUD, schema, chained-request,
  and performance scenarios.
- [dummyjson.com](https://dummyjson.com) `/auth` — token-based login, used for
  the auth and negative-testing scenarios.

## Structure

```
clients/    thin wrappers around requests.Session (one per service)
schemas/    pydantic models describing expected response shapes
fixtures/   pytest fixtures — API clients, auth tokens, test data
tests/      one file per scenario
results/    results.json written after every run
```

### Why client wrappers + schema models instead of inline `requests` calls

Every test could call `requests.get(...)` directly, but scattering base URLs,
headers, and timeouts across dozens of test files means a single API change
(a new auth header, a renamed endpoint) turns into a find-and-replace across
the whole suite. The `clients/` wrappers hold that knowledge in one place, so
tests read as intent (`objects_client.create_object(payload)`) instead of
HTTP plumbing. Similarly, asserting on a handful of fields (`assert
body["name"] == ...`) lets a schema change slip through silently as long as
the fields you happened to check still look right. The `schemas/` pydantic
models validate the *entire* response shape — extra/missing/mistyped fields
fail loudly — which scales far better than manually growing a pile of
`assert "field" in body` checks as the API surface grows.

### Why the chained-request scenario matters

`tests/test_chained_flow.py` creates an object, reads it back using the id
the API just gave it, deletes it, then confirms a 404 on re-fetch. Testing
each endpoint in isolation (with hand-picked ids) can pass even when the real
integration is broken, because a real client never invents its own ids — it
uses whatever the previous response returned. Chaining requests the way an
actual consumer would is what catches bugs like "create returns an id the
read endpoint doesn't recognize," which isolated per-endpoint tests structurally
cannot catch.

### Negative testing approach

`tests/test_negative.py` and the negative cases in `tests/test_auth.py` send
deliberately broken input — wrong password, missing required field, unknown
user, nonexistent resource id — and assert both the 4xx status code *and*
that the error body has the expected shape (e.g. a `message` field). A
suite that only exercises the happy path tells you the API works when used
correctly; it says nothing about whether it fails safely, which is usually
where production incidents actually come from.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # defaults already work against the public APIs
```

## Run

```bash
pytest
```

Runs in well under a minute — no browser, no local server. After the run,
results are written to `results/results.json`:

```json
{
  "stack": "api-testing-python",
  "platform": "api",
  "run_at": "2026-01-01T00:00:00+00:00",
  "total": 15,
  "passed": 15,
  "failed": 0,
  "skipped": 0,
  "duration_seconds": 4.2,
  "tests": [{"name": "tests/test_auth.py::test_login_returns_valid_token", "status": "passed", "duration": 0.31}]
}
```

## CI

`.github/workflows/ci.yml` installs dependencies, runs pytest (failing the
build on any test failure), and uploads `results/results.json` as a build
artifact on every run.
