from fastapi import FastAPI

from src.controllers.time_controller import router as time_router

app = FastAPI()

app.include_router(time_router)