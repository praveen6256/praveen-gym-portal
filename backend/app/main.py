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

from fastapi.responses import JSONResponse
import traceback

@app.middleware("http")
async def catch_exceptions_middleware(request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": f"MIDDLEWARE ERROR: {str(exc)}", "traceback": tb.splitlines()}
        )

from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"GLOBAL ERROR: {tb}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": tb.splitlines()}
    )

# Register routers
app.include_router(auth.router)
app.include_router(members.router)
app.include_router(workouts.router)
app.include_router(nutrition.router)
app.include_router(admin.router)


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
