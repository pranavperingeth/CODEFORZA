"""
main.py — FastAPI application factory and entry point.

Responsibilities:
  - Create the FastAPI app with metadata
  - Register middleware (CORS, rate-limiting)
  - Mount all routers under /api/*
  - Serve the frontend static files
  - Create DB tables on startup (create_all)
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app import models
from app.database import engine
from app.dependencies import get_current_user
from app.routers.auth_router import router as auth_router
from app.routers.judge_router import router as judge_router
from app.routers.problems_router import router as problems_router
from app.routers.rankings_router import router as rankings_router
from app.routers.users_router import router as users_router

# ── Path resolution ───────────────────────────────────────────────────────────
_APP_DIR = os.path.dirname(os.path.abspath(__file__))     # backend/app/
_BACKEND_DIR = os.path.dirname(_APP_DIR)                   # backend/
_PROJECT_DIR = os.path.dirname(_BACKEND_DIR)               # college-cp/
FRONTEND_DIR = os.path.join(_PROJECT_DIR, "frontend")


# ── Lifespan (startup/shutdown) ───────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables that don't exist yet (idempotent — safe to re-run)
    models.Base.metadata.create_all(bind=engine)
    yield
    # (add cleanup here if needed)


# ── Rate limiter ──────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


# ── App factory ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="College CP — Competitive Programming Platform",
    description=(
        "A Codeforces-like platform for college students. "
        "Supports online judge (Python, C++, C, Java), "
        "user/admin roles, and problem management."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── Middleware ────────────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    # For local dev only — tighten this in production
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── API Routers ───────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(problems_router)
app.include_router(judge_router)
app.include_router(rankings_router)


# ── Frontend static serving ───────────────────────────────────────────────────
if os.path.exists(FRONTEND_DIR):
    # CSS, JS, images etc. served from /static/
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ── Server-side auth guard for protected HTML pages ───────────────────────────
# admin.html is ONLY served to users with a valid admin JWT.
# Any other visitor gets a 302 redirect to login — the HTML never reaches them.
@app.get("/admin.html", include_in_schema=False)
def serve_admin(
    current_user: models.User = Depends(get_current_user),
):
    """
    Server-side guard: only admins receive the admin page HTML.
    Non-admins are redirected; unauthenticated requests raise 401.
    """
    if current_user.role != models.UserRole.admin:
        return RedirectResponse(url="/dashboard.html", status_code=302)
    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))


@app.get("/{page}.html", include_in_schema=False)
def serve_page(page: str):
    """
    Serve other *.html files. Admin page is handled separately above
    with server-side auth so this wildcard never matches it.
    """
    filepath = os.path.join(FRONTEND_DIR, f"{page}.html")
    if os.path.exists(filepath):
        return FileResponse(filepath)
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "version": "1.0.0"}
