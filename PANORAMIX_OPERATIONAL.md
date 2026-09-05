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
| Pin Flask/Werkzeug in the Unit contract | **Rejected** — `build` is admission shape; emulate does not execute `build.command` |
| Add `/whoami` so emulate's fixture demo has a domain route | **Rejected** — probe is already `/get` |

## Run (with panoramix tools available)

httpbin's Flask app needs a 1.x stack on Python 3.12 (`Werkzeug.BaseResponse`). Do **not** need `pip install -e .` (that pulls gevent/raven). From a shell that can import `httpbin.core`:

```bash
pip install 'Flask==1.1.4' 'Werkzeug==1.0.1' 'Jinja2==2.11.3' \
  'itsdangerous==1.1.0' 'MarkupSafe==1.1.1' 'click==7.1.2' \
  'flasgger>=0.9.7.1' six decorator brotlipy PyYAML

GUEST=/path/to/panoramix-guest-httpbin
# from a panoramix checkout:
python3 platform-tools/platform_check.py "$GUEST"
python3 platform-tools/platform_emulate.py "$GUEST" --run --duration 2
python3 platform-tools/platform_serve.py "$GUEST" --port 19210
# other terminal:
python3 platform-tools/platform_ctl.py --url http://127.0.0.1:19210 apply
python3 platform-tools/demo_operational.py "$GUEST"
```

Emulate only: Unix adapter, localhost edge, stamped `PLATFORM_NETWORK_EGRESS`. `build.command` is not run.

## Digest gotcha

`run.entrypoint` names only `platform_run.py`. Editing `httpbin/core.py` alone must **not** change the deploy digest under emulate’s entrypoint rule. Editing `platform_run.py` must.
