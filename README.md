# notesAPI

My first backend project. A REST API for notes — create, edit, delete, and like them. Built with FastAPI and PostgreSQL.

---

## Stack

- **FastAPI** — framework
- **PostgreSQL** — database
- **SQLAlchemy + Alembic** — ORM and migrations
- **JWT** — authentication (the part that took the longest to figure out)
- **Pydantic** — request/response validation

---

## Run locally

```bash
git clone https://github.com/CodeWithAffection/notesAPI.git
cd notesAPI
pip install -r requirements.txt
```

Set up your `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/notesdb
SECRET_KEY=your_secret_key
```

Run migrations:
```bash
alembic upgrade head
```

Start the server:
```bash
uvicorn main:app --reload
```

All endpoints are documented in Swagger — open `http://localhost:8000/docs` after starting the server.

---

## What I learned

This was my first time building a backend from scratch. The main challenge was JWT — understanding how tokens are issued, validated, and how to protect routes properly. Alembic migrations also clicked after a couple of broken attempts.
