# Configuration (Reference)

This chapter is a lookup reference for environment variables used by commands,
documentation examples, and CI workflows.

```{glossary}
PYTHONPATH
  Python import search path.
  In this project docs, it is used for module execution from source (for example `PYTHONPATH=src uv run -m ...`).

GH_TOKEN
  Token consumed by the GitHub CLI (`gh`) for authenticated API operations.
  Useful for non-interactive runs such as manual workflow dispatch from CI or scripts.

GITHUB_TOKEN
  Ephemeral token automatically injected by GitHub Actions jobs.
  Used by workflows to interact with repository APIs with job-scoped permissions.

NO_COLOR
  De-facto standard variable used by CLI tools to disable ANSI colors.
  Prefer this for plain-text logs where color escape sequences are undesirable.

FORCE_COLOR
  Variable used by many CLIs to force color output even in non-interactive contexts.
  Use only when colorized logs improve readability and your environment strips correctly.

DATABASE_URL
  SQLAlchemy-compatible connection string for the album database.
  Defaults to `sqlite:///figus2026.db` (local SQLite file in the current directory).
  Example for a named file: `sqlite:////absolute/path/to/figus2026.db`.

ADMIN_USERNAME
  Username for the `/admin` panel.
  Defaults to `admin` if not set.
  Set in `.env` (not versioned — copy from `.env.example`).

ADMIN_PASSWORD
  Password for the `/admin` panel.
  **Required**: the admin panel rejects all logins when this variable is absent or empty.
  Set in `.env` (not versioned — copy from `.env.example`).

ADMIN_SECRET_KEY
  Secret key used to sign the admin session cookie.
  Use a long, random string in production (e.g. `openssl rand -hex 32`).
  Defaults to an insecure placeholder; always override before deploying.
```

## Setting up the admin panel

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
# then edit .env with your preferred values
```

The admin panel is available at `/admin` and requires a browser login.
Only {term}`ADMIN_USERNAME` and {term}`ADMIN_PASSWORD` are checked.
{term}`ADMIN_SECRET_KEY` signs the session cookie; rotate it if the key is ever exposed.
