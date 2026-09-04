# Panoramix operational dogfood notes

Guest for [guypayeur/panoramix](https://github.com/guypayeur/panoramix) [OPERATIONAL.md](https://github.com/guypayeur/panoramix/blob/main/OPERATIONAL.md) / issue #4.

## Claim

httpbin is a real repo (not under `platform-tools/fixtures/`). The platform owns the envelope; httpbin stays an opaque HTTP program.

## Domain-leak log

| Temptation | Decision |
|---|---|
| Put request/response schema types on the adapter | **Rejected** — guest speaks HTTP to public port only for dogfood v1 |
| Add an “httpbin SDK” facet | **Rejected** — HTTP/1.1 + env is the envelope |
| Teach `apply` to walk Flask imports | **Rejected** — Rec 2 gotcha: digest is entrypoint paths only (`platform_run.py`) |
| Encode Postman collection semantics in contract | **Rejected** — content-agnostic |

## Run (with panoramix tools available)

```bash
pip install -e .
# from a panoramix checkout:
python3 platform-tools/platform_check.py /path/to/panoramix-guest-httpbin
python3 platform-tools/platform_emulate.py /path/to/panoramix-guest-httpbin --run --duration 2
```

## Digest gotcha

`run.entrypoint` names only `platform_run.py`. Editing `httpbin/core.py` alone must **not** change the deploy digest under emulate’s entrypoint rule. Editing `platform_run.py` must.
