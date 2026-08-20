# The Text Transformer

A text transformation app I built over a 4-week internship. Started out as a simple local script in week 1-2 (just uppercase/lowercase/reverse type stuff), then grew into a full app with a database, AI integration, and a live deployment.

Live app: https://text-transformer-3702.onrender.com

---

## What it does

You type in some text and pick a transform. There are two kinds:

- Local transforms — uppercase, lowercase, title case, reverse. These run instantly, no API calls involved.
- AI transforms — summarize, improve writing, formal tone. These hit the Google Gemini API.

Every transform gets saved to the database, and you can see your history at `/history`, newest first. In production this runs on PostgreSQL; locally it falls back to SQLite automatically if there's no `DATABASE_URL` set.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Flask (Python) |
| ORM | SQLAlchemy / SQLModel |
| Migrations | Alembic |
| Database | PostgreSQL (prod), SQLite (local) |
| AI | Google Gemini API |
| Frontend | HTML, CSS, vanilla JS |
| Containers | Docker, Docker Compose |
| Hosting | Render |
| Version control | Git/GitHub, feature branches + PRs |

---

## Architecture

```
┌─────────────┐      HTTP       ┌──────────────┐
│   Browser   │ ───────────────▶│  Flask App   │
│ (HTML/CSS/JS)│◀─────────────── │  (app.py)    │
└─────────────┘                 └──────┬───────┘
                                        │
                       ┌────────────────┼────────────────┐
                       ▼                                  ▼
              ┌─────────────────┐              ┌────────────────────┐
              │  Local transforms │              │  Gemini API call    │
              │ (uppercase, etc.) │              │ (ai_service.py)     │
              └─────────────────┘              └────────────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │  PostgreSQL Database │
              │  (via SQLAlchemy)     │
              │  transformation table │
              └─────────────────────┘
```

In production, the Flask app and PostgreSQL run as two separate services on Render, talking over Render's internal network. Locally I reproduce the same setup with Docker Compose (`web` + `db` containers).

---

## Project structure

```
Text-transformer/
├── app.py                  # Main Flask app & routes
├── database.py             # DB engine/session setup (SQLite/PostgreSQL switch)
├── models.py                # SQLModel table definitions
├── ai_service.py            # Gemini API integration
├── alembic/                  # Migration scripts
│   ├── env.py
│   └── versions/
├── alembic.ini
├── templates/
│   ├── index.html            # Main UI
│   └── history.html          # History page
├── static/                   # CSS/JS
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env                      # Local secrets, not committed
└── README.md
```

---

## Running locally (no Docker)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# create a .env file with:
# GEMINI_API_KEY=your_key_here

python app.py
```

Then go to `http://127.0.0.1:5000`. Uses SQLite (`skypoint.db`) by default.

---

## Running locally with Docker

```bash
docker compose up --build
```

Spins up two containers:
- `web` — the Flask app, port 5000
- `db` — PostgreSQL 16, port 5432

Go to `http://localhost:5000`. This time data persists to PostgreSQL instead of SQLite.

---

## Environment variables

| Variable | What it's for |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key for the AI transforms |
| `DATABASE_URL` | PostgreSQL connection string. Falls back to local SQLite if not set |

---

## Database migrations

Using Alembic:

```bash
alembic upgrade head        # apply migrations
alembic revision --autogenerate -m "description"   # create a new one
```

---

## Deployment

Deployed on Render as two services:
1. PostgreSQL database (`text-transformer-db`) — managed instance
2. Web service (`text-transformer`) — built from the repo's `Dockerfile`, deployed off the `feature/ai-integration` branch

Env vars (`DATABASE_URL`, `GEMINI_API_KEY`) are set directly in the Render dashboard, not committed anywhere. Every push to the connected branch auto-rebuilds and redeploys.

---

## Git workflow

Trunk-based development:

1. `git checkout main && git pull origin main`
2. `git checkout -b feature/<name>`
3. Commit work on the feature branch
4. `git push -u origin feature/<name>`
5. Open a PR into `main`
6. Wait for review before merging — no direct commits to `main`

---

## Progress by week

- Week 1-2: core transform logic + basic frontend
- Week 3: database persistence (SQLModel + Alembic), history page
- Week 4: Gemini AI integration, PostgreSQL migration, Docker, live deployment on Render

---

## Known limitations

- Free-tier Render instance spins down when idle, so the first request after a while has a ~50s cold start
- No loading indicator on the frontend while waiting on the AI response
- No automated tests yet
