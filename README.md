# figus2026

[![CI](https://github.com/mgaitan/figus2026/actions/workflows/ci.yml/badge.svg)](https://github.com/mgaitan/figus2026/actions/workflows/ci.yml)
[![docs](https://img.shields.io/badge/docs-blue.svg?style=flat)](https://mgaitan.github.io/figus2026/)
[![pypi version](https://img.shields.io/pypi/v/figus2026.svg)](https://pypi.org/project/figus2026/)
[![Changelog](https://img.shields.io/github/v/release/mgaitan/figus2026?include_prereleases&label=changelog)](https://github.com/mgaitan/figus2026/releases)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/mgaitan/figus2026/actions/workflows/ci.yml)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mgaitan/figus2026/blob/main/LICENSE)

Cloud sticker album for the 2026 World Cup.

## Quick Start

Run the API locally:

```bash
uv run uvicorn figus2026.app:app --reload
```

Seed data is created automatically in `figus2026.db` for the prototype. The first MVP endpoints are:

- `GET /health`
- `GET /api/countries`
- `GET /api/countries/ARG/stickers`
- `POST /api/collectors/demo/packs/open`

## Development

- Install dependencies with `uv sync`.
- New dependency releases are delayed by one week via `uv` cooldown (`[tool.uv].exclude-newer = "1 week"`), with per-package overrides when required (for example, `ty`).
- Install [`prek`](https://github.com/j178/prek) as an external tool:

```bash
uv tool install prek
```

- Install git hooks with `prek`:

```bash
prek install
```

- Run the local QA bundle with `prek`:

```bash
prek run --all-files
```

- PRs with documentation changes publish a docs preview at:

```text
https://mgaitan.github.io/figus2026/_preview/pr-<PR_NUMBER>/
```

## Documentation

- Docs follow [Diataxis](https://diataxis.fr/).
- Start at `docs/index.md` and read:
  - `docs/getting_started.md` (tutorial),
  - `docs/development_workflow.md` (how-to),
  - `docs/configuration.md` (reference),
  - `docs/about_the_docs.md` (explanation and design rationale).
