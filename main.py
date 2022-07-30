from fastapi import FastAPI
from models import router

app = FastAPI()
app.include_router(router)
