from fastapi import FastAPI
from app.routers import employee, session

app = FastAPI()

app.include_router(employee.router)
app.include_router(session.router)



