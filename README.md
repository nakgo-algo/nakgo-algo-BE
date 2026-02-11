# NakgoAlgo Backend (FastAPI)

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export JWT_SECRET_KEY="replace-with-strong-random-secret-min-32-chars"
uvicorn app.main:app --reload --port 8081
```

Base URL: `http://localhost:8081/api`

## Auth notes

- `POST /api/auth/kakao` returns `token`, `refreshToken`, `user`
- `POST /api/auth/refresh` rotates refresh token and returns new `token`, `refreshToken`
