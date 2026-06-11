from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, todos

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="A complete Todo REST API with JWT Authentication built with FastAPI",
    version="1.0.0"
)

# CORS - allows frontend apps to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(todos.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Todo API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
