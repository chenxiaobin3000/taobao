# CLAUDE.md

This file gives Claude Code project-specific context and guardrails for working in this repository.

## Project Summary

Taobao Admin is a Django + Vue 2 management system for e-commerce operations and finance data. It manages platform/shop data, imports raw order-related spreadsheets, merges raw records into archived business tables, refreshes summary tables, and displays reports.

Primary stack:

- Backend: Python 3.10+, Django 5.2.8, django-cors-headers (4.x), SQLite
- Frontend: Vue 2.6.10, Vue Router 3.0.2, Vuex 3.1.0, Element UI 2.13.2, Axios 0.18.1, ECharts 4.2.1, xlsx 0.14.1
- Database: root-level `cxkw.db`
- Backend dependencies: root-level `requirements.txt`
- Frontend dependencies: `client/package.json`

## Repository Layout

```text
.
├── app/                    # Django business app
│   ├── management/commands/ # Custom management commands, including initialize
│   ├── models/              # Django models and native SQL query helpers
│   │   ├── const/           # Business constants
│   │   ├── middle/          # Summary/helper models
│   │   ├── original/        # Raw imported data models
│   │   ├── report/          # Report query models and native SQL helpers
│   │   ├── system/          # Company/shop/user/role/permission models
│   │   └── trunk/           # Archived/core business models
│   ├── templates/           # Django template directory for built frontend index.html
│   ├── url/                 # URL groups by business domain
│   └── views/               # API views
├── client/                  # Vue CLI frontend
│   ├── public/
│   └── src/
│       ├── api/             # Frontend API wrappers
│       ├── components/
│       ├── layout/
│       ├── router/          # Routes and role-gated menus
│       ├── store/
│       └── views/
├── docs/                    # Project documents
├── server/                  # Django project settings/urls/asgi/wsgi
├── static/                  # Django static assets; built frontend static files go here
├── backup/                  # SQLite backup output directory
├── cxkw.db                  # SQLite database
├── manage.py
└── requirements.txt
```

## Core Architecture

Backend routing starts at `server/urls.py`, which concatenates URL lists from:

- `app/url/system.py`
- `app/url/original.py`
- `app/url/trunk.py`
- `app/url/middle.py`
- `app/url/report.py`

The root path returns `app/templates/index.html` through `TemplateView`, so production-style deployment expects the Vue build output to be copied into Django static/template directories.

Most backend views:

- Use function-based Django views
- Use `@require_POST`
- Return `JsonResponse`
- Use response shape similar to:

```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

Frontend requests go through `client/src/utils/request.js`. In development, `client/vue.config.js` proxies:

- `/api` -> `http://localhost:8000/api` (with `pathRewrite: { '^/api': '/' }`)
- `/upload` -> `http://localhost:8000/upload`

## Business Domains

### System

Backend:

- `app/views/account.py`
- `app/views/system/`
- `app/models/account.py`
- `app/models/system/`

Frontend:

- `client/src/views/company/`
- `client/src/views/system/`
- `client/src/api/account.js`
- `client/src/api/system/`

Responsibilities:

- Account login/logout/register/password reset
- Company, platform, shop, product, product alias management
- User, role, permission management
- User-shop relationships

### Original Data

Backend:

- `app/views/original/`
- `app/models/original/`

Frontend:

- `client/src/views/original/`
- `client/src/api/original/`

Responsibilities:

- Raw order data
- Raw fake-order data
- Raw promotion and promotion-detail data
- Raw deduction data
- Raw polymerize data
- Raw purchase data
- Raw refund/refund-gift data
- Raw transfer/small-payment data

These pages often support Excel import, list queries, single delete, and delete-all flows.

### Trunk/Archived Data

Backend:

- `app/views/trunk/`
- `app/models/trunk/`

Frontend:

- `client/src/views/trunk/`
- `client/src/api/trunk/`

Responsibilities:

- Merge raw data into archived/core records
- Query archived records
- Delete archived records

The common endpoint pattern is:

```text
POST /api/<domain>/merge
POST /api/<domain>/getList
POST /api/<domain>/del
```

### Middle/Summary Tools

Backend:

- `app/views/middle/`
- `app/models/middle/`

Frontend:

- `client/src/views/middle/`
- `client/src/api/middle/`

Responsibilities:

- Order summary refresh/query
- Deduction summary refresh/query
- Fake summary refresh/edit/batch/complete
- Good prepare management
- Miscellaneous management
- Receipt-related APIs exist in backend, but are not obviously exposed in frontend menus

### Reports

Backend:

- `app/views/report/`
- `app/models/report/`
- `app/models/report/native_*.py`

Frontend:

- `client/src/views/report/`
- `client/src/api/report/`

Reports:

- Board report
- Year report
- Day report
- Good report and good follow
- Promotion report
- Cost report
- Order report
- Omission report
- Fake report endpoint exists, but there is no separate permission-tree menu item for it

