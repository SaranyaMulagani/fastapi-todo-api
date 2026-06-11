# ✅ FastAPI Todo API

A production-ready REST API built with **FastAPI**, **SQLAlchemy**, and **JWT Authentication**.  
Every user can register, login, and manage their own private todo list.

---

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework |
| **SQLAlchemy** | ORM — database operations |
| **SQLite** | Database (local dev) |
| **JWT (python-jose)** | Authentication tokens |
| **bcrypt (passlib)** | Password hashing |
| **Pydantic v2** | Data validation |
| **Docker** | Containerization |
| **Render.com** | Deployment |

---

## 📌 Features

- ✅ User registration and login
- ✅ JWT token-based authentication
- ✅ Each user only sees their own todos
- ✅ Full CRUD — Create, Read, Update, Delete todos
- ✅ Filter todos by status (completed/pending) and priority
- ✅ Pagination support
- ✅ Auto-generated Swagger UI docs
- ✅ Dockerized

---

## 📁 Project Structure

```
fastapi-todo-api/
├── main.py           # App entry point
├── database.py       # DB connection & session
├── models.py         # SQLAlchemy table models
├── schemas.py        # Pydantic request/response models
├── auth.py           # JWT logic & password hashing
├── routers/
│   ├── users.py      # Register, login, profile endpoints
│   └── todos.py      # Todo CRUD endpoints
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## ⚡ API Endpoints

### 👤 Users
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/users/register` | Register new account | ❌ |
| POST | `/users/login` | Login, get JWT token | ❌ |
| GET | `/users/me` | Get my profile | ✅ |
| DELETE | `/users/me` | Delete my account | ✅ |

### ✅ Todos
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/todos/` | Get all my todos | ✅ |
| POST | `/todos/` | Create new todo | ✅ |
| GET | `/todos/{id}` | Get single todo | ✅ |
| PUT | `/todos/{id}` | Update todo | ✅ |
| PATCH | `/todos/{id}/complete` | Mark as complete | ✅ |
| DELETE | `/todos/{id}` | Delete todo | ✅ |
| DELETE | `/todos/` | Delete all todos | ✅ |

---

## 🛠️ How to Run Locally

### Option 1 — Run directly

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/fastapi-todo-api.git
cd fastapi-todo-api

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env and set your SECRET_KEY

# 5. Run the server
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

### Option 2 — Run with Docker

```bash
docker-compose up --build
```

---

## 🧪 Testing the API

1. Open **http://localhost:8000/docs** (Swagger UI)
2. Register a user: `POST /users/register`
3. Login: `POST /users/login` → copy the `access_token`
4. Click **Authorize** (top right), paste: `Bearer <your_token>`
5. Now you can create and manage todos!

---

## 🌐 Deployment (Render.com)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: `SECRET_KEY`, `DATABASE_URL`
6. Deploy!

---

## 📖 What I Learned Building This

- FastAPI routing, request/response models with Pydantic v2
- JWT authentication flow (register → login → protected routes)
- SQLAlchemy ORM for database operations
- Dependency injection pattern with `Depends()`
- Docker containerization
- Deploying FastAPI to cloud

---

## 👨‍💻 Author

Built as part of my FastAPI learning journey.  
Part of a larger goal: becoming a **Gen AI + FastAPI developer**.

---

## 📄 License

MIT
