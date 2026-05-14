## Cursor Cloud specific instructions

### Overview

DiviPanas is a Django 5.2 shared-expense-splitting web app (Spanish language). Single Django app (`tasks/`) with all models and views. No frontend framework — Django templates + vanilla CSS.

### Running the dev server

```bash
export DATABASE_URL="sqlite:////workspace/db.sqlite3"
python3 manage.py runserver 0.0.0.0:8000
```

The `DATABASE_URL` environment variable is **required** — `settings.py` has no fallback. Use the SQLite URL above for local development.

### Database

- Uses SQLite for local dev via `dj-database-url` (set `DATABASE_URL` as shown above).
- Run `python3 manage.py migrate` after any model changes or on first setup.
- The `django.contrib.sites` framework is used by `allauth`; the initial migration creates SITE_ID=1 automatically.

### Lint / checks

There is no dedicated linter configured. Use Django's built-in system check:

```bash
python3 manage.py check
```

### Tests

```bash
python3 manage.py test
```

The test file (`tasks/tests.py`) is currently empty, but the test runner works.

### Key gotchas

- `DEBUG = True` only when the `RENDER` env var is **not** set (which is the case in local dev).
- `ALLOWED_HOSTS` is empty in dev mode, but Django's dev server permits localhost connections regardless when `DEBUG=True`.
- Google OAuth (`allauth`) is configured but non-functional without API credentials; standard username/password auth works fine.
- There are duplicate decorator applications in `views.py` (e.g. double `@login_required` on `dashboard`). These are harmless but notable.