Some report queries use raw SQL through `django.db.connection`.

## Permissions And Menus

Frontend permissions are role-code based. The reference list is `client/src/utils/role-data.js`; routes live under `client/src/router/modules/`.

Top-level domains:

- `1000`: System management
- `2000`: Company data
- `3000`: Original data
- `4000`: Archived data
- `5000`: Reports
- `6000`: Middle/helper tools

When adding a new frontend page, update all relevant places:

- `client/src/router/modules/*.js`
- `client/src/utils/role-data.js`
- `client/src/api/...`
- Matching backend `app/url/...` and `app/views/...`
- Any model/table changes in `app/models/...`

## Common Commands

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Current `requirements.txt` includes:

- `Django==5.2.8`
- `django-cors-headers>=4.0,<5.0`
- `tzdata>=2024.1; sys_platform == "win32"`

Run backend:

```bash
python manage.py runserver
```

Create/apply migrations:

```bash
python manage.py makemigrations app
python manage.py migrate
```

Initialize seed data:

```bash
python manage.py initialize
```

Run frontend:

```bash
cd client
npm install
npm run dev
```

Build frontend:

```bash
cd client
npm run build
```

Deploy built frontend into Django:

```bat
client\deploy.bat
```

## Batch Script Warnings

Be careful with existing `.bat` scripts.

- `server.bat` runs `backup.bat`, `clean.bat`, migrations, then starts Django.
- `backup.bat` copies `cxkw.db` into `backup/`.
- `clean.bat` deletes Python cache folders and also deletes `app\migrations\__init__.py`. Do not run it casually.
- `client\deploy.bat` deletes old frontend assets under `static/` and replaces `app/templates/index.html`.

Prefer explicit Python/npm commands while developing unless the user asks to run a batch script.

## Database Notes

- SQLite database file: `cxkw.db`
- Django database config: `server/settings.py`
- SQLite timeout is configured as `500`.
- `USE_TZ = False`, `TIME_ZONE = 'Asia/Shanghai'`.
- Database tables use custom `db_table` names such as `t_account` and many `t_*` business tables.
- Migrations exist under `app/migrations/`.

When changing models:

- Inspect existing `db_table` names before renaming anything.
- Avoid destructive schema changes unless explicitly requested.
- Generate migrations with `python manage.py makemigrations app`.
- Do not delete or regenerate the SQLite database without explicit approval.

## Coding Conventions

Backend patterns:

- Use function-based views consistent with existing code.
- Use `@require_POST` for API endpoints unless there is a clear reason not to.
- Use `transaction.atomic` where existing similar views do.
- Return `JsonResponse(..., encoder=MyJSONEncoder)` for business responses.
- Keep response shape compatible with frontend interceptors: `code`, `msg`, `data`.
- Preserve manager-style model methods where existing models use custom `objects` managers.

Frontend patterns:

- API wrappers live in `client/src/api/<domain>/`.
- Views live in `client/src/views/<domain>/`.
- Most list pages use `Pagination` and Vuex `mapState`.
- Login/password flows use `js-md5`.
- Auth state and cached values are handled in `client/src/utils/cache.js`.
- Request errors are handled centrally in `client/src/utils/request.js`.

Style and encoding:

- Prefer UTF-8 for new or rewritten files.
- Some older files may contain garbled Chinese comments/text. Do not spread the corruption; write new Chinese text as UTF-8.
- Keep changes narrow and consistent with surrounding code.

## Security And Production Caveats

Current settings are development-oriented:

- `DEBUG = True`
- `ALLOWED_HOSTS = []`
- `SECRET_KEY` is committed in source
- Login uses MD5 on the frontend
- Backend token/session validation appears incomplete; frontend stores `token`, but login mainly returns `id`

Do not present the current setup as production-ready. If productionizing, externalize secrets, configure hosts, close debug mode, and implement stronger backend authentication/authorization.

## Testing And Verification

There is no obvious backend test suite in the current tree.

Useful checks:

```bash
python -m py_compile manage.py server\settings.py server\urls.py
python manage.py check
```

Frontend checks depend on installed npm dependencies:

```bash
cd client
npm run build
```

If dependencies are missing or network access is unavailable, explain that verification could not be completed instead of inventing results.

## Working Safely In This Repo

- Do not overwrite user data in `cxkw.db`.
- Do not delete backups.
- Do not run destructive cleanup/deploy scripts unless requested.
- Do not change generated frontend build assets in `static/` unless doing a frontend deployment.
- Do not assume garbled comments are intentional business wording; verify against readable route names, permission labels, frontend constants, and UI files.
- If changing a business flow, inspect the matching backend view, model manager, frontend API wrapper, and Vue page together.
- If adding a backend endpoint, register it in the appropriate `app/url/*.py` file and add/update the matching frontend API wrapper if needed.
