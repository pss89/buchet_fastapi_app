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

@app.get("/")
async def hello():
    return {
        "message": "Hello, Python FastAPI",
        "Python-Framework": "FastAPI "+__version__,
    }
    
@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(users_router)

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/hello")
# async def health():
#     return {
#         "message": "Hello, Python FastAPI",
#         "Python-Framework": "FastAPI "+__version__,
#     }
