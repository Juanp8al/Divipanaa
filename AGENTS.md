# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

Divipana is a Django 5.2.1 monolithic web application for splitting expenses among friends ("Gastos Compartidos"). It uses server-side rendered templates, SQLite for local development, and is deployed to Render.com with PostgreSQL.

### Running the development server

```bash
cd /workspace
source venv/bin/activate
export DATABASE_URL="sqlite:///$(pwd)/db.sqlite3"
python manage.py runserver 0.0.0.0:8000
```

The `DATABASE_URL` environment variable **must** be set. Without it, `dj_database_url.config()` returns an empty dict and Django will error. For local development, use the SQLite URL shown above.

### Database migrations

After any model changes, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django system checks (lint equivalent)

```bash
python manage.py check
```

### Running tests

```bash
python manage.py test
```

Note: The repository currently has no automated tests. The test command runs cleanly but reports 0 tests.

### Key caveats

- **No SQLite fallback in settings.py**: The settings file does NOT have a built-in SQLite fallback. You must always set `DATABASE_URL` before running any Django management command.
- **DEBUG mode**: `DEBUG=True` is active when `RENDER` is not in `os.environ` (which is the case in local/cloud dev).
- **ALLOWED_HOSTS**: In DEBUG mode, Django allows all hosts, so no configuration is needed for dev.
- **Google OAuth (optional)**: `django-allauth` is installed with Google provider. Standard username/password authentication works without configuring OAuth credentials.
- **Static files**: In DEBUG mode, Django serves static files from the `static/` directory. No `collectstatic` needed for development.
- **The `Divipana` file** in the repo root is an old SQLite database file. It can be ignored.
