My first backend project. A REST API for notes — create, edit, delete, and like them. Built with FastAPI and PostgreSQL.

## Stack

- **FastAPI** — framework
- **PostgreSQL** — database
- **SQLAlchemy + Alembic** — ORM and migrations
- **JWT** — authentication (the part that took the longest to figure out)
- **Pydantic** — request/response validation

## Run locally

Set up your ".env":
DATABASE_URL=postgresql://user:password@localhost/notesdb
SECRET_KEY=your_secret_key

Run migrations:
alembic upgrade head

Start the server:
uvicorn main:app --reload

All endpoints are documented in Swagger — open `http://localhost:8000/docs` after starting the server.

