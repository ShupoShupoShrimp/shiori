from fastapi import FastAPI

from shiori.api.routers import health, query

app = FastAPI(title="Shiori Security Research Agent")

app.include_router(health.router)
app.include_router(query.router)
