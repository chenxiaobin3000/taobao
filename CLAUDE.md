# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Taobao Admin — a Django + Vue 2 e-commerce operations backend for Taobao/Douyin shop data management. Backend at `app/`, frontend at `client/`, SQLite database `cxkw.db`, Django config at `server/`.

## Development commands

```bash
# Activate virtual environment
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
cd client && npm install && cd ..

# Database migrations (when models change)
python manage.py makemigrations app
python manage.py migrate

# Initialize seed data (first run only — creates default company, roles, permissions, admin user)
python manage.py initialize

# Start backend (port 8000)
python manage.py runserver

# Start frontend dev server (port 9527, proxies /api to localhost:8000)
cd client && npm run dev

# Build frontend for production deployment
cd client && npm run build && npm run deploy
```

Windows shortcut scripts: `server.bat` (backup → clean → migrate → runserver), `init.bat` (initialize), `client/server.bat` (frontend dev), `client/deploy.bat` (copy dist to Django static/templates).

Node version: 14.21.3 (per `.nvmrc`). Python 3.10+.

## Architecture

### Backend: Django with custom patterns (no Django REST Framework)

This project does NOT use Django REST Framework. It uses raw Django views with manual JSON parsing and raw SQL for complex queries.

**View pattern** — every view is a `@require_POST` function that:
1. Parses `json.loads(request.body)` for parameters
2. Calls model manager methods or raw SQL classes
3. Returns `JsonResponse(success(data))` or `JsonResponse(failed(msg))` via `MyJSONEncoder`

`app/views/common.py` defines `success(data)` → `{code: 0, msg: 'success', data: ...}` and `failed(msg, code=-1)` → `{code: -1, msg: ..., data: {}}`.

**Model pattern** — two coexisting approaches:
- **Django ORM models** (`app/models/*.py`): Custom managers with business methods. Example: `Account.objects.add(...)`, `Session.objects.getByToken(...)`.
- **Native SQL classes** (`app/models/report/native_*.py`): Classes inheriting from `app.models.model.Model` that use `connection.cursor()` with raw SQL and the `dictfetchall()` helper. Used for reports and complex aggregations.

**URL routing**: Each business domain has its own URL list in `app/url/<domain>.py`. These are concatenated in `server/urls.py`. All API routes use `/api/` prefix. The catch-all route serves `index.html` for the SPA.

**Authentication**: Custom `TokenAuthMiddleware` in `app/middleware/token_auth_middleware.py`. All `/api/` routes (except `/api/account/login` and `/api/account/register`) require a `token` header. On success, sets `request.account_id`, `request.user_id`, and `request.auth_token`.

### Frontend: Vue 2 + Element UI admin template

- **State**: Vuex store with modules (`account`, `app`, `permission`, `settings`, `tagsView`, `header`)
- **Routing**: `constantRoutes` (login, 404) + `asyncRoutes` loaded dynamically based on user roles. Router modules in `client/src/router/modules/` each define a route tree with numeric `roles` in meta.
- **Permissions**: `permission.js` navigation guard fetches user info/roles on first load, generates accessible routes via `store.dispatch('permission/generateRoutes', roles)`, then adds them dynamically.
- **API layer**: Axios instance in `client/src/utils/request.js` — attaches `token` header, intercepts responses checking for `code !== 0` (code -3 triggers re-login).
- **Dev proxy**: `vue.config.js` proxies `/api` → `http://localhost:8000/api` with path rewrite stripping `/api` prefix.

### Four-layer data pipeline

1. **Original data** (`t_user_*` tables) — raw imports from platform exports (orders, refunds, promotions, purchases, etc.)
2. **Trunk data** — merged/archived records created via `merge` endpoints, consolidating original data into core business tables
3. **Middle/summary data** — aggregated via `flush` endpoints (`t_order_summary`, `t_day_summary`, `t_deduction_summary`, etc.)
4. **Report data** — read-only queries against summary and trunk tables, returned to frontend charts and tables

### Module organization

Each business module follows the same structure:
```
app/models/<module>/   # Django ORM models or native SQL classes
app/views/<module>/    # View functions (one file per resource)
app/url/<module>.py    # URL list for the module
client/src/api/<module>/   # Frontend API wrappers
client/src/views/<module>/ # Vue page components
client/src/router/modules/<module>.js  # Route definitions with role codes
```

### Key conventions

- Password storage: MD5 hashes (frontend MD5s the plaintext before POST; `DefaultPassword.VALUE` stores the MD5 of `888888`)
- Response encoder: `MyJSONEncoder` formats `datetime` as `'%Y-%m-%d %H:%M:%S'`
- CORS: `django-cors-headers` enabled, `CorsMiddleware` placed before `CommonMiddleware`
- Timezone: `Asia/Shanghai` with `USE_TZ = False` (naive datetimes)
- Static files: Django serves from root `static/` directory
- Database: SQLite with 500ms timeout; file is `cxkw.db` in repo root
- CharField encoding concerns: some historical files have non-UTF-8 Chinese text; use UTF-8 for all new changes
