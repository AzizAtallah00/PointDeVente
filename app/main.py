from fastapi import FastAPI
from app.routers import employee

app = FastAPI()

app.include_router(employee.router)



