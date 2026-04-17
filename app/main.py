from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import Base, engine
from app.routers.profiles import router as profiles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
app = FastAPI(title="Data Persistence API Design Assessment", lifespan=lifespan)

# CORS - wildcard required by grading script
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(profiles_router)


@app.get("/")
def home():
    return "Welcome to the Data Persistence API Design Assessment"