
## Stack

- **FastAPI** — framework
- **PostgreSQL** — database
- **SQLAlchemy + Alembic** — ORM and migrations
- **JWT** — authentication 
- **Pydantic** - request/response validation

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

![Swagger UI](image.png)

