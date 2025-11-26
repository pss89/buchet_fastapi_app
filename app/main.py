from fastapi import FastAPI, __version__
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes.users import router as users_router

import subprocess

app = FastAPI(title=settings.APP_NAME)

origins = settings.CORS_ORIGINS or ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/hello")
async def health():
    return {
        "message": "Hello, Python FastAPI",
        "Python-Framework": "FastAPI "+__version__,
    }

# app.include_router(users_router)

# @app.get("/health")
# async def health():
#     return {"status": "ok"}

# @app.get("/hello")
# async def health():
#     return {
#         "message": "Hello, Python FastAPI",
#         "Python-Framework": "FastAPI "+__version__,
#     }
