from fastapi import FastAPI
from shiori.api.routers import health

app = FastAPI(title="Shiori Security Research Agent")

app.include_router(health.router)
