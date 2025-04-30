# Books App Monorepo

This repository contains the source code for a Books App, including both the backend (FastAPI, Celery) and the mobile frontend (React Native/Expo).

---

## Project Structure

```
backend/   # FastAPI backend, Celery worker, database, and API logic
mobile/    # React Native (Expo) mobile app
```

---

## Backend (FastAPI, Celery)
- Python 3.11
- FastAPI for REST API
- Celery for background tasks
- SQL Server/MySQL (configurable)
- Docker & docker-compose support

### Run Backend Locally
```sh
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Run Backend with Docker
```sh
docker build -t books-backend .
docker run -p 8000:8000 books-backend
```

### Run with Docker Compose (from project root)
```sh
docker-compose up --build
```

---

## Mobile (React Native/Expo)
- Expo + TypeScript
- UI in `mobile/app/`

### Run Mobile App
```sh
cd mobile
npm install
npx expo start
```

---

## Push Code to GitHub

1. **Create a repository on GitHub (if not done):**
   - Go to https://github.com/new and create a repo (e.g., books-app)

2. **Initialize git and commit (if not done):**
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Add remote and push:**
   ```sh
   git remote add origin https://github.com/YOUR-USERNAME/books-app.git
   git branch -M main
   git push -u origin main
   ```

---

## Notes
- Add your environment variables in `.env` files (do not commit them).
- Update `docker-compose.yml` as needed for your environment.
- For Celery, make sure Redis or RabbitMQ is running as a broker.

---

## Screenshots


---

## License
MIT
