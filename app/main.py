from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.routers import point
from app.config import settings

app = FastAPI(docs_url=settings.docs_url, redoc_url=None)

app.include_router(point.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts
)


@app.get("/")
def read_root():
    return {"Hello": "World", "env": settings.runtime_env}


@app.get("/ping")
def ping():
    return "is ok"
