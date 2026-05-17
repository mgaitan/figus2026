# figus2026

[![ci](https://github.com/mgaitan/figus2026/workflows/ci/badge.svg)](https://github.com/mgaitan/figus2026/actions?query=workflow%3Aci)
[![docs](https://img.shields.io/badge/docs-blue.svg?style=flat)](https://mgaitan.github.io/figus2026/)
[![pypi version](https://img.shields.io/pypi/v/figus2026.svg)](https://pypi.org/project/figus2026/)
[![Changelog](https://img.shields.io/github/v/release/mgaitan/figus2026?include_prereleases&label=changelog)](https://github.com/mgaitan/figus2026/releases)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/mgaitan/figus2026/actions/workflows/ci.yml)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mgaitan/figus2026/blob/main/LICENSE)

Nuestro album de figus para el mundial

## Quick Start

Run directly without installing via `uvx`:

```bash
uvx figus2026 --help
```

When running from source, we use {term}`PYTHONPATH` in docs examples so the local package is importable without an install step.

```{richterm} env PYTHONPATH=../src uv run -m figus2026 --help
:hide-command: true
```

To install the tool permanently, use:

```bash
uv tool install figus2026
```

## Documentation Map (Diataxis)

This project follows the [Diataxis](https://diataxis.fr/) framework:

- Tutorials: learning-oriented, step-by-step.
- How-to guides: goal-oriented operational procedures.
- Reference: factual, lookup-first technical details.
- Explanation: context, rationale, and design choices.


```{toctree}
:maxdepth: 2
:caption: Tutorials

getting_started.md
```

```{toctree}
:maxdepth: 2
:caption: How-to Guides

development_workflow.md
```

```{toctree}
:maxdepth: 2
:caption: Reference

configuration.md
```

```{toctree}
:maxdepth: 2
:caption: Explanation

about_the_docs.md
```

```{toctree}
:maxdepth: 2
:caption: Project Policies

../CONTRIBUTING.md
../CODE_OF_CONDUCT.md
```
