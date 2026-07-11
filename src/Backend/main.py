from fastapi import FastAPI

from src.Backend.api.routes import router


app=FastAPI(
    title="Used Phone Price Detection",
    version="1.0.0.3",
    description="Price Detection App"
)
app.include_router(router,prefix="/api")