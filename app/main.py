from fastapi import FastAPI
from app.routers import employee, session, customer

app = FastAPI()

app.include_router(employee.router)
app.include_router(session.router)
app.include_router(customer.router)



