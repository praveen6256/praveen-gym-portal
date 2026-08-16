from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import connect_db, close_db
from app.config import get_settings
from app.routers import auth, members, workouts, nutrition, admin

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Praveen Gym Portal API",
    description="Backend API for Praveen Gym Portal — member management, workouts, nutrition, and admin.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "traceback": tb.splitlines()}
        )

# Register routers both with and without /api/v1 prefix
app.include_router(auth.router)
app.include_router(members.router)
app.include_router(workouts.router)
app.include_router(nutrition.router)
app.include_router(admin.router)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(members.router, prefix="/api/v1")
app.include_router(workouts.router, prefix="/api/v1")
app.include_router(nutrition.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


@app.get("/test-db", tags=["Health"])
async def test_db():
    from app.database import get_db
    try:
        db = get_db()
        count = await db.users.count_documents({})
        return {"status": "ok", "user_count": count}
    except Exception as e:
        tb = traceback.format_exc()
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": tb.splitlines()})


@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "Praveen Gym Portal API",
        "status": "running",
        "version": "1.0.0",
        "tagline": "Train Smart. Eat Better. Become Stronger.",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
