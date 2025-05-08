# NTQ78 - Books App

A full-stack Books App with a FastAPI backend (Celery, SQLAlchemy, JWT, Cloudinary) and a React Native (Expo) mobile frontend.

---

## Project Structure

```
NTQ78/
├── backend/   # FastAPI backend, Celery worker, database, and API logic
├── mobile/    # React Native (Expo) mobile app
├── README.md  # Project documentation
```

---

## Backend (FastAPI, Celery)
- **Python 3.11**
- **FastAPI** for REST APIs
- **Celery** for background tasks
- **SQLAlchemy** ORM (MySQL/SQL Server)
- **JWT Authentication**
- **Cloudinary** for image upload
- **Docker & docker-compose** support

### Features
- User authentication (register, login, JWT)
- Book management (CRUD, pagination, upload cover image)
- Profile management (view, update, upload avatar)
- Background processing (Celery)
- Exception handling

### Run Backend Locally
```sh
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Run Backend with Docker
```sh
docker build -t ntq78-backend .
docker run -p 8000:8000 ntq78-backend
```

### Run with Docker Compose (from project root)
```sh
docker-compose up --build
```

### Celery Worker
```sh
celery -A celery_temp.celery_worker.celery_app worker --loglevel=info
```

### API Documentation
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Environment Variables
- Add your environment variables in `.env` files (do not commit them).
- Update `docker-compose.yml` as needed for your environment.

---

## Mobile (React Native/Expo)
- **Expo + TypeScript**
- UI in `mobile/app/`

### Run Mobile App
```sh
cd mobile
npm install
npx expo start
```
- Use the QR code to open the app on your device with Expo Go, or run on an emulator.

### Build for Production
```sh
npx expo build:android   # Android APK
npx expo build:ios       # iOS build (requires Mac)
```

---

## UI Screenshots

### Mobile UI
| Home Screen | Book Details | Settings |
|-------------|-------------|----------|
| ![Home](mobile/assets/images/react-logo.png) | ![Details](mobile/assets/images/partial-react-logo.png) | ![Settings](mobile/assets/images/adaptive-icon.png) |

### Backend API (Swagger UI)
- Visit `http://localhost:8000/docs` after running the backend to explore the API interactively.

---

## API Overview
- **User**: Register, login, profile, update, delete
- **Book**: List, create, update, delete, upload cover image, pagination
- **Profile**: View and update profile, upload avatar

---

## Contribution
1. Fork this repo
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

---

## License
MIT

---

## Contact
- Author: Nguyen Trung Quoc
- Email: ntquoc.work@gmail.com
- Issues: [GitHub Issues](https://github.com/NTQ78/NTQ78/issues)
