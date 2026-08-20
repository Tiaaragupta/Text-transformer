# The Text Transformer

A full-stack text transformation web app built as part of a 4-week internship project. Started as a simple local text utility (Week 1-2) and evolved into a containerized, database-backed, AI-integrated application deployed live on the internet.

**🔗 Live App:** https://text-transformer-3702.onrender.com

---

## Features

- **Local transforms** (instant, no external calls): Uppercase, Lowercase, Title Case, Reverse
- **AI-powered transforms** (via Google Gemini API): Summarize, Improve Writing, Formal Tone
- **Submission history**: every transformation is saved and viewable at `/history`, newest first
- **Persistent storage**: backed by PostgreSQL in production, with automatic fallback to SQLite for local development

---

## Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| Backend        | Flask (Python)                       |
| Database ORM   | SQLAlchemy / SQLModel                |
| Migrations     | Alembic                              |
| Database       | PostgreSQL (production), SQLite (local dev) |
| AI Integration | Google Gemini API                    |
| Frontend       | HTML, CSS, vanilla JS                |
| Containerization | Docker, Docker Compose             |
| Hosting        | Render (Web Service + managed PostgreSQL) |
| Version Control| Git / GitHub (feature branch + PR workflow) |

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

In production, the Flask app and PostgreSQL database run as two separate services on Render, communicating over Render's internal network. Locally, the same setup is reproduced with Docker Compose (`web` + `db` containers).

---

## Project Structure

```
Text-transformer/
├── app.py                  # Main Flask application & routes
├── database.py             # DB engine/session setup (SQLite/PostgreSQL switch)
├── models.py                # SQLModel table definitions
├── ai_service.py            # Gemini API integration (summarize/improve/formal tone)
├── alembic/                  # Database migration scripts
│   ├── env.py
│   └── versions/
├── alembic.ini
├── templates/
│   ├── index.html            # Main transformer UI
│   └── history.html          # Submission history page
├── static/                   # CSS/JS assets
├── requirements.txt
├── Dockerfile                # Builds the Flask app image
├── docker-compose.yml        # Runs app + PostgreSQL together
├── .env                      # Local secrets (GEMINI_API_KEY) — not committed
└── README.md
```

---

## Running Locally (without Docker)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Create a .env file with:
# GEMINI_API_KEY=your_key_here

python app.py
```
Visit `http://127.0.0.1:5000`. Uses local SQLite (`skypoint.db`) by default.

---

## Running Locally with Docker

```bash
docker compose up --build
```

This spins up two containers:
- `web` — the Flask app (port 5000)
- `db` — a PostgreSQL 16 instance (port 5432)

Visit `http://localhost:5000`. Data now persists to PostgreSQL instead of SQLite.

---

## Environment Variables

| Variable          | Description                                  |
|--------------------|-----------------------------------------------|
| `GEMINI_API_KEY`   | API key for Google Gemini (AI transforms)     |
| `DATABASE_URL`     | PostgreSQL connection string (falls back to local SQLite if unset) |

---

## Database Migrations

Migrations are managed with Alembic:

```bash
alembic upgrade head        # apply migrations
alembic revision --autogenerate -m "description"   # create a new migration
```

---

## Deployment (Render)

The app is deployed on Render as two services:
1. **PostgreSQL database** (`text-transformer-db`) — managed Postgres instance
2. **Web Service** (`text-transformer`) — built directly from the repo's `Dockerfile`, deployed from the `feature/ai-integration` branch

Environment variables (`DATABASE_URL`, `GEMINI_API_KEY`) are configured directly in the Render dashboard and are not committed to the repository.

Every push to the connected branch triggers an automatic rebuild and redeploy.

---

## Git Workflow

Following trunk-based development 

1. `git checkout main && git pull origin main`
2. `git checkout -b feature/<name>`
3. Commit work on the feature branch
4. `git push -u origin feature/<name>`
5. Open a PR into `main`
6. Wait for review before merging — no direct commits to `main`

---

## Weekly Progress Summary

- **Week 1-2:** Core text transformation logic + basic frontend
- **Week 3:** Database persistence layer (SQLModel + Alembic), submission history page
- **Week 4:** Gemini AI integration (Summarize / Improve Writing / Formal Tone), PostgreSQL migration, Docker containerization, live deployment to Render

---

## Known Limitations / Future Improvements

- Free-tier Render instance spins down after inactivity, causing a ~50s cold-start delay on the first request
- No loading indicator on the frontend while waiting for AI responses
- No automated tests yet
