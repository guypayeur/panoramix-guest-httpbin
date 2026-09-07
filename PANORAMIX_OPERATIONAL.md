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
| Add `image:` (or any engine pin) to the Unit YAML | **Rejected** — pin stays 0.5; the container runtime records `@sha256` in its binding / lock sidecar |

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

## Image digest for the container profile

The container runtime ([panoramix-runtime](https://github.com/guypayeur/panoramix-runtime)) admits a **guest-CI image digest**. That pin is **not** a Unit field. Pin stays **0.5**. Do not add `image:` here.

Guest CI (off-box, not the operator host) builds the **runtime recipe** image — contract `build.command` + `run.entrypoint`; this repo’s `Dockerfile` is unused — and emits:

```text
localhost/panoramix/httpbin@sha256:<digest>
```

How CI emits it (from a [panoramix-runtime](https://github.com/guypayeur/panoramix-runtime) checkout, this tree as `GUEST_ROOT`):

```bash
export GUEST_ROOT=/path/to/panoramix-guest-httpbin
python3 -m runtime.apply record-lock
# JSON: image, digest, path → bindings/guest-httpbin.lock.yaml
```

Equivalent: generate `Containerfile.runtime` from the Unit, `podman build --timestamp 0`, then `podman image inspect --format '{{.Digest}}'`.

Publish the `@sha256` line as a CI artifact or log. The operator copies it into the runtime lock sidecar. Runtime `apply` compares that digest; a local rebuild that is not that object is refused.

Operator-side schema: [panoramix-runtime bindings/README.md](https://github.com/guypayeur/panoramix-runtime/blob/main/bindings/README.md) (R11 / runtime #26).
